import streamlit as st
import requests
from datetime import datetime

# ── Config ──────────────────────────────────────────────
API_KEY = "91e0d9e9cec947b29db7388e1e87a92a"
BASE_URL = "https://newsapi.org/v2/top-headlines"

COUNTRIES = {
    "🌍 All": "",
    "🇺🇸 United States": "us",
    "🇬🇧 United Kingdom": "gb",
    "🇮🇳 India": "in",
    "🇦🇺 Australia": "au",
    "🇨🇦 Canada": "ca",
    "🇩🇪 Germany": "de",
    "🇫🇷 France": "fr",
    "🇯🇵 Japan": "jp",
    "🇧🇷 Brazil": "br",
    "🇿🇦 South Africa": "za",
}

CATEGORIES = [
    "general", "business", "technology",
    "science", "health", "sports", "entertainment"
]

# ── Page setup ───────────────────────────────────────────
st.set_page_config(
    page_title="NewsFlow",
    page_icon="📰",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.hero {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    border-left: 5px solid #e63946;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #ffffff;
    margin: 0;
    letter-spacing: -1px;
}

.hero p {
    color: #aaaaaa;
    font-size: 1rem;
    margin-top: 0.4rem;
}

.article-card {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    border-left: 4px solid #e63946;
    transition: box-shadow 0.2s;
}

.article-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.article-source {
    font-size: 0.72rem;
    font-weight: 600;
    color: #e63946;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.article-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: #111111;
    margin: 0.4rem 0 0.5rem 0;
    line-height: 1.4;
}

.article-desc {
    font-size: 0.88rem;
    color: #555555;
    line-height: 1.6;
    margin-bottom: 0.8rem;
}

.article-meta {
    font-size: 0.75rem;
    color: #999999;
}

.article-link {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e63946;
    text-decoration: none;
}

.stat-box {
    background: #f9f9f9;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
    border: 1px solid #efefef;
}

.stat-num {
    font-size: 1.8rem;
    font-weight: 700;
    color: #e63946;
}

.stat-label {
    font-size: 0.78rem;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.no-results {
    text-align: center;
    padding: 3rem;
    color: #999999;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📰 NewsFlow</h1>
    <p>Live headlines from around the world — filtered your way.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar filters ───────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Filters")

    keyword = st.text_input("🔍 Search keyword", placeholder="e.g. climate, AI, cricket...")

    country_label = st.selectbox("🌍 Country", list(COUNTRIES.keys()))
    country_code = COUNTRIES[country_label]

    category = st.selectbox("📂 Topic / Category", CATEGORIES)

    num_articles = st.slider("📄 Number of articles", min_value=5, max_value=50, value=10, step=5)

    fetch = st.button("🔄 Fetch News", use_container_width=True)

# ── Fetch & display ───────────────────────────────────────
def fetch_news(keyword, country, category, page_size):
    params = {
        "apiKey": API_KEY,
        "pageSize": page_size,
        "category": category,
    }
    if country:
        params["country"] = country
    if keyword:
        params["q"] = keyword

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        if data.get("status") == "ok":
            return data.get("articles", []), None
        else:
            return [], data.get("message", "Unknown error from NewsAPI.")
    except Exception as e:
        return [], str(e)

def format_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%b %d, %Y · %H:%M UTC")
    except:
        return date_str or "Unknown date"

if fetch or "articles" not in st.session_state:
    with st.spinner("Fetching latest headlines..."):
        articles, error = fetch_news(keyword, country_code, category, num_articles)
        st.session_state.articles = articles
        st.session_state.error = error
        st.session_state.keyword = keyword

articles = st.session_state.get("articles", [])
error = st.session_state.get("error", None)

if error:
    st.error(f"❌ Could not fetch news: {error}")
elif articles:
    # Stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{len(articles)}</div><div class="stat-label">Articles loaded</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{category.title()}</div><div class="stat-label">Category</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{country_label.split(" ", 1)[-1] if country_label != "🌍 All" else "Global"}</div><div class="stat-label">Region</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Article cards
    for article in articles:
        title = article.get("title") or "No title"
        description = article.get("description") or "No description available."
        source = article.get("source", {}).get("name") or "Unknown source"
        published = format_date(article.get("publishedAt", ""))
        url = article.get("url", "#")
        image = article.get("urlToImage")

        if image:
            img_col, text_col = st.columns([1, 3])
            with img_col:
                st.image(image, use_column_width=True)
            with text_col:
                st.markdown(f"""
                <div class="article-card">
                    <div class="article-source">{source}</div>
                    <div class="article-title">{title}</div>
                    <div class="article-desc">{description}</div>
                    <div class="article-meta">🕐 {published}</div><br>
                    <a class="article-link" href="{url}" target="_blank">Read full article →</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="article-card">
                <div class="article-source">{source}</div>
                <div class="article-title">{title}</div>
                <div class="article-desc">{description}</div>
                <div class="article-meta">🕐 {published}</div><br>
                <a class="article-link" href="{url}" target="_blank">Read full article →</a>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown('<div class="no-results">🗞️ No articles found. Try adjusting your filters.</div>', unsafe_allow_html=True)