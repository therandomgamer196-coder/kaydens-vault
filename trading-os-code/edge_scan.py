"""Probability board: for each market, which setups have historically gone up.
Daily bars (2 years stocks/futures via Yahoo, ~2 years crypto via Coinbase).
A signal is checked on a closed day; the "trade" is entry at that close,
target +1 ATR(14), stop -1 ATR(14), up to 10 bars (both hit in one bar = loss).
Decent = win >= 55%, n >= 25, 3+ pts over baseline, and >= 52% in both halves of history (out-of-sample check).
Crypto results are shown after the 1.9% round-trip Robinhood fee."""
import json, sys, time, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York"); UA = {"User-Agent": "Mozilla/5.0"}
STOCKS = [("QQQ", "Nasdaq-100 ETF", "eq"), ("SPY", "S&P 500 ETF", "eq"), ("NQ=F", "Nasdaq futures", "fut"), ("USO", "Oil ETF", "eq"), ("GLD", "Gold ETF", "eq"),
          ("NVDA", "Nvidia", "eq"), ("GOOGL", "Google", "eq"), ("MSFT", "Microsoft", "eq"), ("PLTR", "Palantir", "eq")]
COINS = [("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("SOL", "Solana"), ("XRP", "XRP"), ("DOGE", "Dogecoin"), ("ADA", "Cardano"), ("LINK", "Chainlink"), ("AVAX", "Avalanche"), ("LTC", "Litecoin"), ("PEPE", "Pepe"), ("BONK", "Bonk"), ("WIF", "dogwifhat"), ("PENGU", "Pudgy Penguins")]
FEE_RT = 1.9  # % round trip, crypto only
H = 10

import builtins
def round(x, n=None):  # meme coins trade under $0.01: keep 6 significant figures for those prices (2026-10-04)
    if n is None: return builtins.round(x)
    return float(f"{x:.6g}") if n == 6 and abs(x) < 0.01 else builtins.round(x, n)

def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r: return json.loads(r.read().decode())
        except Exception as e: err = e; time.sleep(2 * (i + 1))
    raise RuntimeError(str(err)[:120])

def yahoo(sym):
    r = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=2y")["chart"]["result"][0]
    q = r["indicators"]["quote"][0]; out = []
    today = dt.datetime.now(ET).date()
    for i, t in enumerate(r["timestamp"]):
        o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if None in (o, h, l, c): continue
        d = dt.datetime.fromtimestamp(t, ET).date()
        out.append(dict(d=d, o=o, h=h, l=l, c=c))
    now = dt.datetime.now(ET)
    if out and out[-1]["d"] == today and now.weekday() < 5 and now.time() < dt.time(16, 15): out.pop()  # drop today's unfinished bar
    return out

def coinbase(sym):
    end = int(time.time()) // 86400 * 86400; rows = {}
    for _ in range(3):
        start = end - 300 * 86400
        raw = get(f"https://api.exchange.coinbase.com/products/{sym}-USD/candles?granularity=86400&start={dt.datetime.utcfromtimestamp(start).isoformat()}&end={dt.datetime.utcfromtimestamp(end).isoformat()}")
        for r in raw: rows[r[0]] = r
        end = start; time.sleep(0.4)
    bars = [dict(d=dt.datetime.utcfromtimestamp(k).date(), l=v[1], h=v[2], o=v[3], c=v[4]) for k, v in sorted(rows.items())]
    if bars and bars[-1]["d"] >= dt.datetime.utcnow().date(): bars.pop()  # unfinished UTC day
    return bars

def ema(xs, n):
    out, k, e = [], 2 / (n + 1), None
    for i, x in enumerate(xs):
        e = x if e is None else x * k + e * (1 - k); out.append(e if i >= n - 1 else None)
    return out

def rsi(xs, n=14):
    out = [None] * len(xs); ag = al = 0
    for i in range(1, len(xs)):
        g, l = max(xs[i] - xs[i-1], 0), max(xs[i-1] - xs[i], 0)
        if i <= n: ag += g / n; al += l / n
        else: ag = (ag * (n - 1) + g) / n; al = (al * (n - 1) + l) / n
        if i >= n: out[i] = 100 if al == 0 else 100 - 100 / (1 + ag / al)
    return out

def atr(b, n=14):
    out, a = [None] * len(b), None
    for i in range(1, len(b)):
        tr = max(b[i]["h"] - b[i]["l"], abs(b[i]["h"] - b[i-1]["c"]), abs(b[i]["l"] - b[i-1]["c"]))
        a = tr if a is None else (a * (n - 1) + tr) / n
        if i >= n: out[i] = a
    return out

SIGNALS = [
    ("pullback", "Uptrend pullback", "20 EMA above 50 EMA, close above the 50, RSI under 45"),
    ("oversold", "Oversold bounce", "RSI(14) under 30"),
    ("pdl_sweep", "Prior-day low sweep", "Dipped under yesterday's low, closed back above it"),
    ("breakout", "20-day breakout in uptrend", "Closed at a 20-day high with 20 EMA above 50 EMA"),
    ("three_down", "3 red days in uptrend", "3 lower closes in a row, still above the 50 EMA"),
]

def flags(b, i, c, e20, e50, r):
    if i < 55 or None in (e20[i], e50[i], r[i]): return {}
    up = e20[i] > e50[i]
    return {
        "pullback": up and c[i] > e50[i] and r[i] < 45,
        "oversold": r[i] < 30,
        "pdl_sweep": b[i]["l"] < b[i-1]["l"] and c[i] > b[i-1]["l"],
        "breakout": up and c[i] >= max(c[i-19:i+1]),
        "three_down": c[i] < c[i-1] < c[i-2] < c[i-3] and c[i] > e50[i],
    }

def outcome(b, i, a):
    entry, tgt, stp = b[i]["c"], b[i]["c"] + a, b[i]["c"] - a
    for j in range(i + 1, min(len(b), i + 1 + H)):
        hs, ls = b[j]["h"] >= tgt, b[j]["l"] <= stp
        if ls: return 0
        if hs: return 1
    if i + H >= len(b): return None  # not enough future bars yet
    return 1 if b[i + H]["c"] > entry else 0

def analyze(key, name, kind, bars):
    c = [x["c"] for x in bars]; e20, e50, r, a = ema(c, 20), ema(c, 50), rsi(c), atr(bars)
    hist = {s[0]: [] for s in SIGNALS}; base = []
    last = len(bars) - 1
    for i in range(55, last + 1):
        f = flags(bars, i, c, e20, e50, r)
        if not f or a[i] is None: continue
        o = outcome(bars, i, a[i])
        if o is None: continue
        up5 = (c[i + 5] > c[i]) if i + 5 <= last else None
        rec = (i, o, up5, a[i] / c[i] * 100)
        base.append(rec)
        for k, v in f.items():
            if v: hist[k].append(rec)
    mid = bars[(55 + last) // 2]["d"]
    def stats(rs):
        if not rs: return dict(n=0)
        w = sum(x[1] for x in rs) / len(rs) * 100
        u = [x[2] for x in rs if x[2] is not None]
        half1 = [x[1] for x in rs if bars[x[0]]["d"] < mid]; half2 = [x[1] for x in rs if bars[x[0]]["d"] >= mid]
        atrp = sum(x[3] for x in rs) / len(rs)
        exp = (w / 100 * 2 - 1) * atrp - (FEE_RT if kind == "crypto" else 0)  # % per trade, 1:1 ATR bracket (approx)
        return dict(n=len(rs), win=round(w, 1), up5=round(sum(u) / len(u) * 100, 1) if u else None,
                    win_h1=round(sum(half1) / len(half1) * 100, 1) if half1 else None, n_h1=len(half1),
                    win_h2=round(sum(half2) / len(half2) * 100, 1) if half2 else None, n_h2=len(half2), exp_pct=round(exp, 2))
    now_f = flags(bars, last, c, e20, e50, r) or {}
    sigs = []
    for sid, label, rule in SIGNALS:
        s = stats(hist[sid])
        sigs.append(dict(id=sid, label=label, rule=rule, active=bool(now_f.get(sid)), **s))
    b = stats(base)
    for s in sigs:
        s["edge"] = round(s["win"] - b["win"], 1) if s["n"] else None
        s["decent"] = bool(s["n"] >= 25 and s["win"] >= 55 and s["edge"] >= 3 and (s["win_h1"] or 0) >= 52 and (s["win_h2"] or 0) >= 52 and s["exp_pct"] > 0)
    px, at = c[last], a[last]
    live = [s for s in sigs if s["active"]]
    good = sorted([s for s in live if s["decent"]], key=lambda s: -s["win"])
    if good: status = "Decent odds now"
    elif live: status = "Signal, weak history"
    else: status = "No setup today"
    best = good[0] if good else None
    nd = 6 if px < 5 else 2
    downs = 0
    for k in range(last, 0, -1):
        if c[k] < c[k-1]: downs += 1
        else: break
    # price that would push RSI(14) to a threshold on the next close (Wilder smoothing)
    ag = al = 0.0
    for k in range(1, len(c)):
        g_, l_ = max(c[k] - c[k-1], 0), max(c[k-1] - c[k], 0)
        if k <= 14: ag += g_ / 14; al += l_ / 14
        else: ag = (ag * 13 + g_) / 14; al = (al * 13 + l_) / 14
    def rsi_px(th):
        L = 13 * ((100 - th) / th * ag - al)
        return round(c[last] - max(L, 0), nd)
    lvl = {
        "pullback": (rsi_px(45), "below"), "oversold": (rsi_px(30), "below"),
        "pdl_sweep": (round(bars[last]["l"], nd), "below"),
        "breakout": (round(max(c[last-19:last+1]), nd), "above"),
        "three_down": (round(c[last], nd), "below") if downs >= 2 and c[last] > e50[last] else (None, None),
    }
    trig = {
        "pullback": f"needs RSI under 45 (now {r[last]:.0f}) while the 20 EMA stays above the 50 ({'yes' if e20[last] > e50[last] else 'no'})",
        "oversold": f"needs RSI under 30 (now {r[last]:.0f})",
        "pdl_sweep": f"a dip under {round(bars[last]['l'], nd)} (today's low) that closes back above it",
        "breakout": f"a close above {round(max(c[last-19:last+1]), nd)} (20-day closing high) with the 20 EMA over the 50",
        "three_down": f"{downs} lower close{'s' if downs != 1 else ''} in a row now; needs 3 while above the 50 EMA ({round(e50[last], nd)})",
    }
    for s_ in sigs:
        s_["trigger"] = trig[s_["id"]]; s_["trigger_level"], s_["trigger_dir"] = lvl[s_["id"]]
    trend = "up" if e20[last] > e50[last] and px > e50[last] else "down" if e20[last] < e50[last] and px < e50[last] else "mixed"
    return dict(symbol=key.replace("=F", ""), yf=key, name=name, kind=kind, bar_date=str(bars[last]["d"]), price=round(px, 6 if px < 5 else 2),
                atr=round(at, 6 if px < 5 else 2), atr_pct=round(at / px * 100, 2), rsi=round(r[last], 1), trend=trend,
                ema20=round(e20[last], 6 if px < 5 else 2), ema50=round(e50[last], 6 if px < 5 else 2),
                baseline=b, signals=sigs, status=status, history_from=str(bars[55]["d"]), bars=len(bars),
                plan=best and dict(signal=best["label"], entry=round(px, 6 if px < 5 else 2), stop=round(px - at, 6 if px < 5 else 2),
                                   target=round(px + at, 6 if px < 5 else 2), win=best["win"], n=best["n"], edge_vs_base=round(best["win"] - b["win"], 1), exp_pct=best["exp_pct"]),
                closes=[round(x, 6 if px < 5 else 2) for x in c[-60:]])

def main():
    now = dt.datetime.now(ET); out = {}; errors = []
    for key, name, kind in STOCKS:
        try: out[key] = analyze(key, name, kind, yahoo(key))
        except Exception as e: errors.append(f"{key}: {e}")
    for key, name in COINS:
        try: out[key] = analyze(key, name, "crypto", coinbase(key))
        except Exception as e: errors.append(f"{key}: {e}")
    meta = dict(t=now.isoformat(timespec="seconds"), time=now.strftime("%-I:%M %p ET"), date=now.strftime("%a %b %-d"), errors=errors,
                method="Daily bars, about 2 years. Trade = buy at the signal day's close, target +1 ATR, stop -1 ATR, max 10 days (both in one day counts as a loss). "
                       "Baseline = the same trade on every day. 'Decent odds' = won at least 55% of at least 25 past signals AND at least 52% in both the older and newer half of the history, beat the market's own every-day baseline by 3+ points, with positive expectancy (crypto after the 1.9% round-trip fee). About 90 market/setup combos are tested, so a few will look good by luck: the half-and-half check filters most of that. Past odds, not a guarantee.",
                decent=[f"{v['symbol']} {v['plan']['signal']}" for v in out.values() if v["plan"]])
    json.dump(dict(meta=meta, markets=out), open(sys.argv[1] if len(sys.argv) > 1 else "edge.json", "w"), indent=1, default=str)
    print(json.dumps(meta, indent=1))
    for v in out.values():
        print(f"{v['symbol']:6} {v['status']:22} base {v['baseline']['win']}% n{v['baseline']['n']} | " + " ".join(f"{s['id']}:{s['win']}%/{s['n']}{'*' if s['decent'] else ''}{'!' if s['active'] else ''}" for s in v["signals"] if s["n"]))

main()
