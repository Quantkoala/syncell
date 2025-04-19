# 📊 Competitor Funding Intelligence Dashboard

This is a Streamlit-based business intelligence dashboard built for Syncell Inc.'s Corporate Affairs team to monitor and benchmark strategic activity of key competitors.

## 🔍 Features

- **KPI Snapshot:** Visualize funding, clinical trial count, product activity
- **Funding History Timeline:** Track funding rounds over time
- **Competitor News Feed:** Display and tag industry announcements
- **News Tag Summary & Scatter Charts:** Understand distribution of news categories by competitor
- **Multilingual UI:** Fully bilingual (English / Traditional Chinese)
- **Material Tracker (temporarily disabled):** Tag & filter press releases by significance

## 🗂 Folder Structure

```
├── funding_dashboard_app.py      # Main Streamlit app
├── secrets.toml                  # [Streamlit Cloud] Secure config for data sources
├── requirements.txt              # App dependencies
├── data/                         # (Optional) for local CSV backups
├── docs/                         # (Optional) screenshots, guides, onboarding
```

## 🚀 Deployment (Streamlit Cloud)

1. Push to a GitHub repo
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **New App** → Select this repo → Branch: `main`
4. Add `secrets.toml` under app settings (copy from your local version)
5. Hit **Deploy**

## 🔒 Secrets Configuration (`secrets.toml`)

```toml
funding_data_url = "https://..."
funding_history_url = "https://..."
news_feed_url = "https://..."
```

## ✅ Recommended

- Keep all `.csv` files on Google Sheets and publish them to the web for live use
- Use GitHub Issues or Projects to plan feature changes
- Re-enable `Material Tracker` in the `.py` file when stable

---
Built and maintained by Syncell Corporate Affairs and Analytics Team
