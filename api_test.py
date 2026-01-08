#!/usr/bin/env python3
"""
HubSpot API Explorer - Get acquainted with the HubSpot API
Tests various endpoints and shows you what data is available
"""

import requests
import os
import sys
import json
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = os.getenv("HUBSPOT_API_KEY")
if not TOKEN:
    print("❌ ERROR: HUBSPOT_API_KEY environment variable not set")
    print("   Set it with: export HUBSPOT_API_KEY='your-token-here'")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)

def print_json(data, max_items=3):
    """Pretty print JSON data, limiting arrays."""
    if isinstance(data, list):
        print(f"  Found {len(data)} items. Showing first {min(len(data), max_items)}:")
        for item in data[:max_items]:
            print(json.dumps(item, indent=2))
    else:
        print(json.dumps(data, indent=2))

def make_request(url, method="GET", **kwargs):
    """Make API request with error handling."""
    try:
        if method == "GET":
            resp = requests.get(url, headers=HEADERS, timeout=10, **kwargs)
        elif method == "POST":
            resp = requests.post(url, headers=HEADERS, timeout=10, **kwargs)
        
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"  ⚠️  403 Forbidden - Missing scope or insufficient permissions")
            return None
        print(f"  ❌ Error {e.response.status_code}: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {e}")
        return None

# =============================================================================
# TEST 1: Account Info / Owners
# =============================================================================
def test_owners():
    print_section("TEST 1: Owners/Users (crm.objects.owners.read)")
    
    print("\n📋 Active Owners:")
    data = make_request("https://api.hubapi.com/crm/v3/owners/", params={"limit": 5, "archived": "false"})
    if data:
        print(f"  Total active owners: {data.get('results', [])}")
        if data.get('results'):
            print("\n  Sample owner:")
            owner = data['results'][0]
            print(f"    ID: {owner.get('id')}")
            print(f"    Email: {owner.get('email')}")
            print(f"    Name: {owner.get('firstName')} {owner.get('lastName')}")
            print(f"    User ID: {owner.get('userId')}")
            print(f"    Created: {owner.get('createdAt')}")
    
    print("\n📋 Archived/Deactivated Owners:")
    data = make_request("https://api.hubapi.com/crm/v3/owners/", params={"limit": 5, "archived": "true"})
    if data:
        print(f"  Total archived owners: {len(data.get('results', []))}")
        if data.get('results'):
            print("\n  Sample archived owner:")
            owner = data['results'][0]
            print(f"    ID: {owner.get('id')}")
            print(f"    Email: {owner.get('email')}")

# =============================================================================
# TEST 2: Login History (Enterprise Only)
# =============================================================================
def test_login_history():
    print_section("TEST 2: Login History (Enterprise Only)")
    
    print("\n🔐 Attempting to fetch login history...")
    data = make_request("https://api.hubapi.com/account-info/v3/activity/login", params={"limit": 5})
    if data:
        print(f"  ✅ Enterprise API available!")
        print(f"  Total login records: {len(data.get('results', []))}")
        if data.get('results'):
            print("\n  Sample login record:")
            login = data['results'][0]
            print(f"    User ID: {login.get('userId')}")
            print(f"    Login Time: {login.get('loginAt')}")
            print(f"    IP: {login.get('ipAddress', 'N/A')}")
    else:
        print("  ℹ️  Enterprise login API not available (normal for Pro/Starter tiers)")

# =============================================================================
# TEST 3: Engagements (v1 API)
# =============================================================================
def test_engagements():
    print_section("TEST 3: Engagements - Calls, Emails, Meetings, Tasks")
    
    print("\n📞 Fetching recent engagements...")
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    cutoff_ts = int(cutoff.timestamp() * 1000)
    
    data = make_request("https://api.hubapi.com/engagements/v1/engagements/paged", 
                       params={"limit": 10})
    if data:
        results = data.get('results', [])
        print(f"  Total engagements found: {len(results)}")
        
        if results:
            print("\n  Sample engagement:")
            item = results[0]
            eng = item.get('engagement', {})
            assoc = item.get('associations', {})
            
            print(f"    Type: {eng.get('type')}")
            print(f"    Created: {datetime.fromtimestamp(eng.get('createdAt', 0)/1000)}")
            print(f"    Owner ID: {eng.get('ownerId', 'None')}")
            print(f"    Created By User ID: {eng.get('createdBy', 'None')}")
            print(f"    Source ID: {eng.get('sourceId', 'None')}")
            print(f"    Associations:")
            print(f"      Contact IDs: {assoc.get('contactIds', [])}")
            print(f"      Deal IDs: {assoc.get('dealIds', [])}")
            print(f"      Owner IDs: {assoc.get('ownerIds', [])}")
        
        # Count by type
        types = {}
        for item in results:
            eng_type = item.get('engagement', {}).get('type', 'unknown')
            types[eng_type] = types.get(eng_type, 0) + 1
        
        print(f"\n  Engagement breakdown:")
        for eng_type, count in types.items():
            print(f"    {eng_type}: {count}")

# =============================================================================
# TEST 4: CRM Objects - Contacts
# =============================================================================
def test_contacts():
    print_section("TEST 4: CRM Contacts (crm.objects.contacts.read)")
    
    print("\n👤 Fetching recent contacts...")
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    cutoff_ts = int(cutoff.timestamp() * 1000)
    
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "hs_lastmodifieddate",
                "operator": "GTE",
                "value": str(cutoff_ts)
            }]
        }],
        "properties": ["firstname", "lastname", "email", "hubspot_owner_id", "hs_lastmodifieddate"],
        "limit": 5
    }
    
    data = make_request("https://api.hubapi.com/crm/v3/objects/contacts/search", 
                       method="POST", json=payload)
    if data:
        results = data.get('results', [])
        print(f"  Contacts modified in last 30 days: {len(results)}")
        
        if results:
            print("\n  Sample contact:")
            contact = results[0]
            props = contact.get('properties', {})
            print(f"    ID: {contact.get('id')}")
            print(f"    Name: {props.get('firstname')} {props.get('lastname')}")
            print(f"    Email: {props.get('email')}")
            print(f"    Owner ID: {props.get('hubspot_owner_id', 'None')}")
            print(f"    Last Modified: {props.get('hs_lastmodifieddate')}")

# =============================================================================
# TEST 5: CRM Objects - Deals
# =============================================================================
def test_deals():
    print_section("TEST 5: CRM Deals (crm.objects.deals.read)")
    
    print("\n💼 Fetching recent deals...")
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    cutoff_ts = int(cutoff.timestamp() * 1000)
    
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "hs_lastmodifieddate",
                "operator": "GTE",
                "value": str(cutoff_ts)
            }]
        }],
        "properties": ["dealname", "amount", "dealstage", "hubspot_owner_id", "hs_lastmodifieddate"],
        "limit": 5
    }
    
    data = make_request("https://api.hubapi.com/crm/v3/objects/deals/search", 
                       method="POST", json=payload)
    if data:
        results = data.get('results', [])
        print(f"  Deals modified in last 30 days: {len(results)}")
        
        if results:
            print("\n  Sample deal:")
            deal = results[0]
            props = deal.get('properties', {})
            print(f"    ID: {deal.get('id')}")
            print(f"    Name: {props.get('dealname')}")
            print(f"    Amount: {props.get('amount', 'N/A')}")
            print(f"    Stage: {props.get('dealstage')}")
            print(f"    Owner ID: {props.get('hubspot_owner_id', 'None')}")
            print(f"    Last Modified: {props.get('hs_lastmodifieddate')}")

# =============================================================================
# TEST 6: CRM Objects - Tickets
# =============================================================================
def test_tickets():
    print_section("TEST 6: CRM Tickets (crm.objects.tickets.read)")
    
    print("\n🎫 Fetching recent tickets...")
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    cutoff_ts = int(cutoff.timestamp() * 1000)
    
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "hs_lastmodifieddate",
                "operator": "GTE",
                "value": str(cutoff_ts)
            }]
        }],
        "properties": ["subject", "content", "hs_ticket_priority", "hubspot_owner_id", "hs_lastmodifieddate"],
        "limit": 5
    }
    
    data = make_request("https://api.hubapi.com/crm/v3/objects/tickets/search", 
                       method="POST", json=payload)
    if data:
        results = data.get('results', [])
        print(f"  Tickets modified in last 30 days: {len(results)}")
        
        if results:
            print("\n  Sample ticket:")
            ticket = results[0]
            props = ticket.get('properties', {})
            print(f"    ID: {ticket.get('id')}")
            print(f"    Subject: {props.get('subject', 'N/A')}")
            print(f"    Priority: {props.get('hs_ticket_priority', 'N/A')}")
            print(f"    Owner ID: {props.get('hubspot_owner_id', 'None')}")
            print(f"    Last Modified: {props.get('hs_lastmodifieddate')}")

# =============================================================================
# TEST 7: Properties (understand what fields are available)
# =============================================================================
def test_properties():
    print_section("TEST 7: Available Properties for Contacts")
    
    print("\n📋 Fetching contact properties...")
    data = make_request("https://api.hubapi.com/crm/v3/properties/contacts", params={"limit": 10})
    if data:
        results = data.get('results', [])
        print(f"  Total properties available: {len(results)}")
        
        print("\n  Sample properties (first 5):")
        for prop in results[:5]:
            print(f"    {prop.get('name')}: {prop.get('label')} ({prop.get('type')})")

# =============================================================================
# MAIN
# =============================================================================
def main():
    print("\n" + "="*70)
    print("  HUBSPOT API EXPLORER")
    print("  Get acquainted with what data is available")
    print("="*70)
    
    # Run all tests
    test_owners()
    test_login_history()
    test_engagements()
    test_contacts()
    test_deals()
    test_tickets()
    test_properties()
    
    print_section("✅ API Exploration Complete")
    print("\n💡 Key Takeaways:")
    print("  - Owners API: Shows all users (active + archived)")
    print("  - Engagements API: Tracks calls, emails, meetings, tasks")
    print("  - CRM Objects: Can filter by date and owner_id")
    print("  - Login History: Enterprise only (shows actual login activity)")
    print("  - Properties API: Shows what fields you can query/filter by")
    print("\n📚 Next Steps:")
    print("  - Review the output above to see what data you have")
    print("  - Check which APIs returned 403 (missing scopes)")
    print("  - Use this understanding to improve your audit tool")
    print()

if __name__ == "__main__":
    main()