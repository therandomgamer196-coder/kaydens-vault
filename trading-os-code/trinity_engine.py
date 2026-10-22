"""Trinity model paper engine on 1-minute candles (NQ and ES, each using the other for SMT).
Steps (from Kayden's saved trinity-model skill):
 1 Bias: last overnight (6 PM-9:30 AM ET) 1h candle that CLOSES through an unfilled 1h FVG -> bias in the close's direction.
 2 Tag: 9:30-12:00, price trades into an unfilled 1h FVG in the bias direction; no 1m body closes past the gap midpoint.
 3 SMT: within +/-5 min of the tag, one index makes a new session extreme and the other doesn't.
 4 CISD: a 1m FVG against the bias forms around the tag, then a 1m candle closes back through it -> entry at that close.
    Stop = protected extreme (tag low/high to entry) +/- 1 tick; targets 1R/2R/3R; flat at 3:59 PM. One trade per symbol per day.
Usage: python3 trinity1m.py backtest            (last ~29 days)
       python3 trinity1m.py today out.json       (today's session, for the daily paper run)"""
import json, sys, time, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York"); TICK = 0.25
PV = {"NQ": 2.0, "ES": 5.0}  # $ per point for MNQ and MES (micro contracts)

def y(sym, iv, p1=None, p2=None, rng=None):
    q = f"interval={iv}&includePrePost=true&" + (f"range={rng}" if rng else f"period1={p1}&period2={p2}")
    for i in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?{q}", headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())["chart"]["result"][0]
            break
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    else: raise RuntimeError(f"{sym} {iv}: {err}")
    qq = r["indicators"]["quote"][0]; out = []
    for i, t in enumerate(r.get("timestamp") or []):
        o, h, l, c = qq["open"][i], qq["high"][i], qq["low"][i], qq["close"][i]
        if None in (o, h, l, c): continue
        out.append(dict(t=dt.datetime.fromtimestamp(t, ET), o=o, h=h, l=l, c=c))
    return out

def one_min(sym, days):
    now = int(time.time()); start = now - days * 86400; out = {}
    while start < now:
        end = min(start + 7 * 86400, now)
        for b in y(sym, "1m", start, end): out[b["t"]] = b
        start = end; time.sleep(0.5)
    return [out[k] for k in sorted(out)]

def htf_gaps(h1, upto):
    bars = [b for b in h1 if b["t"] + dt.timedelta(hours=1) <= upto]; gs = []
    for i in range(2, len(bars)):
        A, B, C = bars[i-2], bars[i-1], bars[i]
        if C["l"] > A["h"]: gs.append(dict(dir="bull", bot=A["h"], top=C["l"], i=i, formed=C["t"]))
        if C["h"] < A["l"]: gs.append(dict(dir="bear", bot=C["h"], top=A["l"], i=i, formed=C["t"]))
    for g in gs:
        g["inv"] = None
        for b in bars[g["i"]+1:]:
            if (g["dir"] == "bear" and b["c"] > g["top"]) or (g["dir"] == "bull" and b["c"] < g["bot"]):
                g["inv"] = b["t"] + dt.timedelta(hours=1); break
    return gs

def run_day(d, sym, partner, m1, p1m, h1):
    open_t = dt.datetime.combine(d, dt.time(9, 30), ET); on_start = open_t - dt.timedelta(hours=15, minutes=30)
    if d.weekday() == 0: on_start -= dt.timedelta(days=2)
    rth = [b for b in m1 if open_t <= b["t"] < open_t + dt.timedelta(hours=6, minutes=29)]
    pm = {b["t"]: b for b in p1m}
    if len(rth) < 200: return dict(status="no data")
    gs = htf_gaps(h1, open_t)
    inv = [g for g in gs if g["inv"] and on_start <= g["inv"] <= open_t]
    if not inv: return dict(status="no overnight inversion, no bias")
    last = max(inv, key=lambda g: g["inv"]); bias = "long" if last["dir"] == "bear" else "short"
    info = dict(bias=bias, bias_gap=[round(last["bot"], 2), round(last["top"], 2)], bias_time=last["inv"].strftime("%m-%d %I:%M %p"))
    px = rth[0]["o"]
    zones = [dict(g) for g in gs if g["inv"] is None and g["dir"] == ("bull" if bias == "long" else "bear") and abs((g["top"] + g["bot"]) / 2 / px - 1) < 0.03]
    if not zones: return dict(status="bias but no unfilled 1h gap in range", **info)
    for z in zones: z["mid"] = (z["top"] + z["bot"]) / 2; z["dead"] = False
    sess_lo = sess_hi = None; p_lo = p_hi = None
    for k, b in enumerate(rth):
        if b["t"].time() > dt.time(12, 0): break
        pb = pm.get(b["t"])
        for z in zones:  # a body closing past the midpoint kills the zone
            if z["dead"]: continue
            if (bias == "long" and min(b["o"], b["c"]) < z["mid"]) or (bias == "short" and max(b["o"], b["c"]) > z["mid"]):
                if b["l"] <= z["top"] and b["h"] >= z["bot"]: z["dead"] = True
        tag = next((z for z in zones if not z["dead"] and b["l"] <= z["top"] and b["h"] >= z["bot"]), None)
        if tag and k >= 5:
            # SMT within +/-5 bars: compare each index's extreme in the window with its session extreme before the window
            w = rth[max(0, k-5):k+6]; before = rth[:max(0, k-5)]
            pw = [pm.get(x["t"]) for x in w]; pbef = [pm.get(x["t"]) for x in before]
            if before and None not in pw and None not in pbef:
                if bias == "long":
                    a_new = min(x["l"] for x in w) < min(x["l"] for x in before); b_new = min(x["l"] for x in pw) < min(x["l"] for x in pbef)
                else:
                    a_new = max(x["h"] for x in w) > max(x["h"] for x in before); b_new = max(x["h"] for x in pw) > max(x["h"] for x in pbef)
                if a_new != b_new:
                    # CISD on 1m: opposing FVG formed from k-5 onward, closed through within 30 bars of the tag
                    seg = rth[max(0, k-5):min(len(rth), k+31)]; prot = b["l"] if bias == "long" else b["h"]
                    for j in range(2, len(seg)):
                        A, C = seg[j-2], seg[j]
                        if bias == "long" and C["h"] < A["l"]: lvl = A["l"]
                        elif bias == "short" and C["l"] > A["h"]: lvl = A["h"]
                        else: continue
                        for m in range(j+1, len(seg)):
                            prot = min(prot, seg[m]["l"]) if bias == "long" else max(prot, seg[m]["h"])
                            if (bias == "long" and seg[m]["c"] > lvl) or (bias == "short" and seg[m]["c"] < lvl):
                                eb = seg[m]; e = eb["c"]; stop = prot - TICK if bias == "long" else prot + TICK; risk = abs(e - stop)
                                if risk <= 0: break
                                res = {}
                                for R in (1, 2, 3):
                                    tgt = e + R*risk if bias == "long" else e - R*risk; out = None; when = None
                                    for x in [x for x in rth if x["t"] > eb["t"]]:
                                        if (bias == "long" and x["l"] <= stop) or (bias == "short" and x["h"] >= stop): out = -1.0; when = x["t"]; break
                                        if (bias == "long" and x["h"] >= tgt) or (bias == "short" and x["l"] <= tgt): out = float(R); when = x["t"]; break
                                    if out is None: out = round(((rth[-1]["c"] - e) if bias == "long" else (e - rth[-1]["c"])) / risk, 2); when = rth[-1]["t"]
                                    res[f"{R}R"] = dict(r=out, exit_time=when.strftime("%I:%M %p"), usd_per_micro=round(out * risk * PV[sym], 2))
                                # sweep/break bias of the overnight high/low (research: sweep -> opposite extreme 41.5% vs 14.3% after a break)
                                on = [x for x in m1 if on_start <= x["t"] < open_t]; sb = None
                                if on:
                                    onh, onl = max(x["h"] for x in on), min(x["l"] for x in on)
                                    for x in [x for x in rth if x["t"] <= eb["t"]]:
                                        if x["h"] > onh: sb = ("sweep of the overnight high", "short") if x["c"] <= onh else ("break of the overnight high", "long"); break
                                        if x["l"] < onl: sb = ("sweep of the overnight low", "long") if x["c"] >= onl else ("break of the overnight low", "short"); break
                                sweep_info = dict(sweep_break=sb[0] if sb else "no touch of the overnight high/low yet", aligned=(sb[1] == bias) if sb else None)
                                return dict(status="trade", symbol=sym, side=bias, **sweep_info, tag_time=b["t"].strftime("%I:%M %p"), entry_time=eb["t"].strftime("%I:%M %p"),
                                            entry=round(e, 2), stop=round(stop, 2), risk_pts=round(risk, 2), risk_usd_micro=round(risk * PV[sym], 2),
                                            gap=[round(tag["bot"], 2), round(tag["top"], 2)], smt=f"{sym} {'new' if a_new else 'no new'} extreme vs {partner} {'new' if b_new else 'no new'}", results=res, **info)
                        break
    return dict(status="bias, no full setup by noon", **info)

def load(days):
    nq1, es1 = one_min("NQ=F", days), one_min("ES=F", days)
    nqh, esh = y("NQ=F", "60m", rng="730d"), y("ES=F", "60m", rng="730d")
    return nq1, es1, nqh, esh

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "backtest"
    if mode == "backtest":
        nq1, es1, nqh, esh = load(29)
        days = sorted({b["t"].date() for b in nq1 if b["t"].weekday() < 5 and b["t"].time() >= dt.time(9, 30)})
        trades = []
        for d in days:
            for sym, m1, p1, h1, partner in (("NQ", nq1, es1, nqh, "ES"), ("ES", es1, nq1, esh, "NQ")):
                r = run_day(d, sym, partner, m1, p1, h1)
                if r["status"] == "trade": r["day"] = str(d); trades.append(r)
        print("sessions", len(days), days[0], "to", days[-1])
        for t in trades: print(t["day"], t["symbol"], t["side"], t["entry_time"], "aligned", t["aligned"], "risk", t["risk_pts"], {k: v["r"] for k, v in t["results"].items()})
        summ = {}
        for sym in ("NQ", "ES", "ALL"):
            ts = [t for t in trades if sym == "ALL" or t["symbol"] == sym]
            for R in ("1R", "2R", "3R"):
                rs = [t["results"][R]["r"] for t in ts]
                if rs: summ[f"{sym} {R}"] = dict(n=len(rs), win=round(sum(1 for x in rs if x > 0) / len(rs) * 100), total_r=round(sum(rs), 2), usd_1_micro=round(sum(t["results"][R]["usd_per_micro"] for t in ts), 2))
        print(json.dumps(summ, indent=0))
        json.dump(dict(trades=trades, summary=summ, sessions=len(days), first=str(days[0]), last=str(days[-1])), open("bt1m.json", "w"), indent=1, default=str)
    else:
        nq1, es1, nqh, esh = load(3); d = dt.datetime.now(ET).date()
        out = dict(date=str(d), checked_at=dt.datetime.now(ET).isoformat(timespec="seconds"),
                   NQ=run_day(d, "NQ", "ES", nq1, es1, nqh), ES=run_day(d, "ES", "NQ", es1, nq1, esh))
        json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "today.json", "w"), indent=1, default=str); print(json.dumps(out, indent=1, default=str))
