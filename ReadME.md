
# News Summarizer

This web application allows users to input a keyword, fetches related news articles using the NewsAPI, and summarizes them using a fine-tuned FLAN-T5 model through Hugging Face Transformers.

## 🖼️ Project Architecture

![Architecture Diagram](path/to/your/image.png) <!-- Replace with actual image path -->

```mermaid
graph TD
  A[User enters keyword on frontend] --> B[Flask receives POST request]
  B --> C[Flask calls NewsAPI to fetch articles]
  C --> D{Are articles found?}
  D -- No --> E[Show error: No articles found]
  D -- Yes --> F[Loop through articles]
  F --> G{Content length > 100?}
  G -- No --> H[Show: Content too short for summarization]
  G -- Yes --> I[Pass content to Hugging Face summarization model]
  I --> J[Receive summarized text]
  J --> K[Display summary + article metadata in UI]
  K --> L[User clicks link to view full article optional]
  style A fill:#f9f,stroke:#333,stroke-width:1px
  style I fill:#bbf,stroke:#333,stroke-width:1px
  style J fill:#bfb,stroke:#333,stroke-width:1px
  style K fill:#ff9,stroke:#333,stroke-width:1px
```

## 🛠️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Summarization**: FLAN-T5 (Fine-tuned using Hugging Face Transformers)
- **News API**: NewsAPI.org
- **Data Preprocessing**: Custom cleaning pipeline

## 🚀 How to Run

### Prerequisites

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the App

```bash
python app.py
```

Then, open `http://localhost:5000` in your browser.

## 🧪 Future Improvements

- Add user login and summary history
- Support summarization in multiple languages
- Allow export of summaries (PDF, DOCX, etc.)
- Integrate more summarization models (BART, T5)

