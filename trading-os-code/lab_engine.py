"""Z.E.R.O Lab - the always-on paper-trading curator for Kayden's Trading OS.

Every run it:
  1. Evolves a population of trading strategies on the older 70% of each market's daily history
     (fitness = return per day in a trade, after costs, scaled by confidence and consistency).
  2. Checks each strategy on the newest 30% it never trained on (out-of-sample).
  3. Forward paper-trades the best out-of-sample "champions" with live prices, $7.50 notional each.
  4. Scores the strategies Z.E.R.O trades today ("incumbents") the same way and flags any that a
     tested alternative beats.
  5. Audits the whole setup for flaws (offline tasks, stop overshoot, fee drag, tiny samples...).

PAPER ONLY. It never touches Robinhood and never changes real-money rules; it writes proposals.
Standard library only.

  python lab.py --state state.json --open open.json --ctx ctxdir --out outdir [--gens 5]
"""
import argparse, datetime as dt, json, math, os, random, statistics, sys, time, urllib.request
from zoneinfo import ZoneInfo

VERSION = "1.4"
ET = ZoneInfo("America/New_York")
UA = {"User-Agent": "Mozilla/5.0 (ZERO-lab)"}
COST = {"crypto": 0.0095, "eq": 0.0005}          # per side: Agentic crypto fee; stock slippage allowance
MARKETS = {"QQQ": "eq", "SPY": "eq", "USO": "eq", "GLD": "eq", "NVDA": "eq", "GOOGL": "eq", "MSFT": "eq", "PLTR": "eq",
           "BTC": "crypto", "ETH": "crypto", "SOL": "crypto", "XRP": "crypto", "DOGE": "crypto", "ADA": "crypto",
           "LINK": "crypto", "AVAX": "crypto", "LTC": "crypto", "SUI": "crypto", "PEPE": "crypto", "BONK": "crypto", "WIF": "crypto"}
ZERO_UNIVERSE = {"QQQ", "SPY", "USO", "GLD", "NVDA", "GOOGL", "MSFT", "PLTR"}
POP, ELITE, IMMIGRANTS = 90, 26, 10
TRAIN_FRAC, MAX_OPEN, CHAMPS, NOTIONAL = 0.70, 30, 12, 7.50

# ------------------------------------------------------------------ data
def _get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception:
            if i == 2: raise
            time.sleep(1.5)

def bars_for(sym, kind):
    """Daily bars oldest-first incl. today's partial bar: list of dicts d,o,h,l,c."""
    if kind == "crypto":
        out, end = {}, dt.datetime.now(dt.timezone.utc)
        for _ in range(3):  # ~900 days, 300 per request
            start = end - dt.timedelta(days=299)
            rows = _get(f"https://api.exchange.coinbase.com/products/{sym}-USD/candles?granularity=86400&start={start:%Y-%m-%dT00:00:00Z}&end={end:%Y-%m-%dT23:59:59Z}")
            for r in rows:
                d = dt.datetime.fromtimestamp(r[0], dt.timezone.utc).date().isoformat()
                out[d] = {"d": d, "l": r[1], "h": r[2], "o": r[3], "c": r[4]}
            end = start - dt.timedelta(days=1)
        return [out[k] for k in sorted(out)]
    j = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=3y")["chart"]["result"][0]
    q = j["indicators"]["quote"][0]
    return [{"d": dt.datetime.fromtimestamp(t, ET).date().isoformat(), "o": o, "h": h, "l": l, "c": c}
            for t, o, h, l, c in zip(j["timestamp"], q["open"], q["high"], q["low"], q["close"]) if None not in (o, h, l, c)]

def live_price(sym, kind):
    if kind == "crypto":
        return float(_get(f"https://api.exchange.coinbase.com/products/{sym}-USD/ticker")["price"])
    return float(_get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d")["chart"]["result"][0]["meta"]["regularMarketPrice"])


# ------------------------------------------------------------------ universe discovery (v1.3)
MIN_MCAP, MIN_VOL = 2e9, 1e6          # Kayden 2026-10-16: market cap >= $2B, average daily volume >= 1M (shares; USD for crypto)
MAX_NEW_EQ, MAX_NEW_CR, KEEP_RUNS = 40, 30, 12
STABLE = {"USDT", "USDC", "USDS", "DAI", "USDE", "PYUSD", "FDUSD", "TUSD", "USDD", "USD1", "USDG"}
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

def _screen(scr, count=100):
    j = _get(f"https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?scrIds={scr}&count={count}")
    return j["finance"]["result"][0]["quotes"]
def discover():
    """Large, liquid, moving names from Yahoo screeners (market cap and volume come with them). Returns ({sym: kind}, notes)."""
    eq, cr, notes = {}, {}, []
    for scr in ("day_gainers", "day_losers", "most_actives", "growth_technology_stocks", "undervalued_growth_stocks"):
        try:
            for q in _screen(scr):
                s = q.get("symbol", "")
                if not s or any(c in s for c in ".-=^") or q.get("quoteType") not in ("EQUITY", "ETF"): continue
                if (q.get("marketCap") or 0) < MIN_MCAP or (q.get("averageDailyVolume3Month") or 0) < MIN_VOL: continue
                eq[s] = abs(q.get("regularMarketChangePercent") or 0) + (eq.get(s) or 0)
        except Exception as e:
            notes.append(f"{scr}: {type(e).__name__}")
    fv = finviz()
    for name, ts in fv.items():                     # Finviz finds (already cap > $2B, avg vol > 1M)
        for k, t in enumerate(ts): eq[t] = (eq.get(t) or 0) + 10 - min(k, 9)
    notes.append("finviz: " + ", ".join(f"{k} {len(v)}" for k, v in fv.items()))
    try:
        prods = {p["base_currency"] for p in _get("https://api.exchange.coinbase.com/products") if p.get("quote_currency") == "USD" and p.get("status") == "online"}
        for off in (0, 100):
            j = _get(f"https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?scrIds=all_cryptocurrencies_us&count=100&offset={off}")
            for q in j["finance"]["result"][0]["quotes"]:
                b = q.get("symbol", "").replace("-USD", "")
                if b in STABLE or b.startswith(("W", "ST", "CB", "AETH")) and b not in ("WIF", "WLD", "W") or any(ch.isdigit() for ch in b): continue
                if b in prods and (q.get("marketCap") or 0) >= MIN_MCAP and (q.get("averageDailyVolume3Month") or 0) >= MIN_VOL:
                    cr[b] = q["marketCap"]
    except Exception as e:
        notes.append(f"crypto: {type(e).__name__}")
    eqs = sorted(eq, key=lambda s: eq[s], reverse=True)[:MAX_NEW_EQ]
    crs = sorted(cr, key=lambda s: cr[s], reverse=True)[:MAX_NEW_CR]
    return {**{s: "eq" for s in eqs}, **{s: "crypto" for s in crs}}, notes

# ------------------------------------------------------------------ indicators (cached per market)
class M:
    def __init__(self, sym, kind, bars):
        self.sym, self.kind, self.bars = sym, kind, bars
        self.c = [b["c"] for b in bars]; self.h = [b["h"] for b in bars]; self.l = [b["l"] for b in bars]
        self.n = len(bars); self._cache = {}
        tr = [self.h[0] - self.l[0]] + [max(self.h[i] - self.l[i], abs(self.h[i] - self.c[i-1]), abs(self.l[i] - self.c[i-1])) for i in range(1, self.n)]
        a, self.atr = None, []
        for i, t in enumerate(tr):
            a = t if a is None else (a * 13 + t) / 14
            self.atr.append(a)
    def ema(self, p):
        k = ("ema", p)
        if k not in self._cache:
            al, e, out = 2 / (p + 1), None, []
            for v in self.c:
                e = v if e is None else v * al + e * (1 - al); out.append(e)
            self._cache[k] = out
        return self._cache[k]
    def rsi(self, p):
        k = ("rsi", p)
        if k not in self._cache:
            out, ag, al = [None] * self.n, 0.0, 0.0
            for i in range(1, self.n):
                ch = self.c[i] - self.c[i-1]; g, l = max(ch, 0), max(-ch, 0)
                if i <= p:
                    ag += g / p; al += l / p
                    if i == p: out[i] = 100 if al == 0 else 100 - 100 / (1 + ag / al)
                else:
                    ag = (ag * (p - 1) + g) / p; al = (al * (p - 1) + l) / p
                    out[i] = 100 if al == 0 else 100 - 100 / (1 + ag / al)
            self._cache[k] = out
        return self._cache[k]
    def band(self, p, k):
        key = ("bb", p, k)
        if key not in self._cache:
            out = [None] * self.n
            for i in range(p - 1, self.n):
                w = self.c[i - p + 1:i + 1]; m = sum(w) / p; sd = statistics.pstdev(w)
                out[i] = m - k * sd
            self._cache[key] = out
        return self._cache[key]

# ------------------------------------------------------------------ strategies
SIGS = {
    "rsi_dip":   {"label": "RSI dip",            "params": {"p": [2, 3, 5, 7, 14], "th": [5, 10, 15, 20, 25, 30, 35]}},
    "pullback":  {"label": "Uptrend pullback",   "params": {"f": [10, 20], "s": [50, 100], "th": [35, 40, 45, 50]}},
    "pdl_sweep": {"label": "Prior-day low sweep", "params": {}},
    "breakout":  {"label": "N-day breakout",     "params": {"n": [10, 20, 55]}},
    "n_down":    {"label": "Down-day streak",    "params": {"k": [2, 3, 4, 5]}},
    "bb_low":    {"label": "Lower-band stretch", "params": {"p": [10, 20], "k": [1.5, 2.0, 2.5]}},
    "ema_cross": {"label": "EMA cross up",       "params": {"f": [5, 10, 20], "s": [20, 50, 100]}},
}
FILTERS = ["none", "above200", "trend50_200"]
EXITS = {"sm": [0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0], "tm": [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0], "H": [2, 3, 5, 7, 10, 15, 20]}
MODES = ["fixed", "half_trail"]  # half_trail: sell half at +1R, stop to breakeven, trail the rest (Kayden, 2026-10-15)

def describe(g):
    p = g["params"]; s = g["sig"]
    core = {"rsi_dip": f"RSI({p.get('p')}) < {p.get('th')}", "pullback": f"EMA{p.get('f')}>EMA{p.get('s')}, RSI14 < {p.get('th')}",
            "pdl_sweep": "dip under yesterday's low, close back above", "breakout": f"close at {p.get('n')}-day high",
            "n_down": f"{p.get('k')} down closes in a row", "bb_low": f"close under {p.get('p')}-day band −{p.get('k')}σ",
            "ema_cross": f"EMA{p.get('f')} crosses above EMA{p.get('s')}"}[s]
    filt = {"none": "", "above200": ", above 200-day EMA", "trend50_200": ", 50 EMA over 200"}[g["filt"]]
    if g.get("mode") == "half_trail":
        return f"{g['market']} · {SIGS[s]['label']}: {core}{filt}; stop {g['sm']}×ATR, sell half at +1R, trail the rest {g['sm']}×ATR, max {g['H'] * 3}d"
    return f"{g['market']} · {SIGS[s]['label']}: {core}{filt}; stop {g['sm']}×ATR, target {g['tm']}×ATR, max {g['H']}d"

def plain(g):
    """One-paragraph instruction a person can follow."""
    p, s, sym = g["params"], g["sig"], g["market"]
    when = {"rsi_dip": f"its {p.get('p')}-day RSI drops below {p.get('th')}", "pullback": f"it is in an uptrend (EMA{p.get('f')} over EMA{p.get('s')}) and RSI14 dips under {p.get('th')}",
            "pdl_sweep": "it dips under yesterday's low, then closes back above it", "breakout": f"it closes at a new {p.get('n')}-day high",
            "n_down": f"it closes down {p.get('k')} days in a row", "bb_low": f"it closes {p.get('k')} std devs under its {p.get('p')}-day average",
            "ema_cross": f"its {p.get('f')}-day average crosses above its {p.get('s')}-day average"}[s]
    filt = {"none": "", "above200": " Only if it is above its 200-day average.", "trend50_200": " Only if its 50-day average is above its 200-day."}[g["filt"]]
    if g.get("mode") == "half_trail":
        out = f"Stop {g['sm']}x ATR below entry. At +1R sell half, move the stop to entry, trail the rest. Sell what is left after {g['H'] * 3} days."
    else:
        out = f"Stop {g['sm']}x ATR below entry. Sell at {g['tm']}x ATR above. Sell after {g['H']} days if neither hits."
    return f"Buy {sym} when {when}.{filt} {out}"

def gkey(g):
    return json.dumps([g["market"], g["sig"], g["params"], g["filt"], g["sm"], g["tm"], g["H"], g.get("mode", "fixed")], sort_keys=True)

def signal(g, m, i):
    s, p, c = g["sig"], g["params"], m.c
    if i < 201: return False
    if g["filt"] == "above200" and c[i] < m.ema(200)[i]: return False
    if g["filt"] == "trend50_200" and m.ema(50)[i] < m.ema(200)[i]: return False
    if s == "rsi_dip":   r = m.rsi(p["p"])[i]; return r is not None and r < p["th"]
    if s == "pullback":  r = m.rsi(14)[i]; return m.ema(p["f"])[i] > m.ema(p["s"])[i] and c[i] > m.ema(p["s"])[i] and r is not None and r < p["th"]
    if s == "pdl_sweep": return m.l[i] < m.l[i-1] and c[i] > m.l[i-1]
    if s == "breakout":  return c[i] >= max(c[i - p["n"] + 1:i + 1]) and m.ema(20)[i] > m.ema(50)[i]
    if s == "n_down":    return all(c[i-j] < c[i-j-1] for j in range(p["k"]))
    if s == "bb_low":    b = m.band(p["p"], p["k"])[i]; return b is not None and c[i] < b
    if s == "ema_cross": f, sl = m.ema(p["f"]), m.ema(p["s"]); return p["f"] < p["s"] and f[i] > sl[i] and f[i-1] <= sl[i-1]
    return False

def simulate_half(g, m, last):
    """Sell half at +1R (R = sm*ATR), stop to breakeven, trail the runner sm*ATR under the high. Max hold 3*H days."""
    cost, out, i = COST[m.kind], [], 201
    while i < last:
        if not signal(g, m, i): i += 1; continue
        e, a = m.c[i], m.atr[i]; R = g["sm"] * a; stop, t1 = e - R, e + R
        half, r1, hw, px, j = False, 0.0, e, None, i
        for j in range(i + 1, min(i + 1 + g["H"] * 3, last + 1)):
            if not half:
                if m.l[j] <= stop: px = stop; break
                if m.h[j] >= t1: half, r1, stop, hw = True, t1 / e - 1, e, max(m.h[j], t1)
                continue
            if m.l[j] <= stop: px = stop; break
            hw = max(hw, m.h[j]); stop = max(stop, hw - R)
        if px is None:
            if j - i < g["H"] * 3 and j >= last: break
            px = m.c[j]
        r2 = px / e - 1
        ret = (0.5 * r1 + 0.5 * r2 if half else r2) - 2 * cost
        out.append((i, ret, max(1, j - i), "half" if half else "stop"))
        i = j + 1
    return out

def simulate(g, m, upto=None):
    """Trades: list of (entry_idx, ret_after_costs, hold_days, how). Entry at signal-bar close, one trade at a time."""
    cost, out, i, last = COST[m.kind], [], 201, (upto if upto is not None else m.n - 1)
    if g.get("mode") == "half_trail": return simulate_half(g, m, last)
    while i < last:
        if not signal(g, m, i): i += 1; continue
        e, a = m.c[i], m.atr[i]
        stop, tgt = e - g["sm"] * a, e + g["tm"] * a
        exit_px, how, j = None, "time", i
        for j in range(i + 1, min(i + 1 + g["H"], last + 1)):
            if m.l[j] <= stop: exit_px, how = stop, "stop"; break      # both hit same bar -> stop (conservative)
            if m.h[j] >= tgt: exit_px, how = tgt, "target"; break
        if exit_px is None:
            if j - i < g["H"] and j >= last: break                     # trade still open at the end of data
            exit_px = m.c[j]
        out.append((i, exit_px / e - 1 - 2 * cost, max(1, j - i), how))
        i = j + 1
    return out

def stats(trs):
    n = len(trs)
    if not n: return {"n": 0}
    r = [t[1] for t in trs]; mean = sum(r) / n; sd = statistics.pstdev(r) if n > 1 else 0
    w = sum(1 for x in r if x > 0); gw = sum(x for x in r if x > 0); gl = -sum(x for x in r if x <= 0)
    hold = sum(t[2] for t in trs)
    aw = (gw / w * 100) if w else None
    return {"n": n, "avgwin": round(aw, 3) if aw else None, "size5": round(500 / aw) if aw else None, "win": round(w / n * 100, 1), "exp": round(mean * 100, 3), "ppd": round(sum(r) / hold * 100, 4),
            "pf": round(gw / gl, 2) if gl > 0 else None, "hold": round(hold / n, 1), "t": round(mean / (sd / math.sqrt(n)), 2) if sd > 0 and n > 1 else 0}

def evaluate(g, m):
    trs = simulate(g, m); split = int(m.n * TRAIN_FRAC)
    tr = [t for t in trs if t[0] < split]; te = [t for t in trs if t[0] >= split]
    h = len(tr) // 2
    s_tr, s_te = stats(tr), stats(te)
    a, b = stats(tr[:h]), stats(tr[h:])
    consistent = a.get("n", 0) and b.get("n", 0) and a["exp"] > 0 and b["exp"] > 0
    if s_tr["n"] < 20:
        fit = -1 + s_tr["n"] / 40
    elif s_tr["exp"] <= 0:
        fit = s_tr["exp"] / 10 - 0.1
    else:
        fit = s_tr["ppd"] * min(1.0, s_tr["t"] / 2.0) * (1.0 if consistent else 0.25)
    champ = bool(fit > 0 and s_tr["n"] >= 30 and consistent and s_te.get("n", 0) >= 10 and s_te["exp"] > 0 and (s_te.get("pf") or 0) > 1.1)
    return {"fit": round(fit, 5), "train": s_tr, "oos": s_te, "consistent": bool(consistent), "champion": champ}

# ------------------------------------------------------------------ evolution
def rnd_genome(markets, gen, rng):
    sig = rng.choice(list(SIGS)); p = {k: rng.choice(v) for k, v in SIGS[sig]["params"].items()}
    if sig == "ema_cross" and p["f"] >= p["s"]: p["f"], p["s"] = min(p["f"], p["s"]), max(p["f"], p["s"]) if p["f"] != p["s"] else 50
    cm = [x for x in markets if MARKETS[x] == "crypto"]
    pick = rng.choice(cm) if cm and rng.random() < 0.6 else rng.choice(markets)   # crypto first (Kayden, 2026-10-15)
    g = {"market": pick, "sig": sig, "params": p, "filt": rng.choice(FILTERS),
         "sm": rng.choice(EXITS["sm"]), "tm": rng.choice(EXITS["tm"]), "H": rng.choice(EXITS["H"]), "mode": rng.choice(MODES), "born": gen, "parent": None}
    g["id"] = f"g{gen}-{rng.randrange(16**6):06x}"; return g

def mutate(g, markets, gen, rng):
    c = json.loads(json.dumps(g)); c["parent"] = g["id"]; c["born"] = gen
    for _ in range(rng.choice([1, 1, 2, 3])):
        what = rng.choice(["param", "param", "exit", "exit", "filt", "market", "mode"])
        if what == "param" and SIGS[c["sig"]]["params"]:
            k = rng.choice(list(SIGS[c["sig"]]["params"])); c["params"][k] = rng.choice(SIGS[c["sig"]]["params"][k])
        elif what == "exit":
            k = rng.choice(list(EXITS)); vals = EXITS[k]; i = vals.index(c[k]) if c[k] in vals else 0
            c[k] = vals[max(0, min(len(vals) - 1, i + rng.choice([-1, 1])))]
        elif what == "filt":
            c["filt"] = rng.choice(FILTERS)
        elif what == "mode":
            c["mode"] = rng.choice(MODES)
        else:
            same = [x for x in markets if MARKETS[x] == MARKETS[c["market"]]]; c["market"] = rng.choice(same)
    if c["sig"] == "ema_cross" and c["params"]["f"] >= c["params"]["s"]: c["params"]["f"] = 5
    c["id"] = f"g{gen}-{rng.randrange(16**6):06x}"; return c

INCUMBENTS = [  # what Z.E.R.O and the board trade today, as daily-bar equivalents
    {"id": "inc-uso-trend", "market": "USO", "sig": "pullback", "params": {"f": 20, "s": 50, "th": 100}, "filt": "none", "sm": 1.0, "tm": 2.0, "H": 10, "incumbent": "USO 4h trend (daily proxy, −2%/+4%)", "pct": [0.02, 0.04]},
    {"id": "inc-gld-trend", "market": "GLD", "sig": "pullback", "params": {"f": 20, "s": 50, "th": 100}, "filt": "none", "sm": 1.0, "tm": 2.0, "H": 10, "incumbent": "GLD 4h trend (daily proxy, −2%/+4%)", "pct": [0.02, 0.04]},
    {"id": "inc-googl-pdl", "market": "GOOGL", "sig": "pdl_sweep", "params": {}, "filt": "none", "sm": 1.0, "tm": 1.0, "H": 10, "incumbent": "Board: GOOGL prior-day low sweep"},
    {"id": "inc-ada-os", "market": "ADA", "sig": "rsi_dip", "params": {"p": 14, "th": 30}, "filt": "none", "sm": 1.0, "tm": 1.0, "H": 10, "incumbent": "Board: ADA oversold bounce (paper)"},
]

def simulate_pct(g, m):
    """Incumbent trend proxy with fixed % brackets: buy when EMA20>EMA50 and close crosses back above EMA20."""
    cost, out, i = COST[m.kind], [], 201
    e20, e50 = m.ema(20), m.ema(50)
    while i < m.n - 1:
        if not (e20[i] > e50[i] and m.c[i] > e20[i] and m.c[i-1] <= e20[i-1]): i += 1; continue
        e = m.c[i]; stop, tgt = e * (1 - g["pct"][0]), e * (1 + g["pct"][1]); px, j = None, i
        for j in range(i + 1, min(i + 1 + g["H"], m.n)):
            if m.l[j] <= stop: px = stop; break
            if m.h[j] >= tgt: px = tgt; break
            if e20[j] < e50[j]: px = m.c[j]; break
        if px is None:
            if j - i < g["H"]: break
            px = m.c[j]
        out.append((i, px / e - 1 - 2 * cost, max(1, j - i), ""))
        i = j + 1
    return out

def eval_incumbent(g, m):
    if "pct" not in g: return evaluate(g, m)
    trs = simulate_pct(g, m); split = int(m.n * TRAIN_FRAC)
    return {"fit": None, "train": stats([t for t in trs if t[0] < split]), "oos": stats([t for t in trs if t[0] >= split]), "consistent": None, "champion": False}

# ------------------------------------------------------------------ forward paper trading
def now_et(): return dt.datetime.now(ET)

def forward(champs, open_trades, mk, now):
    """Update open paper trades, then open new ones for champions whose signal fired on the latest completed bar."""
    updates, opened, closed = [], [], []
    for t in open_trades:
        m = mk.get(t["symbol"])
        if not m: continue
        try: px = live_price(t["symbol"], m.kind)
        except Exception: px = None
        after = [b for b in m.bars if b["d"] > t["opened_at"][:10]]
        how, exit_px = None, None
        for b in after:
            if b["l"] <= t["stop"]: how, exit_px = "stop", t["stop"]; break
            if b["h"] >= t["target"]: how, exit_px = "target", t["target"]; break
        if how is None and px is not None:
            if px <= t["stop"]: how, exit_px = "stop", px
            elif px >= t["target"]: how, exit_px = "target", px
        done_bars = len([b for b in after if b["d"] < now.date().isoformat()]) if m.kind == "eq" else len(after) - 1
        if how is None and done_bars >= t["max_days"]: how, exit_px = "time", px if px is not None else after[-1]["c"]
        t = dict(t, last=px, updated_at=now.isoformat(timespec="seconds"))
        if how:
            ret = exit_px / t["entry"] - 1 - 2 * COST[m.kind]
            t.update(status="closed", exit=round(exit_px, 8), exit_reason=how, closed_at=now.isoformat(timespec="seconds"), ret_pct=round(ret * 100, 3), pnl=round(NOTIONAL * ret, 4))
            closed.append(t)
        updates.append(t)
    busy = {t["genome_id"] for t in open_trades if t["status"] == "open"} - {t["genome_id"] for t in closed}
    n_open = len(busy)
    for g, ev in champs:
        if n_open >= MAX_OPEN or g["id"] in busy: continue
        m = mk[g["market"]]
        today = now.date().isoformat() if m.kind == "eq" else dt.datetime.now(dt.timezone.utc).date().isoformat()
        i = m.n - 1 if m.bars[-1]["d"] < today else m.n - 2          # latest completed bar
        if i < 202 or not signal(g, m, i): continue
        sig_day = m.bars[i]["d"]
        if any(t["genome_id"] == g["id"] and t.get("signal_day") == sig_day for t in open_trades): continue
        if m.kind == "eq" and not (now.weekday() < 5 and dt.time(9, 30) <= now.time() < dt.time(16, 0)): continue
        try: px = live_price(g["market"], m.kind)
        except Exception: continue
        a = m.atr[i]
        t = {"id": f"L-{g['market']}-{now:%Y%m%dT%H%M}-{g['id'][-4:]}", "genome_id": g["id"], "desc": describe(g), "symbol": g["market"], "kind": m.kind,
             "signal_day": sig_day, "signal_close": m.c[i], "entry": px, "entry_slip_pct": round((px / m.c[i] - 1) * 100, 3),
             "stop": round(px - g["sm"] * a, 8), "target": round(px + g["tm"] * a, 8), "max_days": g["H"], "notional": NOTIONAL,
             "opened_at": now.isoformat(timespec="seconds"), "status": "open", "oos_exp": ev["oos"].get("exp"), "oos_n": ev["oos"].get("n"),
             "route_if_proven": "zero-real" if g["market"] in ZERO_UNIVERSE else ("paper (crypto fee)" if MARKETS.get(g["market"]) == "crypto" else "paper (outside Z.E.R.O universe)")}
        opened.append(t); busy.add(g["id"]); n_open += 1
    return updates, opened, closed

# ------------------------------------------------------------------ flaw audit
def audit(ctx, board, now, lab_closed_all, mk_errors):
    F = []
    def add(sev, title, evidence, fix): F.append({"sev": sev, "title": title, "evidence": evidence, "fix": fix})
    bot = ctx.get("bot") or {}
    try:
        age = (now - dt.datetime.fromisoformat(bot["updated_at"])).total_seconds() / 3600
        if age > 24: add("high", "Z.E.R.O is offline", f"Last stock check {bot['updated_at'][:16]} ({age/24:.0f} days ago); scheduled tasks look switched off.", "Turn the auto-trader and crypto monitor tasks back on.")
    except Exception: pass
    trades = [t for t in ctx.get("trades", []) if t.get("status") == "closed"]
    over = []
    for t in trades:
        try:
            risk = (t["entry"] - t["stop"]) * t["qty"]
            if risk > 0 and t["pnl"] / risk < -1.2: over.append(f"{t['symbol']} {t['pnl']/risk:.2f}R")
        except Exception: pass
    if over: add("high", "Stops overshoot on fractional shares", f"Losses beyond planned risk: {', '.join(over)}. Fractional shares can't hold resting stops; exits wait for the hourly check.", "Use whole shares where a resting stop is possible, or check open trades more often (scout).")
    logs = ctx.get("log", []); blocked = [l for l in logs if "day-trade" in (l.get("text") or "")]
    if blocked: add("med", "Entries blocked by the day-trade guard", f"{len(blocked)} checks logged entries skipped because of the same-day trade count.", "Switch the Agentic account to a cash account (no pattern-day-trader limit), or favor swing setups held overnight.")
    ct = [t for t in ctx.get("crypto_trades", []) if t.get("status") == "closed"]
    if ct:
        fees = sum(t.get("fees") or 0 for t in ct); gross = sum(t.get("pnl_gross") or 0 for t in ct)
        add("med", "Crypto fees eat the edge", f"{len(ct)} paper crypto trades: gross {gross:+.3f}, fees {fees:.3f} (0.95% each way).", "Only take crypto setups with targets well above 1.9%; the Lab tests crypto with the full fee.")
    live_n = len(trades)
    if live_n < 30: add("med", "Real-money sample is tiny", f"{live_n} closed real trades. Nothing is proven or disproven yet.", "Keep size at $7.50 until a strategy has 30+ forward trades that hold up.")
    meta = (ctx.get("edge_meta") or {})
    try:
        bage = (now - dt.datetime.fromisoformat(meta["t"])).days
        if bage > 3: add("med", "Probability board is stale", f"Last refresh {meta['t'][:10]} ({bage} days ago).", "Turn the nightly board refresh back on; the Lab re-tests markets itself meanwhile.")
    except Exception: pass
    for row in board:
        if row.get("beaten_by"): add("med", f"{row['incumbent']} is beaten by a tested alternative", f"Incumbent OOS {row['oos'].get('exp')}%/trade (n={row['oos'].get('n')}) vs {row['beaten_by']['desc']} at {row['beaten_by']['oos_exp']}%/trade (n={row['beaten_by']['oos_n']}).", "Forward paper-test the alternative; propose a swap only after it holds up live on paper.")
    slips = [t.get("entry_slip_pct") for t in lab_closed_all if t.get("entry_slip_pct") is not None]
    if len(slips) >= 5:
        avg = sum(slips) / len(slips)
        if abs(avg) > 0.3: add("low", "Entry slippage vs signal price", f"Paper entries average {avg:+.2f}% from the signal close (n={len(slips)}).", "Pre-stage limit orders at the signal level instead of buying at the next check.")
    if mk_errors: add("low", "Data gaps", f"Markets with data errors this run: {', '.join(mk_errors)}.", "Retries next run; persistent gaps need another data source.")
    order = {"high": 0, "med": 1, "low": 2}
    return sorted(F, key=lambda f: order[f["sev"]])

# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--state"); ap.add_argument("--open"); ap.add_argument("--ctx"); ap.add_argument("--out", required=True)
    ap.add_argument("--gens", type=int, default=5); ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    t0, now = time.time(), now_et()
    rng = random.Random(a.seed if a.seed is not None else int(t0))
    load = lambda p, d: json.load(open(p)) if p and os.path.exists(p) else d
    state = load(a.state, {}) or {}
    open_trades = load(a.open, []) or []
    ctx = {}
    if a.ctx and os.path.isdir(a.ctx):
        for f in os.listdir(a.ctx):
            if f.endswith(".json"): ctx[f[:-5]] = json.load(open(os.path.join(a.ctx, f)))
    os.makedirs(a.out, exist_ok=True)

    # universe = core list + names discovered now + names discovered in the last KEEP_RUNS runs
    core = dict(MARKETS)
    found, dnotes = discover()
    seen_u = {s: v for s, v in (state.get("universe") or {}).items() if isinstance(v, dict) and v.get("runs_left", 0) > 0}
    for s, k in found.items(): seen_u[s] = {"kind": k, "runs_left": KEEP_RUNS}
    for s in list(seen_u):
        if s not in found: seen_u[s]["runs_left"] -= 1
    seen_u = {s: v for s, v in seen_u.items() if v["runs_left"] > 0 and s not in core}
    for s, v in seen_u.items(): MARKETS[s] = v["kind"]
    # v1.5 fix (2026-10-21): a symbol with an open paper trade is always loaded, even after it leaves the
    # discovered universe, so its stop/target/time exit keep being checked (GM/NU bug).
    held = {t["symbol"]: t.get("kind") or "eq" for t in open_trades if t.get("status") == "open"}
    for s, k in held.items(): MARKETS.setdefault(s, k)
    from concurrent.futures import ThreadPoolExecutor
    def load_one(item):
        s, k = item
        try:
            b = bars_for(s, k)
            if len(b) <= 260: return s, None
            m = M(s, k, b)
            if s not in core and s not in held:    # high-movement gate for discovered names (never drop a held symbol)
                a = sum(m.atr[-20:]) / 20 / (sum(m.c[-20:]) / 20)
                if a < (0.03 if k == "crypto" else 0.02): return s, "calm"
            return s, m
        except Exception:
            return s, None
    mk, errors, calm = {}, [], []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for s, m in ex.map(load_one, list(MARKETS.items())):
            if m == "calm": calm.append(s)
            elif m is None: errors.append(s)
            else: mk[s] = m
    for s in calm: seen_u.pop(s, None)
    discovered_live = sorted(s for s in mk if s not in core and s not in held)
    if len(mk) < 5:
        json.dump({"error": f"data feed down ({len(errors)} markets failed)"}, open(os.path.join(a.out, "error.json"), "w")); print("DATA FEED DOWN"); return 2
    markets = sorted(mk)

    gen = int(state.get("generation", 0)); pop = [g for g in state.get("population", []) if g.get("market") in mk]
    seen = set(); pop = [g for g in pop if not (gkey(g) in seen or seen.add(gkey(g)))]
    while len(pop) < POP: pop.append(rnd_genome(markets, gen, rng))
    history = state.get("history", [])
    evals = {}
    idle = not open_trades                     # Kayden 2026-10-16: no paper trades running -> spend the run improving setups
    for _ in range(max(1, a.gens) * (3 if idle else 1)):
        gen += 1
        for g in pop:
            if g["id"] not in evals: evals[g["id"]] = evaluate(g, mk[g["market"]])
        pop.sort(key=lambda g: evals[g["id"]]["fit"], reverse=True)
        best = pop[0]; history.append({"gen": gen, "t": now.isoformat(timespec="seconds"), "best": evals[best["id"]]["fit"],
                                       "champs": sum(1 for g in pop if evals[g["id"]]["champion"]), "best_id": best["id"]})
        elite, per = [], {}                      # diversity: at most 3 elites per market+setup
        for g in pop:
            k = (g["market"], g["sig"])
            if per.get(k, 0) < 3: elite.append(g); per[k] = per.get(k, 0) + 1
            if len(elite) >= ELITE: break
        keys = {gkey(g) for g in elite}; children = []
        while len(children) < POP - ELITE - IMMIGRANTS:
            c = mutate(rng.choice(elite[:max(6, ELITE // 2)] if rng.random() < .6 else elite), markets, gen, rng)
            if gkey(c) not in keys: keys.add(gkey(c)); children.append(c)
        imm = [rnd_genome(markets, gen, rng) for _ in range(IMMIGRANTS)]
        pop = elite + children + imm
    for g in pop:
        if g["id"] not in evals: evals[g["id"]] = evaluate(g, mk[g["market"]])
    pop.sort(key=lambda g: evals[g["id"]]["fit"], reverse=True)

    # hall of fame: best champions ever seen (kept across runs, re-scored on fresh data)
    hof = {g["id"]: g for g in state.get("hall", []) if g.get("market") in mk}
    for g in pop:
        if evals[g["id"]]["champion"]: hof[g["id"]] = g
    scored = []
    for g in hof.values():
        ev = evals.get(g["id"]) or evaluate(g, mk[g["market"]]); evals[g["id"]] = ev
        if ev["champion"]: scored.append((g, ev))
    scored.sort(key=lambda x: (MARKETS[x[0]["market"]] == "crypto", x[1]["oos"]["ppd"]), reverse=True)   # crypto champions trade first
    # learn from experience: a champion whose live paper record turns negative after 5+ trades is retired
    exp0 = {}
    for t in (ctx.get("lab_closed") or []):
        r = exp0.setdefault(t["genome_id"], [0, 0.0]); r[0] += 1; r[1] += t["ret_pct"]
    retired = {gid for gid, (n, sm) in exp0.items() if n >= 5 and sm / n < 0}
    scored = [x for x in scored if x[0]["id"] not in retired]
    uniq, used = [], set()
    for g, ev in scored:
        k = (g["market"], g["sig"])
        if k in used: continue
        used.add(k); uniq.append((g, ev))
    champs = uniq[:CHAMPS]
    hall = [g for g, _ in scored[:40]]

    # incumbents
    board = []
    for g in INCUMBENTS:
        if g["market"] not in mk: continue
        ev = eval_incumbent(g, mk[g["market"]])
        rival = next(((c, e) for c, e in champs if c["market"] == g["market"] and e["oos"]["exp"] > (ev["oos"].get("exp") or -99) + 0.25), None)
        board.append({"id": g["id"], "incumbent": g["incumbent"], "market": g["market"], "train": ev["train"], "oos": ev["oos"],
                      "beaten_by": {"id": rival[0]["id"], "desc": describe(rival[0]), "oos_exp": rival[1]["oos"]["exp"], "oos_n": rival[1]["oos"]["n"]} if rival else None})

    updates, opened, closed = forward(champs, [t for t in open_trades if t.get("status") == "open"], mk, now)
    lab_closed_all = (ctx.get("lab_closed") or []) + closed
    flaws = audit(ctx, board, now, lab_closed_all, errors)

    # forward record per genome -> proposals
    rec = {}
    for t in lab_closed_all:
        r = rec.setdefault(t["genome_id"], {"n": 0, "w": 0, "sum": 0.0, "desc": t["desc"], "symbol": t["symbol"]})
        r["n"] += 1; r["w"] += 1 if t["ret_pct"] > 0 else 0; r["sum"] += t["ret_pct"]
    proposals = []
    for gid, r in rec.items():
        if r["n"] >= 10 and r["sum"] / r["n"] > 0:
            proposals.append({"genome_id": gid, "desc": r["desc"], "forward_n": r["n"], "forward_win": round(r["w"] / r["n"] * 100, 1),
                              "forward_exp": round(r["sum"] / r["n"], 3), "action": "Adopt into Z.E.R.O at $7.50" if r["symbol"] in ZERO_UNIVERSE else ("Keep on paper (crypto fee) or trade by hand" if MARKETS.get(r["symbol"]) == "crypto" else "Keep on paper: new-universe stock, needs Kayden OK to add to Z.E.R.O"),
                              "needs": "Kayden's OK (real-money rule change)"})
    fwd = {"n": len(lab_closed_all), "win": round(sum(1 for t in lab_closed_all if t["ret_pct"] > 0) / len(lab_closed_all) * 100, 1) if lab_closed_all else None,
           "net": round(sum(t["pnl"] for t in lab_closed_all), 4), "exp": round(sum(t["ret_pct"] for t in lab_closed_all) / len(lab_closed_all), 3) if lab_closed_all else None}

    leader = []
    for g, ev in champs:
        leader.append({"id": g["id"], "desc": describe(g), "market": g["market"], "kind": MARKETS[g["market"]], "sig": g["sig"], "born": g["born"], "plain": plain(g),
                       "train": ev["train"], "oos": ev["oos"], "fwd": rec.get(g["id"]), "status": "champion"})
    shown = {(r["market"], r["sig"]) for r in leader}
    for g in pop[:60]:
        if any(g["id"] == r["id"] for r in leader) or (g["market"], g["sig"]) in shown: continue
        shown.add((g["market"], g["sig"]))
        ev = evals[g["id"]]
        leader.append({"id": g["id"], "desc": describe(g), "market": g["market"], "kind": MARKETS[g["market"]], "sig": g["sig"], "born": g["born"], "plain": plain(g),
                       "train": ev["train"], "oos": ev["oos"], "fwd": rec.get(g["id"]), "status": "candidate" if ev["fit"] > 0 else "rejected"})
        if len(leader) >= 30: break

    runs = int(state.get("runs", 0)) + 1
    best_ch = champs[0] if champs else None
    mood = "promoting" if proposals else "trading" if opened or any(u["status"] == "open" for u in updates) else "researching"
    summary = (f"Gen {gen}: {len(champs)} champions pass out-of-sample; {len([u for u in updates if u['status']=='open']) + len(opened)} paper trades open"
               f" ({len(opened)} new, {len(closed)} closed); forward record {fwd['n']} trades" + (f", {fwd['exp']:+.2f}%/trade" if fwd['exp'] is not None else "") + f"; {len(flaws)} flaws flagged; testing {len(mk)} markets ({len(discovered_live)} discovered: mcap>=$2B, vol>=1M).")
    out_state = {"t": now.isoformat(timespec="seconds"), "version": VERSION, "generation": gen, "runs": runs, "population": pop, "hall": hall,
                 "history": history[-400:], "markets": markets, "universe": seen_u, "discovered": discovered_live, "calm": calm, "discovery_notes": dnotes, "errors": errors, "secs": round(time.time() - t0, 1), "mood": mood, "idle_boost": idle, "summary": summary,
                 "best": {"desc": describe(best_ch[0]), "oos": best_ch[1]["oos"], "train": best_ch[1]["train"]} if best_ch else None,
                 "forward": fwd, "retired": sorted(retired), "rules": {"train_frac": TRAIN_FRAC, "notional": NOTIONAL, "max_open": MAX_OPEN, "cost": COST}}
    dump = lambda n, o: json.dump(o, open(os.path.join(a.out, n), "w"), default=str)
    dump("state.json", out_state)
    dump("leaderboard.json", {"t": out_state["t"], "generation": gen, "rows": leader, "incumbents": board})
    dump("flaws.json", {"t": out_state["t"], "items": flaws})
    dump("proposals.json", {"t": out_state["t"], "items": proposals, "forward": fwd})
    tdir = os.path.join(a.out, "trades"); os.makedirs(tdir, exist_ok=True)
    for t in updates + opened: json.dump(t, open(os.path.join(tdir, t["id"] + ".json"), "w"), default=str)
    events = [f"Lab paper BUY {t['symbol']} at {t['entry']:.6g} (stop {t['stop']:.6g}, target {t['target']:.6g}): {t['desc'].split(': ',1)[-1]}" for t in opened]
    events += [f"Lab paper {t['symbol']} closed: {t['exit_reason']}, {t['ret_pct']:+.2f}% after costs" for t in closed]
    events += [f"Lab proposal: {p['desc']} - {p['forward_n']} forward trades, {p['forward_exp']:+.2f}%/trade. Needs your OK." for p in proposals]
    dump("events.json", events)
    print(summary); print(f"{len(mk)} markets, {time.time()-t0:.0f}s"); return 0

if __name__ == "__main__":
    sys.exit(main())
