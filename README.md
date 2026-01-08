# 🎯 SeatScout - HubSpot Seat Optimizer

> **Stop paying for seats you don't need.**

HubSpot shows you who's inactive. SeatScout shows you where you're overpaying.

---

## 💰 The Problem

Most companies waste **20-40% of their HubSpot budget** on unused seats:

- ❌ Deactivated users who still have paid seats assigned (HubSpot doesn't auto-remove them)
- ❌ Users who login but don't actually *work* in HubSpot
- ❌ Users with expensive Sales Hub seats who never use sales features
- ❌ Old employees who left months ago but still occupy licenses

**HubSpot's native tools don't show you this.** They show last login date, but not actual usage.

---

## ✨ What SeatScout Does

SeatScout audits your HubSpot account and finds:

1. **Deactivated users with paid seats** (100% confidence)
2. **Users with no login activity** in 90+ days (Enterprise only, 95% confidence)
3. **Users with no real work** - no calls, meetings, tasks, CRM updates (80% confidence)
4. **Estimated dollar savings** - monthly and annual waste

### Example Output

```
🚨 HIGH CONFIDENCE - REMOVE IMMEDIATELY (3 users, $225/mo)
----------------------------------------------------------------------
1. John Doe (john@company.com)
   Account deactivated - check if seat still assigned
   Confidence: 100% | Monthly cost: $75

2. Jane Smith (jane@company.com)
   No login in 120 days, no engagements detected
   Confidence: 95% | Monthly cost: $75

⚠️  MEDIUM-HIGH CONFIDENCE (2 users, $150/mo)
----------------------------------------------------------------------
1. Old Employee (old@company.com)
   No engagements in 60+ days, no CRM activity in 30+ days
   Confidence: 80% | Monthly cost: $75

SUMMARY
----------------------------------------------------------------------
Estimated monthly waste: $225
Estimated annual waste: $2,700
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- HubSpot account (Free, Starter, Professional, or Enterprise)
- HubSpot Private App API key

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/seatscout.git
cd seatscout

# Install dependencies
pip install requests

# Set your API key
export HUBSPOT_API_KEY='your-private-app-token-here'

# Run the audit
python hubspot_user_audit.py
```

### Getting Your API Key

1. In HubSpot, go to **Settings** → **Integrations** → **Private Apps**
2. Click **"Create a private app"**
3. Name it "SeatScout" and give it these scopes:
   - `crm.objects.contacts.read`
   - `crm.objects.deals.read`
   - `crm.objects.owners.read`
   - `crm.objects.users.read` (if available)
   - `sales-email-read` (optional, for email tracking)
4. Click **"Create app"** and copy the access token

---

## 📊 What Gets Tracked

### ✅ What We Track

**Tier 1 Signals (Highest Confidence):**
- Deactivated user status (100% accurate)
- Login history (Enterprise only, 95% accurate)

**Tier 2 Signals (High Confidence):**
- Calls, emails, meetings, tasks, notes created/logged
- CRM object modifications (contacts, deals, tickets)
- Owner assignments

### ⚠️ What We DON'T Track

- Report/dashboard viewing (HubSpot doesn't expose this)
- Sequence usage (requires additional scopes)
- Marketing email activity
- Some mobile app usage

**Accuracy:**
- **Enterprise accounts**: 90-95% (with login history API)
- **Pro/Standard accounts**: 70-80% (engagement + CRM activity only)

---

## 🎯 Use Cases

### For Finance/Operations Teams
- Audit SaaS spend before renewals
- Find quick cost savings
- Justify budget cuts with data

### For IT/RevOps Teams
- Clean up user access
- Ensure compliance (remove ex-employees)
- Optimize license allocation

### For Managers
- See who's actually using HubSpot
- Identify training needs
- Right-size team access

---

## 📋 Output

SeatScout generates two outputs:

1. **Console report** - Detailed breakdown with confidence scores
2. **CSV file** (`seatscout_report.csv`) - Ready to share with finance/leadership

CSV includes:
- User name and email
- Confidence score (0-100%)
- Reason for flagging
- Estimated monthly/annual cost

---

## 🔒 Security & Privacy

- **Read-only access** - SeatScout never modifies your HubSpot data
- **No data storage** - We don't store or transmit your data anywhere
- **Local execution** - Runs entirely on your machine
- **Open source** - Audit the code yourself

---

## ⚠️ Known Limitations
   
   - Cannot detect "view-only" seats that should be upgraded
   - Doesn't track report/dashboard usage (not exposed via API)
   - Sequence engagement requires additional scopes
   - Accuracy varies by HubSpot tier (70-95%)

---

## 🛠️ Troubleshooting

### "No engagements attributed"

**Cause:** Engagements don't have owners assigned

**Fix:** In HubSpot:
1. Go to **Settings** → **Properties** → **Contact properties**
2. Find "HubSpot Owner" and set a default value
3. Train users to assign owners when logging calls/meetings

### "Enterprise login API not available"

**Normal for Pro/Standard accounts.** You'll get 70-80% accuracy instead of 95%.

To upgrade accuracy: Contact HubSpot to upgrade to Enterprise tier.

### "API rate limit exceeded"

**Cause:** Too many API calls in a short time

**Fix:** Wait 10 minutes and run again. For large accounts (500+ users), contact us about the Enterprise version.

---

## 💡 Next Steps After Running

1. **Review the CSV** - Share with your finance team
2. **Cross-check in HubSpot** - Go to Settings → Users & Teams → Seats
3. **For deactivated users**: 
   - Reactivate the user
   - Unassign their seat
   - Deactivate again
4. **For inactive users**: Contact them to verify they still need access
5. **Set calendar reminder** to run quarterly

---

## 🗺️ Roadmap

### Coming Soon
- [ ] Web-based version (no Python required)
- [ ] Automated weekly/monthly reports
- [ ] Slack/email notifications
- [ ] Seat downgrade recommendations (Sales → Core)
- [ ] Historical trend tracking

**Want these features faster?** Star the repo and let us know! ⭐

---

## 🤝 Contributing

Found a bug? Have a feature request? 

1. Open an issue
2. Submit a pull request
3. Share your results (anonymized) so we can improve accuracy

---

## 📄 License

MIT License - Use freely, modify as needed, no warranty provided.

---

## 🙋 FAQ

**Q: Will this work on my HubSpot tier?**  
A: Yes! Works on Free, Starter, Professional, and Enterprise. Accuracy varies by tier.

**Q: How long does it take to run?**  
A: 30 seconds for small accounts (< 50 users), 2-3 minutes for large accounts (500+ users).

**Q: Can I run this on multiple HubSpot accounts?**  
A: Yes! Just change the API key for each account.

**Q: What if I find a false positive?**  
A: Always cross-check with HubSpot's "Last Active" column before removing seats. When in doubt, contact the user first.

**Q: Can I use this commercially?**  
A: Yes! MIT license allows commercial use. If you offer this as a service, we'd love to hear about it.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/wjewell3/seatscout/issues)
- **Email**: jewell.will@gmail.com

---

## ⭐ Show Your Support

If SeatScout saved you money, give us a star! It helps others discover the tool.

**Saved your company $5K+?** Share your story (anonymized) so others can see the impact!

---

**Built with ❤️ for HubSpot admins tired of overpaying for unused seats.**

*Not affiliated with HubSpot, Inc.*