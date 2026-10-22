import json, subprocess, sys, math, datetime as dt
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York"); UTC = dt.timezone.utc
MEME = ["PEPE", "BONK", "WIF", "PENGU"]  # added 2026-10-04 (Kayden: prioritize crypto); entries gated by the daily coin check
COINS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "LINK", "AVAX", "LTC", "SUI"] + MEME
TIER1 = {"SOL", "XRP", "ADA", "LINK", "AVAX", "DOGE", "LTC", "SUI", "PEPE", "BONK", "WIF", "PENGU"}
FEE = 0.0095  # Robinhood Agentic crypto fee, each way

def get(url):
    out = subprocess.run(["curl", "-s", "-m", "20", "-A", "Mozilla/5.0", url], capture_output=True, text=True).stdout
    return json.loads(out)

def candles(sym, gran):
    raw = get(f"https://api.exchange.coinbase.com/products/{sym}-USD/candles?granularity={gran}")
    if not isinstance(raw, list): raise RuntimeError(f"{sym} {gran}: {str(raw)[:120]}")
    rows = [dict(t=r[0], l=float(r[1]), h=float(r[2]), o=float(r[3]), c=float(r[4]), v=float(r[5])) for r in raw]
    rows.sort(key=lambda x: x["t"]); return rows

def ema(xs, n):
    if len(xs) < n: return None
    k = 2 / (n + 1); e = sum(xs[:n]) / n
    for x in xs[n:]: e = x * k + e * (1 - k)
    return e

def rsi(xs, n=14):
    if len(xs) < n + 1: return None
    g = [max(xs[i] - xs[i-1], 0) for i in range(1, len(xs))]; l = [max(xs[i-1] - xs[i], 0) for i in range(1, len(xs))]
    ag = sum(g[:n]) / n; al = sum(l[:n]) / n
    for i in range(n, len(g)): ag = (ag * (n - 1) + g[i]) / n; al = (al * (n - 1) + l[i]) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)

def atr(rows, n=14):
    trs = [max(r["h"] - r["l"], abs(r["h"] - p["c"]), abs(r["l"] - p["c"])) for p, r in zip(rows, rows[1:])]
    return sum(trs[-n:]) / min(n, len(trs)) if trs else None

def agg(rows, sec):
    out = []
    for r in rows:
        b = r["t"] - r["t"] % sec
        if out and out[-1]["t"] == b:
            o = out[-1]; o["h"] = max(o["h"], r["h"]); o["l"] = min(o["l"], r["l"]); o["c"] = r["c"]; o["v"] += r["v"]
        else: out.append(dict(r, t=b))
    return out

def iso(t): return dt.datetime.fromtimestamp(t, ET).isoformat(timespec="minutes")
def hm(t): return dt.datetime.fromtimestamp(t, ET).strftime("%-I:%M %p ET")
def rp(x): return float(f"{x:.6g}")
def fx(x): return f"{x:,.2f}" if x >= 100 else f"{x:.4f}" if x >= 1 else f"{x:.6g}" if x >= 0.001 else f"{x:.10f}".rstrip("0")

def swings(rows, k=3):
    hi, lo = [], []
    for i in range(k, len(rows) - k):
        w = rows[i-k:i+k+1]
        if rows[i]["h"] == max(x["h"] for x in w): hi.append((rows[i]["t"], rows[i]["h"], i))
        if rows[i]["l"] == min(x["l"] for x in w): lo.append((rows[i]["t"], rows[i]["l"], i))
    return hi, lo

def scan(sym, now):
    m15 = [r for r in candles(sym, 900) if r["t"] + 900 <= now]
    h1 = [r for r in candles(sym, 3600) if r["t"] + 3600 <= now]
    d1 = candles(sym, 86400)
    price = m15[-1]["c"]
    h4 = [r for r in agg(h1, 14400) if r["t"] + 14400 <= now]
    c4 = [r["c"] for r in h4]; e20, e50 = ema(c4, 20), ema(c4, 50)
    trend = "up" if e20 and e50 and e20 > e50 and price > e20 else "down" if e20 and e50 and e20 < e50 and price < e20 else "mixed"
    r1, r4 = rsi([r["c"] for r in h1]), rsi(c4)
    datr = atr(d1[:-1]) if len(d1) > 15 else None
    ago = [r for r in h1 if r["t"] <= now - 86400]
    chg24 = (price / ago[-1]["c"] - 1) * 100 if ago else None
    vol24 = sum(r["v"] * r["c"] for r in h1[-24:]) / 1e6
    prev = d1[-2] if len(d1) >= 2 else None
    # resting liquidity: PDH/PDL + untaken 1h swing points from the last 72h
    levels = []
    if prev: levels += [("PDH", prev["h"], "buy", prev["t"] + 86400), ("PDL", prev["l"], "sell", prev["t"] + 86400)]
    recent = h1[-72:]; hi, lo = swings(recent)
    for t, v, i in hi: levels.append(("1h swing high", v, "buy", t + 4 * 3600))
    for t, v, i in lo: levels.append(("1h swing low", v, "sell", t + 4 * 3600))
    # equal highs / lows: two swing points within 0.1%, at least 6 hours apart
    def eq(pts):
        out = []
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                if abs(pts[a][1] - pts[b][1]) / pts[a][1] < 0.001 and abs(pts[a][0] - pts[b][0]) >= 6 * 3600: out.append((pts[a][1] + pts[b][1]) / 2)
        return out
    eqh, eql = eq(hi), eq(lo)
    def untaken(lv, side, vf):
        later = [x for x in h1 if x["t"] >= vf]
        return all(x["h"] <= lv for x in later) if side == "buy" else all(x["l"] >= lv for x in later)
    # sweeps in the last 24h on completed 1h candles: wick through a level, close back inside
    sweeps = []
    for name, lv, side, valid_from in levels:
        for j, r in enumerate(h1):
            if r["t"] < valid_from or r["t"] < now - 86400: continue
            if side == "sell" and r["l"] < lv and r["c"] > lv and all(x["l"] >= lv for x in h1 if valid_from <= x["t"] < r["t"]):
                sweeps.append(dict(kind="bull", level=name, price=rp(lv), wick=rp(r["l"]), t=r["t"] + 3600, eq=any(abs(lv - e) / e < 0.0015 for e in eql))); break
            if side == "buy" and r["h"] > lv and r["c"] < lv and all(x["h"] <= lv for x in h1 if valid_from <= x["t"] < r["t"]):
                sweeps.append(dict(kind="bear", level=name, price=rp(lv), wick=rp(r["h"]), t=r["t"] + 3600, eq=any(abs(lv - e) / e < 0.0015 for e in eqh))); break
    # keep the strongest sweep per side (PDH/PDL beat swings; latest first)
    rank = {"PDL": 2, "PDH": 2}
    sweeps.sort(key=lambda s: (rank.get(s["level"], 1) + (1 if s["eq"] else 0), s["t"]), reverse=True)
    seen, keep = set(), []
    for s in sweeps:
        if s["kind"] in seen: continue
        seen.add(s["kind"]); keep.append(s)
    # long setup: bull sweep -> 15m bullish FVG (displacement) within 2h, still unfilled
    setup = None
    for s in keep:
        if s["kind"] != "bull": continue
        after = [r for r in m15 if r["t"] >= s["t"] - 3600]
        for i in range(2, min(len(after), 10)):
            a, b, c = after[i-2], after[i-1], after[i]
            if c["l"] > a["h"] and b["c"] > b["o"]:
                gap_lo, gap_hi = a["h"], c["l"]
                if any(x["c"] < gap_lo for x in after[i+1:]): break
                stop = s["wick"] * 0.998
                entry = min(price, gap_hi)
                above = sorted(v for n, v, sd, vf in levels if sd == "buy" and v > entry * 1.002 and untaken(v, sd, vf))
                target = above[0] if above else None
                if target is None or entry <= stop: break
                risk, reward = (entry - stop) / entry, (target - entry) / entry
                net_r = (reward - 2 * FEE) / (risk + 2 * FEE)
                setup = dict(entry=rp(entry), stop=rp(stop), target=rp(target), gap=[rp(gap_lo), rp(gap_hi)], gross_rr=round(reward / risk, 2),
                             net_rr=round(net_r, 2), reward_pct=round(reward * 100, 2), risk_pct=round(risk * 100, 2), in_gap=gap_lo <= price <= gap_hi * 1.003,
                             after_fees=net_r >= 1.5 and reward - 2 * FEE >= 0.02, sweep=s["level"], formed=c["t"])
                break
        if setup: break
    score = 0.0
    if setup: score += 4 if setup["after_fees"] else 2
    if any(s["kind"] == "bull" for s in keep): score += 1
    if trend == "up": score += 1.5
    if (r1 and r1 < 30) or (r4 and r4 < 30): score += 1.5 if sym in TIER1 else 1
    if datr: score += min(2, datr / price * 100 / 2)
    score += min(1.5, math.log10(max(vol24, 1)) / 2)
    events = []
    for s in keep:
        what = "swept" + (" equal" if s["eq"] else "") + f" the {s['level']} {fx(s['price'])}"
        if s["kind"] == "bull": events.append(dict(key=f"{sym}|bull|{s['level']}|{s['t']}", t=s["t"], text=f"{sym} {what} (wick {fx(s['wick'])}) and closed back above: sell-side liquidity taken."))
        else: events.append(dict(key=f"{sym}|bear|{s['level']}|{s['t']}", t=s["t"], text=f"{sym} {what} (wick {fx(s['wick'])}) and closed back below: buy-side liquidity taken."))
    if setup:
        events.append(dict(key=f"{sym}|setup|{setup['formed']}", t=setup["formed"] + 900, setup=True, text=f"{sym} sweep + FVG long: entry {fx(setup['entry'])}, stop {fx(setup['stop'])}, target {fx(setup['target'])} ({setup['gross_rr']}R, {setup['net_rr']}R after fees){'' if setup['after_fees'] else ', fees too heavy, paper only'}."))
    for lab, v in (("1h", r1), ("4h", r4)):
        if v is not None and v < 30 and sym in TIER1:
            day = dt.datetime.fromtimestamp(now, ET).strftime("%Y-%m-%d")
            events.append(dict(key=f"{sym}|rsi{lab}|{day}", t=now, text=f"{sym} {lab} RSI {v:.0f}: oversold, matches your Tier-1 dip rule."))
    if chg24 is not None and abs(chg24) >= 5:
        events.append(dict(key=f"{sym}|move|{dt.datetime.fromtimestamp(now, ET):%Y-%m-%d}|{'up' if chg24 > 0 else 'down'}", t=now, text=f"{sym} {chg24:+.1f}% in 24h."))
    below = sorted([(n, v) for n, v, sd, vf in levels if sd == "sell" and v < price and untaken(v, sd, vf)], key=lambda x: -x[1])[:2]
    above = sorted([(n, v) for n, v, sd, vf in levels if sd == "buy" and v > price and untaken(v, sd, vf)], key=lambda x: x[1])[:2]
    note = f"4h trend {trend}; RSI 1h {r1:.0f} / 4h {r4:.0f}" if r1 and r4 else f"4h trend {trend}"
    if above: note += f"; buy-side liquidity {fx(above[0][1])} ({above[0][0]})"
    if below: note += f"; sell-side {fx(below[0][1])} ({below[0][0]})"
    return dict(symbol=sym, price=rp(price), chg24=None if chg24 is None else round(chg24, 2), trend4h=trend, ema20_4h=e20 and rp(e20), ema50_4h=e50 and rp(e50),
                rsi1h=r1 and round(r1, 1), rsi4h=r4 and round(r4, 1), atr_pct=datr and round(datr / price * 100, 2), vol24_musd=round(vol24, 1),
                pdh=prev and rp(prev["h"]), pdl=prev and rp(prev["l"]), liq_above=[dict(name=n, price=rp(v)) for n, v in above], liq_below=[dict(name=n, price=rp(v)) for n, v in below],
                sweeps=[dict(s, t=iso(s["t"])) for s in keep], setup=setup and dict(setup, formed=iso(setup["formed"])), score=round(score, 2), note=note,
                closes=[rp(r["c"]) for r in h1[-48:]], meme=sym in MEME, day_low=rp(min([r["l"] for r in m15 if r["t"] >= now - now % 86400] or [price])), events=[dict(e, t=iso(e["t"]), time=hm(e["t"])) for e in events], _m15=m15)

def load_board(path):
    """Crypto rows of the Probability board with 'decent' odds. path = a JSON list, or a folder of edge docs (ArtifactData out_dir)."""
    import os, glob
    if not os.path.isdir(path): return json.load(open(path))
    out = []
    for f in glob.glob(os.path.join(path, "**", "*.json"), recursive=True):
        m = json.load(open(f))
        if "signals" not in m and isinstance(m.get("data"), dict): m = m["data"]
        if m.get("kind") != "crypto": continue
        for s in m.get("signals", []):
            if s.get("decent") and s.get("trigger_level") is not None and s["id"] in ("oversold", "pullback", "pdl_sweep", "breakout"):
                out.append(dict(symbol=m["symbol"], signal=s["id"], label=s.get("label"), trigger_level=s["trigger_level"], trigger_dir=s.get("trigger_dir"), atr=m["atr"], win=s["win"], n=s["n"]))
    return out

def board_hits(board, data):
    """Kayden's Probability board, crypto rows with 'decent' odds, checked in real time (2026-10-04)."""
    out = []
    for b in board:
        d = data.get(b["symbol"]); lvl = b.get("trigger_level")
        if not d or lvl is None: continue
        px = d["price"]; sid = b["signal"]
        if sid == "pdl_sweep": hit = d["day_low"] < lvl < px
        elif b.get("trigger_dir") == "above": hit = px >= lvl
        else: hit = px <= lvl
        if hit:
            a = b["atr"]; out.append(dict(symbol=b["symbol"], signal=sid, label=b.get("label"), trigger_level=lvl, price=px, stop=rp(px - a), target=rp(px + a),
                                          win=b.get("win"), n=b.get("n"), meme=d["meme"], net_rr=round((a - 2 * FEE * px) / (a + 2 * FEE * px), 2)))
    return out

def paper_exits(open_trades, data):
    out = []; time_now = dt.datetime.now(UTC).timestamp()
    for tr in open_trades:
        d = data.get(tr["symbol"]);
        if not d: continue
        t0 = dt.datetime.fromisoformat(tr["opened_at"]).timestamp()
        if tr.get("max_days") and time_now - t0 >= tr["max_days"] * 86400:
            r = d["_m15"][-1]; px = r["c"]; gross = (px - tr["entry"]) * tr["qty"]; fees = (px + tr["entry"]) * tr["qty"] * FEE
            hit = next((x for x in d["_m15"] if x["t"] >= t0 and (x["l"] <= tr["stop"] or x["h"] >= tr["target"])), None)
            if hit is None:
                out.append(dict(id=tr["id"], symbol=tr["symbol"], exit=rp(px), exit_reason=f"{tr['max_days']}-day time exit", closed_at=iso(r["t"] + 900), time=hm(r["t"] + 900), pnl_gross=round(gross, 4), fees=round(fees, 4), pnl=round(gross - fees, 4)))
                continue
        for r in d["_m15"]:
            if r["t"] < t0: continue
            hit = "stop hit" if r["l"] <= tr["stop"] else "target hit" if r["h"] >= tr["target"] else None
            if hit:
                px = tr["stop"] if hit == "stop hit" else tr["target"]
                gross = (px - tr["entry"]) * tr["qty"]; fees = (px + tr["entry"]) * tr["qty"] * FEE
                out.append(dict(id=tr["id"], symbol=tr["symbol"], exit=px, exit_reason=hit, closed_at=iso(r["t"] + 900), time=hm(r["t"] + 900), pnl_gross=round(gross, 4), fees=round(fees, 4), pnl=round(gross - fees, 4)))
                break
    return out

if __name__ == "__main__":
    now = int(dt.datetime.now(UTC).timestamp())
    open_trades = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else []
    board = load_board(sys.argv[2]) if len(sys.argv) > 2 else []
    data, errors = {}, []
    for s in COINS:
        try: data[s] = scan(s, now)
        except Exception as e: errors.append(f"{s}: {e}")
    exits = paper_exits(open_trades, data); hits = board_hits(board, data)
    coins = sorted(data.values(), key=lambda d: -d["score"])
    for i, d in enumerate(coins): d["rank"] = i + 1; d.pop("_m15", None)
    print(json.dumps(dict(checked_at=dt.datetime.now(ET).isoformat(timespec="seconds"), checked_time=dt.datetime.now(ET).strftime("%-I:%M %p ET"), fee_each_way=FEE, coins=coins, paper_exits=exits, board_hits=hits, errors=errors), indent=1))
