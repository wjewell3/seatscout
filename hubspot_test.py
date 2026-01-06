import requests, os
from datetime import datetime, timedelta, timezone

TOKEN = os.getenv("HUBSPOT_API_KEY") # Your HubSpot private app token
INACTIVE_DAYS = 0 #30 #60 #90

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

cutoff = datetime.now(timezone.utc) - timedelta(days=INACTIVE_DAYS)

resp = requests.get(
    "https://api.hubapi.com/crm/v3/owners/",
    headers=headers,
    timeout=10
)
resp.raise_for_status()

SEAT_COST = 20  # baseline

inactive_users = []
for o in resp.json()["results"]:
    updated = datetime.fromisoformat(o["updatedAt"].replace("Z", "+00:00"))
    if updated < cutoff:
        inactive_users.append(o)

count = len(inactive_users)
monthly = count * SEAT_COST

print("\nSummary")
print("-------")
print(f"Inactive seats: {count}")
print(f"Estimated monthly waste: ${monthly}")
print(f"Estimated annual waste: ${monthly * 12}\n")

print("Inactive users:")
for o in resp.json()["results"]:
    updated = datetime.fromisoformat(o["updatedAt"].replace("Z", "+00:00"))
    if updated < cutoff:
        print(
            f"{o['firstName']} {o['lastName']} "
            f"({o['email']}) — "
            f"last detected activity {updated.date()} "
            f"({'inactive' if updated < cutoff else 'active'})"
        )

print("\n**Estimated savings are based on an assumed average paid seat cost of $20/mo. Actual HubSpot seat pricing varies by plan type, contract terms, and billing frequency.")