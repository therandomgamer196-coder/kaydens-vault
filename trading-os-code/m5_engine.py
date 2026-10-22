#!/usr/bin/env python3
"""Z.E.R.O 5-minute engine (v1.0, 2026-10-16).

Kayden's 5m plan: enter on 5-minute candles, sell HALF at +5%, move the stop to entry,
trail the rest toward +20% and beyond. This script:
  1. builds a universe (focus list + liquid movers: market cap >= $2B, avg volume >= 1M),
  2. backtests 6 setup families on recent 5m bars (oldest 70% train, newest 30% unseen test),
  3. marks setups that pass both as PROVEN,
  4. says which proven setups fired on the latest closed bar, and which Robinhood alerts to keep.
Stdlib only. Usage: python3 m5.py OUT.json
"""
import json, sys, time, math, statistics, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo

VERSION = "1.0"
ET = ZoneInfo("America/New_York")
UA = {"User-Agent": "Mozilla/5.0 (ZERO-m5)"}
COST = {"crypto": 0.0095, "eq": 0.0005}
HALF_AT = 0.05                     # sell half at +5% (Kayden, 2026-10-16)
FOCUS_EQ = ["QQQ", "SPY", "GLD", "USO", "NVDA", "PLTR", "TSLA", "AMD", "COIN", "MSTR", "HOOD", "IONQ", "RKLB", "SMCI"]
FOCUS_CR = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "LINK", "AVAX", "SUI", "PEPE", "BONK", "SHIB", "HBAR", "XLM"]
MAX_DISC = 20
CRYPTO_PAGES = 18                  # 18 x 300 bars ~ 19 days of 5m candles
MAX_HOLD = {"eq": 78 * 5, "crypto": 288 * 3}   # 5 sessions / 3 days

def _get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception:
            if i == 2: raise
            time.sleep(1.2)


FINVIZ = {   # Kayden 2026-10-16: use Finviz to find names worth tracking. All screens: market cap > $2B, avg volume > 1M.
    "Top gainers": "cap_midover,sh_avgvol_o1000,ta_change_u5&o=-change",
    "Unusual volume": "cap_midover,sh_avgvol_o1000,sh_relvol_o2&o=-relativevolume",
    "New 52-week highs": "cap_midover,sh_avgvol_o1000,ta_highlow52w_nh&o=-change",
    "Oversold in uptrend": "cap_midover,sh_avgvol_o1000,ta_rsi_os30,ta_sma200_pa&o=rsi",
}
def finviz():
    """A few page loads per run (personal, low-volume use). Returns {screen: [tickers]}."""
    import re
    out = {}
    for name, f in FINVIZ.items():
        try:
            req = urllib.request.Request(f"https://finviz.com/screener.ashx?v=111&f={f}",
                                         headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"})
            with urllib.request.urlopen(req, timeout=20) as r: html = r.read().decode("utf-8", "ignore")
            seen = []
            for t in re.findall(r'data-boxover-ticker="([A-Z]{1,5})"', html):
                if t not in seen: seen.append(t)
            out[name] = seen[:20]
            time.sleep(1.0)
        except Exception as e:
            out[name] = []
    return out

def discover(fv=None):
    out = {}
    for scr in ("day_gainers", "most_actives", "day_losers"):
        try:
            for q in _get(f"https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?scrIds={scr}&count=100")["finance"]["result"][0]["quotes"]:
                s = q.get("symbol", "")
                if not s or any(c in s for c in ".-=^") or q.get("quoteType") not in ("EQUITY", "ETF"): continue
                if (q.get("marketCap") or 0) >= 2e9 and (q.get("averageDailyVolume3Month") or 0) >= 1e6:
                    out[s] = out.get(s, 0) + abs(q.get("regularMarketChangePercent") or 0)
        except Exception:
            pass
    for name, ts in (fv or {}).items():          # Finviz finds get a boost
        for k, t in enumerate(ts): out[t] = out.get(t, 0) + 10 - min(k, 9)
    return [s for s in sorted(out, key=out.get, reverse=True) if s not in FOCUS_EQ][:MAX_DISC]

def bars_eq(sym):
    j = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=5m&range=60d")["chart"]["result"][0]
    q = j["indicators"]["quote"][0]
    out = []
    for t, o, h, l, c, v in zip(j["timestamp"], q["open"], q["high"], q["low"], q["close"], q["volume"]):
        if None in (o, h, l, c): continue
        d = dt.datetime.fromtimestamp(t, ET)
        if not (dt.time(9, 30) <= d.time() < dt.time(16, 0)): continue
        out.append({"t": t, "day": d.date().isoformat(), "mins": d.hour * 60 + d.minute, "o": o, "h": h, "l": l, "c": c, "v": v or 0})
    return out

def bars_cr(sym):
    rows, end = {}, dt.datetime.now(dt.timezone.utc)
    for _ in range(CRYPTO_PAGES):
        st = end - dt.timedelta(minutes=5 * 299)
        for r in _get(f"https://api.exchange.coinbase.com/products/{sym}-USD/candles?granularity=300&start={st:%Y-%m-%dT%H:%M:%SZ}&end={end:%Y-%m-%dT%H:%M:%SZ}"):
            rows[r[0]] = r
        end = st
    out = []
    for t in sorted(rows):
        r = rows[t]; d = dt.datetime.fromtimestamp(t, dt.timezone.utc)
        out.append({"t": t, "day": d.date().isoformat(), "mins": d.hour * 60 + d.minute, "o": r[3], "h": r[2], "l": r[1], "c": r[4], "v": r[5]})
    return out

# ---------------------------------------------------------------- indicators
def ema(xs, p):
    a, e, out = 2 / (p + 1), None, []
    for x in xs:
        e = x if e is None else x * a + e * (1 - a); out.append(e)
    return out

def rsi(xs, p):
    out, ag, al = [None] * len(xs), 0.0, 0.0
    for i in range(1, len(xs)):
        ch = xs[i] - xs[i - 1]; g, l = max(ch, 0), max(-ch, 0)
        if i <= p:
            ag += g / p; al += l / p
            if i == p: out[i] = 100 if al == 0 else 100 - 100 / (1 + ag / al)
        else:
            ag = (ag * (p - 1) + g) / p; al = (al * (p - 1) + l) / p
            out[i] = 100 if al == 0 else 100 - 100 / (1 + ag / al)
    return out

class Mk:
    def __init__(self, sym, kind, b):
        self.sym, self.kind, self.b, self.n = sym, kind, b, len(b)
        c = [x["c"] for x in b]; self.c = c
        self.e9, self.e21, self.e50, self.e200 = ema(c, 9), ema(c, 21), ema(c, 50), ema(c, 200)
        self.r2 = rsi(c, 2)
        tr = [b[0]["h"] - b[0]["l"]] + [max(b[i]["h"] - b[i]["l"], abs(b[i]["h"] - c[i - 1]), abs(b[i]["l"] - c[i - 1])) for i in range(1, self.n)]
        a, self.atr = None, []
        for t in tr:
            a = t if a is None else (a * 13 + t) / 14; self.atr.append(a)
        v = [x["v"] for x in b]; self.vavg = []
        s = 0.0
        for i in range(self.n):
            s += v[i] - (v[i - 48] if i >= 48 else 0); self.vavg.append(s / min(i + 1, 48))
        # session VWAP (stocks: per day; crypto: rolling 288 bars = 24h)
        self.vwap, pv, vv, day = [], 0.0, 0.0, None
        q = []
        for i, x in enumerate(b):
            tp = (x["h"] + x["l"] + x["c"]) / 3
            if kind == "eq":
                if x["day"] != day: pv, vv, day = 0.0, 0.0, x["day"]
                pv += tp * x["v"]; vv += x["v"]
            else:
                q.append((tp * x["v"], x["v"])); pv += tp * x["v"]; vv += x["v"]
                if len(q) > 288:
                    a1, a2 = q.pop(0); pv -= a1; vv -= a2
            self.vwap.append(pv / vv if vv else x["c"])
        # prior-day low (stocks) / prior 24h low (crypto)
        self.plow = [None] * self.n
        if kind == "eq":
            lows, prev, cur, day = {}, None, None, None
            for i, x in enumerate(b):
                if x["day"] != day:
                    prev = lows.get(day); day = x["day"]; lows[day] = x["l"]
                else:
                    lows[day] = min(lows[day], x["l"])
                self.plow[i] = prev
            self.orh = [None] * self.n; hi, day = None, None
            for i, x in enumerate(b):
                if x["day"] != day: hi, day = None, x["day"]
                if x["mins"] < 600: hi = x["h"] if hi is None else max(hi, x["h"])
                self.orh[i] = hi if x["mins"] >= 600 else None
        else:
            from collections import deque
            dq = deque()
            for i, x in enumerate(b):
                if i >= 288: self.plow[i] = min(y["l"] for y in b[i - 288:i - 12]) if i % 1 == 0 else None
            self.orh = [None] * self.n

SETUPS = {
    "rsi2_dip":     {"label": "5m RSI(2) dip in an uptrend", "params": {"th": [5, 10, 20]}},
    "vwap_reclaim": {"label": "VWAP reclaim",                "params": {"k": [3, 6]}},
    "ema_cross":    {"label": "EMA 9/21 cross above the 200", "params": {}},
    "nbar_break":   {"label": "N-bar breakout on volume",    "params": {"n": [24, 48]}},
    "sweep_low":    {"label": "Prior-low sweep and reclaim", "params": {}},
    "orb":          {"label": "Opening-range breakout",      "params": {}},
}

def sig(m, s, p, i):
    b, c = m.b, m.c
    if i < 210: return False
    if s == "rsi2_dip":
        return m.r2[i] is not None and m.r2[i] < p["th"] and m.e50[i] > m.e200[i] and c[i] > m.e200[i]
    if s == "vwap_reclaim":
        return c[i] > m.vwap[i] and all(c[j] < m.vwap[j] for j in range(i - p["k"], i)) and m.e50[i] > m.e200[i]
    if s == "ema_cross":
        return m.e9[i] > m.e21[i] and m.e9[i - 1] <= m.e21[i - 1] and c[i] > m.e200[i]
    if s == "nbar_break":
        return c[i] > max(x["h"] for x in b[i - p["n"]:i]) and b[i]["v"] > 1.5 * m.vavg[i - 1] and m.e50[i] > m.e200[i]
    if s == "sweep_low":
        pl = m.plow[i]
        return pl is not None and b[i]["l"] < pl and c[i] > pl
    if s == "orb":
        h = m.orh[i]
        return m.kind == "eq" and h is not None and c[i] > h and c[i - 1] <= h and c[i] > m.vwap[i] and b[i]["mins"] < 900
    return False

def trade(m, i, sm):
    """Enter at bar i close. Stop sm x ATR (1%-4%). Half at +5%, stop to entry, trail rest by the stop distance."""
    e = m.c[i]; dist = min(max(sm * m.atr[i], 0.01 * e), 0.04 * e)
    stop, half, hw, part, cost = e - dist, False, e, 0.0, COST[m.kind]
    last = min(m.n - 1, i + MAX_HOLD[m.kind])
    for j in range(i + 1, last + 1):
        x = m.b[j]
        if x["l"] <= stop:
            px = min(stop, x["o"]); r = (px / e - 1)
            return (part + 0.5 * r if half else r) - 2 * cost, j - i, half
        if not half and x["h"] >= e * (1 + HALF_AT):
            half, part, stop = True, 0.5 * HALF_AT, e
        hw = max(hw, x["h"])
        if half: stop = max(stop, hw - dist)
    r = m.c[last] / e - 1
    return (part + 0.5 * r if half else r) - 2 * cost, last - i, half

def stats(rs):
    if not rs: return {"n": 0}
    w = [r for r, _, _ in rs if r > 0]; l = [r for r, _, _ in rs if r <= 0]
    gp, gl = sum(w), -sum(l)
    return {"n": len(rs), "win": round(len(w) / len(rs) * 100, 1), "exp": round(sum(r for r, _, _ in rs) / len(rs) * 100, 3),
            "pf": round(gp / gl, 2) if gl > 0 else None, "half_hit": round(sum(1 for _, _, h in rs if h) / len(rs) * 100, 1),
            "bars": round(sum(k for _, k, _ in rs) / len(rs), 1)}

def combos():
    for s, d in SETUPS.items():
        keys = list(d["params"])
        vals = [d["params"][k] for k in keys] or [[]]
        import itertools
        for v in (itertools.product(*vals) if keys else [()]):
            for sm in (1.5, 3.0, 5.0):
                yield s, dict(zip(keys, v)), sm

def plain(sym, kind, s, p, sm):
    when = {"rsi2_dip": f"its 5-minute RSI(2) drops below {p.get('th')} while the 50 EMA is above the 200 EMA",
            "vwap_reclaim": f"a 5-minute candle closes back above VWAP after {p.get('k')} candles below it (uptrend only)",
            "ema_cross": "the 9 EMA crosses above the 21 EMA with price above the 200 EMA (5-minute chart)",
            "nbar_break": f"a 5-minute candle closes above the high of the last {p.get('n')} candles on 1.5x volume",
            "sweep_low": "price dips under " + ("yesterday's low" if kind == "eq" else "the 24-hour low") + " and a 5-minute candle closes back above it",
            "orb": "a 5-minute candle closes above the 9:30-10:00 high, above VWAP, before 3 PM"}[s]
    return (f"Buy {sym} when {when}. Stop {sm}x the 5-minute ATR below entry (1%-4%). "
            f"At +5% sell half and move the stop to entry; trail the rest and let it run toward +20%.")

def run(out_path):
    t0 = time.time()
    fv = finviz()
    disc = discover(fv)
    uni = [(s, "eq") for s in FOCUS_EQ + disc] + [(s, "crypto") for s in FOCUS_CR]
    def load(it):
        s, k = it
        try:
            b = bars_eq(s) if k == "eq" else bars_cr(s)
            return Mk(s, k, b) if len(b) > 1500 else None
        except Exception:
            return None
    with ThreadPoolExecutor(8) as ex:
        mks = [m for m in ex.map(load, uni) if m]
    proven, cands, fired = [], [], []
    for m in mks:
        cut = int(m.n * 0.7)
        best = None
        for s, p, sm in combos():
            if s == "orb" and m.kind != "eq": continue
            tr, te, gap = [], [], -1
            for i in range(210, m.n - 1):
                if i <= gap: continue
                if sig(m, s, p, i):
                    r = trade(m, i, sm); (tr if i < cut else te).append(r); gap = i + r[1]
            a, b_ = stats(tr), stats(te)
            ok = a["n"] >= 15 and a["exp"] > 0 and b_.get("n", 0) >= 8 and b_["exp"] > 0 and (b_["pf"] or 0) > 1.2
            score = (b_.get("exp", -9) if b_.get("n", 0) >= 8 else -9) + min(a.get("exp", -9), b_.get("exp", -9) if b_.get("n", 0) else -9)
            row = {"symbol": m.sym, "kind": m.kind, "setup": s, "label": SETUPS[s]["label"], "params": p, "stop_atr": sm,
                   "train": a, "test": b_, "proven": ok, "score": round(score, 3), "plain": plain(m.sym, m.kind, s, p, sm)}
            if best is None or (ok, score) > (best["proven"], best["score"]): best = row
            if ok:
                i = m.n - 1
                if sig(m, s, p, i):
                    e = m.c[i]; dist = min(max(sm * m.atr[i], 0.01 * e), 0.04 * e)
                    fired.append({**row, "bar_time": dt.datetime.fromtimestamp(m.b[i]["t"], ET).isoformat(timespec="minutes"),
                                  "entry": e, "stop": e - dist, "half_at": e * (1 + HALF_AT), "stop_pct": round(dist / e * 100, 2)})
        if best: (proven if best["proven"] else cands).append(best)
    proven.sort(key=lambda r: r["test"]["exp"], reverse=True)
    cands.sort(key=lambda r: r["score"], reverse=True)
    # Robinhood alerts to keep for proven setups (fire as push notifications in the Robinhood app)
    want = []
    byk = {m.sym: m for m in mks}
    for r in proven[:10]:
        m = byk[r["symbol"]]; i = m.n - 1; ac = "equity" if m.kind == "eq" else "crypto"
        if r["setup"] == "nbar_break":
            lvl = max(x["h"] for x in m.b[i - r["params"]["n"] + 1:i + 1])
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "price_above", "threshold": f"{lvl:.6g}", "why": r["label"]})
        elif r["setup"] == "orb" and m.orh[i]:
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "price_above", "threshold": f"{m.orh[i]:.6g}", "why": r["label"]})
        elif r["setup"] == "sweep_low" and m.plow[i]:
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "price_below", "threshold": f"{m.plow[i]:.6g}", "why": r["label"] + " (watch for the close back above)"})
        elif r["setup"] == "vwap_reclaim" and m.kind == "eq":
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "price_crosses_vwap", "indicator": {"interval_secs": 300}, "why": r["label"]})
        elif r["setup"] == "rsi2_dip" and m.kind == "eq":
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "rsi_below", "threshold": str(r["params"]["th"]), "indicator": {"period": 2, "interval_secs": 300}, "why": r["label"]})
        elif r["setup"] == "ema_cross" and m.kind == "eq":
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "price_crosses_ema", "indicator": {"period": 21, "interval_secs": 300}, "why": r["label"]})
        else:   # crypto price-only: alert at a 1-ATR pullback level
            want.append({"symbol": m.sym, "asset_class": ac, "condition_type": "price_below", "threshold": f"{m.c[i] - m.atr[i] * 2:.6g}", "why": r["label"] + " (price nearing the setup zone)"})
    for w in want: w["key"] = "|".join([w["symbol"], w["condition_type"], w.get("threshold", ""), json.dumps(w.get("indicator") or {}, sort_keys=True)])
    out = {"t": dt.datetime.now(ET).isoformat(timespec="seconds"), "version": VERSION, "rules": {"half_at_pct": HALF_AT * 100, "cost": COST, "train_frac": 0.7},
           "markets": [m.sym for m in mks], "discovered": disc, "finviz": fv, "secs": round(time.time() - t0, 1),
           "proven": proven, "candidates": cands[:12], "fired": fired, "alerts_wanted": want,
           "summary": f"5m engine: {len(mks)} markets, {len(proven)} proven 5m setups, {len(fired)} firing on the latest closed candle."}
    json.dump(out, open(out_path, "w"), default=str)
    print(out["summary"], f"({out['secs']}s)")
    return 0

if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else "m5_out.json"))
