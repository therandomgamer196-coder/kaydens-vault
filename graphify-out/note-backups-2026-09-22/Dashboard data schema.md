---
tags: [dashboard, reference]
---

# Dashboard data schema

`punch-in-data.js` is one statement: `window.PUNCH_IN_DATA = { ... };` — the same object stored in the artifact database at `dashboard/data`.

```json
{
  "updatedAt": "ISO UTC time of the sync",
  "events": [
    { "id": "calendar event id", "title": "Papa John's shift | Greenfield: <event> | <Name> wedding | ...",
      "note": "optional detail", "type": "shift | bill | pay | personal",
      "allDay": false, "start": "ISO with offset", "end": "ISO with offset",
      "date": "YYYY-MM-DD (all-day only)", "link": "Google Calendar htmlLink" }
  ],
  "inbox": {
    "unreadTotal": 201, "todayUnreadCount": 15,
    "highlights": [ { "id": "thread id", "sender": "", "subject": "", "cat": "security | account | bill",
                      "when": "ISO UTC", "link": "https://mail.google.com/mail/u/0/#inbox/<id>" } ],
    "noiseSample": "senders/topics not flagged"
  },
  "robinhood": {
    "totalValue": 0, "dayChange": 0, "dayChangePct": 0, "realizedPnlAllTime": 0, "note": "one sentence",
    "accounts": [ { "name": "Individual | Agentic", "mask": "last 4", "value": 0, "note": "holdings phrase" } ]
  },
  "payPeriods": {
    "papaJohns":  { "label": "Papa John's", "periodStart": "YYYY-MM-DD", "periodEnd": "YYYY-MM-DD", "hours": 0, "rate": 12.5, "estPay": 0 },
    "greenfield": { "label": "Greenfield",  "periodStart": "YYYY-MM-DD", "periodEnd": "YYYY-MM-DD", "hours": 0, "rate": 20,   "estPay": 0 }
  },
  "weather": { "place": "Ephrata, PA", "station": "", "tempF": 0, "condition": "", "humidity": 0,
               "wind": "N mph", "observedAt": "", "periods": [ { "name": "Today", "temp": "High X° / Low Y°", "text": "" } ] }
}
```

Account values can be negative (margin debit). Only the last 4 digits of any account number are ever stored.
