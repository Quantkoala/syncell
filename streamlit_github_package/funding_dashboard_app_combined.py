
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io

st.set_page_config(layout="wide")

# Language selector
lang = st.sidebar.selectbox("🌐 Language / 語言", ["English", "繁體中文"])

# Localized label dictionaries
labels = {
    "English": {
        "title": "🧠 Competitor Intelligence Dashboard",
        "pages": [
            "KPI Snapshot",
            "Advanced KPI Dashboard",
            "Funding History Timeline",
            "Competitor News Feed",
            "Scatter Plots by Competitor",
            "News Tag Summary",
            "Competitor Activity Timeline",
            "Competitor by Announcement Type"
        ],
        "filter_by_tag": "Filter by tag",
        "select_competitors": "Select Competitors",
        "select_company": "Select Company",
        "open": "Open",
        "no_data": "No data available."
    },
    "繁體中文": {
        "title": "🧠 競爭對手情報儀表板",
        "pages": [
            "KPI 快照",
            "進階 KPI 儀表板",
            "融資歷程圖",
            "新聞資料流",
            "依公司分類散點圖",
            "新聞類型統計",
            "活動時間軸",
            "公司與公告類型分析"
        ],
        "filter_by_tag": "依標籤篩選",
        "select_competitors": "選擇公司",
        "select_company": "選擇公司",
        "open": "開啟",
        "no_data": "目前無可用資料。"
    }
}

L = labels[lang]
st.title(L["title"])

@st.cache_data
def fetch_csv_from_url(secret_key, parse_tags=True):
    try:
        url = st.secrets[secret_key]
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            if parse_tags:
                df['title'] = df['title'].fillna("")
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df['tag'] = df.apply(tag_news_item, axis=1)
                df = df.dropna(subset=['date'])
            return df
        else:
            st.error(f"Failed to fetch data from: {url}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching '{secret_key}': {e}")
        return pd.DataFrame()

def tag_news_item(row):
    title = row['title'].lower()
    tag_keywords = {
        'Funding': ['series a', 'series b', 'series c', 'funding', 'investment', 'raises', 'venture capital', 'financing'],
        'Product Launch': ['launch', 'introduces', 'unveils', 'releases', 'new product', 'commercial availability', 'rolls out'],
        'M&A': ['merger', 'acquisition', 'acquires', 'buys', 'takeover', 'merges with'],
        'Partnership': ['partnership', 'collaboration', 'teams up', 'joins forces', 'strategic alliance'],
        'IPO / Capital Market': ['sec filing', 'ipo', 'public offering', 'spac', 'files s-1'],
        'Clinical Development': ['clinical trial', 'phase i', 'phase ii', 'phase iii', 'first-in-human', 'pivotal trial'],
        'Patent': ['patent', 'intellectual property', 'ip protection', 'trademark'],
        'Recognition': ['award', 'recognition', 'grants', 'honor', 'winner', 'recipient'],
        'Regulatory': ['fda approval', 'ce mark', '510(k)', 'regulatory clearance', 'notified body'],
        'Corporate Update': ['expands', 'rebrands', 'opens office', 'hiring', 'growth update', 'board member'],
    }
    for tag, keywords in tag_keywords.items():
        if any(kw in title for kw in keywords):
            return tag
    return 'Other' if lang == "English" else '其他'

page = st.sidebar.selectbox("📂", L["pages"])
news_df = fetch_csv_from_url("news_feed_url", parse_tags=True)
data = fetch_csv_from_url("funding_data_url", parse_tags=False)


# Enhanced KPI Snapshot Page with interactive filters and KPI ratios

if page == L["pages"][0]:  # KPI Snapshot
    if not data.empty:
        st.subheader(L["pages"][0])

        # Interactive Company Filter
        companies = data['Company'].dropna().unique().tolist()
        selected = st.multiselect("📌 Select companies to view:", companies, default=companies)
        filtered_data = data[data['Company'].isin(selected)]

        # KPI Summary
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Total Funding (M)", f"${filtered_data['Funding ($M)'].sum():,.1f}")
        col2.metric("📊 Total Clinical Trials", f"{filtered_data['Clinical Trials'].sum():.0f}")
        col3.metric("🔬 Active Products", f"{filtered_data['Active Products'].sum():.0f}")
        col4.metric("📄 Patents Filed", f"{filtered_data['Patents Filed'].sum():.0f}")

        # Basic KPI Charts
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.bar(filtered_data, x="Company", y="Funding ($M)", color="Company", title="Total Funding"), use_container_width=True)
            st.plotly_chart(px.bar(filtered_data, x="Company", y="Patents Filed", color="Company", title="Patents Filed"), use_container_width=True)
        with col2:
            st.plotly_chart(px.bar(filtered_data, x="Company", y="Active Products", color="Company", title="Active Products"), use_container_width=True)
            st.plotly_chart(px.bar(filtered_data, x="Company", y="Clinical Trials", color="Company", title="Clinical Trials"), use_container_width=True)

        # KPI Ratios and Derived Metrics
        if "Active Products" in filtered_data.columns and (filtered_data["Active Products"] != 0).any():
            filtered_data["Funding per Product"] = filtered_data["Funding ($M)"] / filtered_data["Active Products"]
            st.plotly_chart(
                px.bar(filtered_data, x="Company", y="Funding per Product", color="Company", title="💡 Funding per Product"),
                use_container_width=True
            )

        if "Clinical Trials" in filtered_data.columns and (filtered_data["Clinical Trials"] != 0).any():
            filtered_data["Patents per Trial"] = filtered_data["Patents Filed"] / filtered_data["Clinical Trials"]
            st.plotly_chart(
                px.bar(filtered_data, x="Company", y="Patents per Trial", color="Company", title="💡 Patents per Clinical Trial"),
                use_container_width=True
            )

        # Leaderboard Table
        st.subheader("🏆 KPI Leaderboard")
        st.dataframe(
            filtered_data.sort_values("Funding ($M)", ascending=False)[
                ["Company", "Funding ($M)", "Active Products", "Patents Filed", "Clinical Trials"]
            ]
        )
    else:
        st.warning(L["no_data"])
elif page == L["pages"][1]:  # Advanced KPI Dashboard
    if not data.empty:
        st.subheader(L["pages"][1])

        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Total Funding (M)", f"${data['Funding ($M)'].sum():,.1f}")
            st.metric("📊 Avg. Clinical Trials", f"{data['Clinical Trials'].mean():.1f}")
        with col2:
            st.metric("🔬 Avg. Active Products", f"{data['Active Products'].mean():.1f}")
            st.metric("📄 Total Patents Filed", f"{data['Patents Filed'].sum():,.0f}")

        st.plotly_chart(px.imshow(
            data.set_index("Company")[["Funding ($M)", "Patents Filed", "Active Products", "Clinical Trials"]],
            text_auto=True, aspect="auto", title="📊 Competitor KPI Matrix"
        ), use_container_width=True)

        top_companies = data.nlargest(3, "Funding ($M)")["Company"]
        fig = go.Figure()
        for comp in top_companies:
            row = data[data["Company"] == comp][["Patents Filed", "Active Products", "Clinical Trials"]]
            fig.add_trace(go.Scatterpolar(
                r=row.values.flatten().tolist(),
                theta=["Patents", "Products", "Trials"],
                fill='toself',
                name=comp
            ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(L["no_data"])
