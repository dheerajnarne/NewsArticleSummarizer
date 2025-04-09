import os
from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer
import requests
import re
import torch
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import warnings

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configuration
NEWS_API_KEY = # Use your own tokens
HF_TOKEN =   # Use your own tokens
MODEL_NAME = "dheerajnarne/textsummarizer"
DEVICE = 0 if torch.cuda.is_available() else -1

# Suppress warnings
warnings.filterwarnings("ignore", message="You set `add_prefix_space`")
warnings.filterwarnings("ignore", message="The following `model_kwargs`")

def initialize_model():
    """Initialize the text summarization pipeline with proper error handling"""
    try:
        # Initialize tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            use_fast=True,
            token=HF_TOKEN
        )
        
        # Initialize model with corrected parameters
        model = pipeline(
            task="text2text-generation",
            model=MODEL_NAME,
            tokenizer=tokenizer,
            device=DEVICE,
            token=HF_TOKEN,
            truncation=True
        )
        print("✓ Model loaded successfully")
        return model, True
        
    except Exception as e:
        print(f"Failed to load model: {str(e)}")
        return None, False

# Initialize model
pipe, MODEL_LOADED = initialize_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if not keyword:
            return render_template('index.html', 
                                error="Please enter a keyword",
                                model_available=MODEL_LOADED)
        
        articles = fetch_news_articles(keyword)
        if not articles:
            return render_template('index.html', 
                                error="No articles found for the given keyword",
                                model_available=MODEL_LOADED)
        
        # Summarize articles
        for article in articles:
            if article["content"] and len(article["content"]) > 100:
                article["summary"] = summarize_text(article["content"])
        
        return render_template('index.html', 
                            articles=articles, 
                            keyword=keyword,
                            model_available=MODEL_LOADED)
    
    return render_template('index.html', model_available=MODEL_LOADED)

def fetch_news_articles(keyword):
    """Fetch news articles from NewsAPI"""
    try:
        params = {
            'q': keyword,
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': NEWS_API_KEY,
            'pageSize': 5
        }
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params=params,
            timeout=15
        )
        response.raise_for_status()
        
        data = response.json()
        return [{
            "headline": article["title"],
            "link": article["url"],
            "content": clean_content(article.get("content") or article.get("description", "")),
            "source": article.get("source", {}).get("name", "Unknown"),
            "publishedAt": format_date(article.get("publishedAt", ""))
        } for article in data.get("articles", [])]
    
    except Exception as e:
        print(f"NewsAPI Error: {str(e)}")
        return []

def summarize_text(text):
    """Generate summary using the loaded model"""
    if not MODEL_LOADED or not pipe:
        return None
    
    try:
        result = pipe(
            text,
            max_length=150,
            min_length=50,
            do_sample=False,
            truncation=True
        )
        return result[0]["generated_text"]
    except Exception as e:
        print(f"Summarization Error: {str(e)}")
        return None

def clean_content(content):
    """Clean article content"""
    if not content:
        return ""
    content = re.sub(r"http\S+|www\S+|https\S+", "", content, flags=re.MULTILINE)
    content = re.sub(r"[^\w\s.,\-']", "", content)
    return re.sub(r"\s+", " ", content).strip()

def format_date(date_str):
    """Format date string"""
    from datetime import datetime
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y at %H:%M")
    except:
        return date_str

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
