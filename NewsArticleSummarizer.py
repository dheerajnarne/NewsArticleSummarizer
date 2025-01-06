import streamlit as st
from transformers import pipeline
import requests
import re

# Initialize the text summarization pipeline
pipe = pipeline("text2text-generation", model="dheerajnarne/textsummarizer", device=-1)

# Set the page configuration for Streamlit
st.set_page_config(
    page_title="News Summarizer",
    page_icon="🗞",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "This is a news summarization app built with Streamlit and Hugging Face Transformers."
    },
)

# Apply dark theme using custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e2f;
        color: #ffffff;
    }
    .stTextInput label, .stButton button {
        color: #ffffff;
    }
    .stButton button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to clean article content
def clean_content(content):
    if not content:
        return ""
    # Remove URLs, special characters, and unnecessary whitespace
    content = re.sub(r"http\S+|www\S+|https\S+", "", content, flags=re.MULTILINE)
    content = re.sub(r"[^\w\s.,]", "", content)
    return content.strip()

# Function to fetch news articles using NewsAPI
def fetch_news_articles(keyword):
    api_key = "6fb86e5265d340088783deb29eb146f5"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = [
            {
                "headline": article["title"],
                "link": article["url"],
                "content": clean_content(article.get("content") or article.get("description", ""))
            }
            for article in data.get("articles", [])[:5]  # Get top 5 articles
        ]
        return articles
    else:
        return []

# App title and description
st.title("🗞 News Summarizer")
st.markdown(
    """
    Welcome to the **News Summarizer**! Enter a topic below, and our app will fetch related news articles and summarize them for you.
    """
)

# Input keyword from the user
keyword = st.text_input(
    "Enter a topic or keyword:",
    placeholder="e.g., Indian economy, technology trends, climate change...",
)

# Fetch and summarize news on button click
if st.button("Fetch and Summarize News"):
    if keyword.strip():
        with st.spinner("Fetching news articles..."):
            articles = fetch_news_articles(keyword)

        if articles:
            st.markdown("### Top News Articles:")
            for i, article in enumerate(articles, 1):
                st.markdown(f"**{i}. {article['headline']}**")
                st.markdown(f"[Read more]({article['link']})")

                if article["content"] and len(article["content"]) > 100:  # Check if content is long enough
                    with st.spinner("Summarizing..."):
                        summary = pipe(
                            article["content"], 
                            max_length=150,  # Increased summary length
                            min_length=50,  # Minimum summary length
                            do_sample=False,
                            skip_special_tokens=True,
                        )[0]["generated_text"]
                    st.markdown(f"**Summary:** {summary}")
                else:
                    st.warning("Content is too short for summarization or no content available.")
        else:
            st.warning("No articles found for the given keyword.")
    else:
        st.warning("Please enter a keyword.")

# Footer
st.markdown("---")
st.markdown(
    "Developed by **Narne Dheeraj Balaram** using [Hugging Face Transformers](https://huggingface.co/) and [Streamlit](https://streamlit.io/)."
)
