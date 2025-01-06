# News Summarizer

**News Summarizer** is a simple web application built with **Streamlit** and powered by the **Hugging Face Transformers** library. The app fetches the latest news articles related to a keyword entered by the user and provides summaries for each article.

This project uses a fine-tuned model based on the T5 architecture, specifically the `dheerajnarne/textsummarizer` model, which can be found [here](https://github.com/dheerajnarne/TextSummarizerUsingT5-small).

## Features

- **Fetch Latest News:** Enter a topic or keyword, and the app will fetch the most recent articles related to that topic.
- **Summarize Articles:** The app automatically summarizes the content of each article using a fine-tuned summarization model.
- **Dark Mode:** The app features a dark theme for better readability.
- **Link to Original Articles:** You can click the title of each article to read the full story.

## Requirements

To run this project locally, ensure you have the following dependencies:

- Python 3.x
- Streamlit
- Hugging Face Transformers
- Requests
- Re

You can install the required dependencies by running:

```bash
pip install streamlit transformers requests
```

How to Use
Clone the repository or download the source code.
Set up the NewsAPI key by signing up at NewsAPI and replacing the api_key variable in the app.py file with your own key.
Run the Streamlit app:

```bash
streamlit run app.py
```

Open the application in your browser. Enter a keyword or topic in the search bar to fetch news articles. Click the "Fetch and Summarize News" button to get summarized articles.
## How It Works

- **News Fetching:** The app uses the NewsAPI to fetch news articles based on the keyword provided by the user. It retrieves the top 5 articles and extracts their titles, descriptions, and content.
- **Content Cleaning:** The content is cleaned to remove URLs, special characters, and unnecessary whitespace for better summarization.
- **Summarization:** The content of each article is summarized using a fine-tuned **T5-based model** (`dheerajnarne/textsummarizer`). The model generates concise summaries of the articles.
- **Display:** The app displays the summarized version of the articles along with links to the full articles.

## Model Used

- The summarization model used in this application is a fine-tuned version of the **T5 (Text-to-Text Transfer Transformer)** model.
- The fine-tuning was done on a dataset specifically designed for text summarization tasks.


## Example
Input:
Keyword: "Indian economy"

Output:

Headline: "India’s economy set for major growth despite global challenges"
Summary: "India's economy continues to grow despite challenges from the global market. The government has implemented various reforms to promote economic stability and development."

Headline: "Indian GDP expected to reach new highs by 2025"
Summary: "Experts predict that India's GDP will hit new milestones in the next few years due to ongoing industrialization and growth in key sectors like technology and manufacturing."

License
