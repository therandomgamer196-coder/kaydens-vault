# Daily automated coin check for the meme coins the crypto monitor trades (Kayden's coin-check skill, automated).
# Verdict OK = still matches the hand-checked Oct 3 WATCH status; CHANGED/FAIL = block paper entries.
import json, time, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
UA = {"User-Agent": "Mozilla/5.0", "accept": "application/json"}
COINS = {  # sym: (chain, address, baseline unlabeled top-10 %, baseline biggest unlabeled wallet %)
    "PEPE": ("eth", "0x6982508145454ce325ddbe47a25d4ec3d2311933", 35.4, 8.83),
    "BONK": ("sol", "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", 38.5, 8.83),
    "WIF": ("sol", "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm", 46.5, 13.72),
    "PENGU": ("sol", "2zMMhcVQEXDtdE6vsFS7S7D5oUodfJHE8vd1gnBouauv", 38.0, 9.61),
}
DEAD = ("", "0x0000000000000000000000000000000000000000", "0x000000000000000000000000000000000000dead")
def get(u):
    err = None
    for i in range(3):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())
        except Exception as e: err = e; time.sleep(4 * (i + 1))
    raise RuntimeError(str(err)[:100])
def check(sym, chain, addr, base_unl, base_max):
    flags = []; r = dict(symbol=sym, address=addr)
    if chain == "sol":
        d = get(f"https://api.rugcheck.xyz/v1/tokens/{addr}/report"); known = d.get("knownAccounts") or {}
        if d.get("rugged"): flags.append("marked rugged")
        if d.get("mintAuthority"): flags.append("mint authority not revoked")
        if d.get("freezeAuthority"): flags.append("freeze authority not revoked")
        hs = [dict(pct=h["pct"], label=(known.get(h.get("owner")) or known.get(h.get("address")) or {}).get("name"), insider=h.get("insider")) for h in (d.get("topHolders") or [])[:10]]
        if any(h["insider"] for h in hs): flags.append("insider wallet in top 10")
        sup = float(d["token"]["supply"]); net = max([n["currentHolding"] / sup * 100 for n in (d.get("insiderNetworks") or [])] or [0])
        r["net_max_pct"] = round(net, 1) if net <= 100 else None
        if r["net_max_pct"] and r["net_max_pct"] > 10: flags.append(f"linked-wallet network holds {r['net_max_pct']}%")
        r["verify"] = f"https://rugcheck.xyz/tokens/{addr}"
    else:
        d = get(f"https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses={addr}")["result"][addr.lower()]
        live_owner = (d.get("owner_address") or "").lower() not in DEAD
        for k, lab in (("is_honeypot", "honeypot"), ("hidden_owner", "hidden owner"), ("can_take_back_ownership", "owner can take back control"), ("owner_change_balance", "owner can change balances"), ("selfdestruct", "self-destruct"), ("cannot_sell_all", "cannot sell all")):
            if d.get(k) == "1": flags.append(lab)
        if live_owner and (d.get("is_blacklisted") == "1" or d.get("is_mintable") == "1"): flags.append("blacklist/mint controlled by a live owner")
        if float(d.get("sell_tax") or 0) > 0.05 or float(d.get("buy_tax") or 0) > 0.05: flags.append("tax over 5%")
        hs = [dict(pct=float(h["percent"]) * 100, label=h.get("tag") or ("locked" if h.get("is_locked") else None), insider=False) for h in (d.get("holders") or [])[:10]]
        r["verify"] = f"https://gopluslabs.io/token-security/1/{addr}"
    unl = [h["pct"] for h in hs if not h["label"]]
    r["unlabeled_top10_pct"] = round(sum(unl), 1); r["max_unlabeled_pct"] = round(max(unl or [0]), 2)
    if r["unlabeled_top10_pct"] > base_unl + 5: flags.append(f"unidentified top-10 wallets up to {r['unlabeled_top10_pct']}% (was {base_unl}%)")
    if r["max_unlabeled_pct"] > max(base_max + 3, 15): flags.append(f"one unidentified wallet now holds {r['max_unlabeled_pct']}% (was {base_max}%)")
    r["flags"] = flags; r["verdict"] = "OK" if not flags else "BLOCK"; return r
if __name__ == "__main__":
    now = dt.datetime.now(ZoneInfo("America/New_York")); out = {}
    for s, (c, a, bu, bm) in COINS.items():
        try: out[s] = check(s, c, a, bu, bm)
        except Exception as e: out[s] = dict(symbol=s, verdict="BLOCK", flags=[f"check failed: {e}"])
        time.sleep(1.5)
    print(json.dumps(dict(checked_at=now.isoformat(timespec="seconds"), checked_time=now.strftime("%-I:%M %p ET"), date=now.strftime("%Y-%m-%d"), coins=out), indent=1))
