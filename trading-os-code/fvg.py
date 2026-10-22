import json, subprocess, datetime as dt
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")
def fetch(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=15m&range=1d"
    r = json.loads(subprocess.run(["curl","-s","-m","15","-A","Mozilla/5.0",url],capture_output=True,text=True).stdout)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]; bars = []
    for i, t in enumerate(r["timestamp"]):
        o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if None in (o, h, l, c): continue
        ts = dt.datetime.fromtimestamp(t, ET)
        if dt.time(9,30) <= ts.time() < dt.time(16,0): bars.append(dict(t=ts,o=o,h=h,l=l,c=c))
    return bars, r["meta"].get("regularMarketPrice")
now = dt.datetime.now(ET); out = []
for sym in ("QQQ","SPY"):
    bars, price = fetch(sym)
    done = [b for b in bars if b["t"].date()==now.date() and b["t"]+dt.timedelta(minutes=15) <= now]
    gaps = []
    for i in range(2, len(done)):
        A, B, C = done[i-2], done[i-1], done[i]
        if C["l"] > A["h"] and B["c"] > B["o"] and (C["l"]-A["h"])/A["h"] >= 0.0005 and not any(x["c"] < A["h"] for x in done[i+1:]):
            gaps.append(dict(formed=C["t"].strftime("%H:%M"), bottom=round(A["h"],2), top=round(C["l"],2)))
    entry = None
    if dt.time(9,45) <= now.time() <= dt.time(14,50):
        for g in reversed(gaps):
            if g["bottom"] <= price <= g["top"]:
                stop = round(g["bottom"]*0.999, 2); entry = dict(price=price, stop=stop, target=round(price+2*(price-stop),2), gap=g); break
    out.append(dict(symbol=sym, price=price, live_gaps=gaps, entry=entry))
print(json.dumps(dict(checked_at=now.isoformat(timespec="seconds"), signals=out), indent=1))