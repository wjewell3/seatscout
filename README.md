# SeatScout - HubSpot Seat Audit (Python POC)

A lightweight Python script to detect inactive HubSpot users (seats) and estimate potential wasted spend.  

This is a **proof-of-concept** for educational and testing purposes. A full-featured commercial SaaS app with dashboards and recurring monitoring is coming soon.

---

## Features

- Connects to HubSpot via read-only private app token  
- Flags users with no detectable activity in the past X days  
- Outputs a simple list of inactive users  
- Estimates potential monthly/annual savings (configurable per-seat cost)  

---

## Usage

1. Clone the repo
2. Install dependencies:
```bash
pip install requests
```
3. Set your HubSpot token in hubspot_test.py
4. Run: python hubspot_test.py

Sample Output:
```
Summary
-------
Inactive seats: 3
Estimated monthly waste: $60
Estimated annual waste: $720

Inactive users:
Test test (blah@gmail.com) — last detected activity 2026-01-06 (inactive)
Sales Rep4 (testuser123@gmail.com) — last detected activity 2026-01-06 (inactive)
Will Jewell (jewell.will@gmail.com) — last detected activity 2026-01-06 (inactive)

**Estimated savings are based on an assumed average paid seat cost of $20/mo. Actual HubSpot seat pricing varies by plan type, contract terms, and billing frequency.
```