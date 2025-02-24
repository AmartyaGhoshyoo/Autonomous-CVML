from newsapi import NewsApiClient
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
import google.generativeai as genai
import streamlit as st
import os
import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Define the prompt for summarization
prompt = """
    You are an News Summarizer, You will be given news article with advertisement and other irrelevant content, you just have to summarize and write the news articles in more Effectively that can attract audience.
    You will be provided the URL in the sense of getting understand the main concept so that you can easily work on that topic from the whole input,
    Find the article above "End of Article" in the input
"""

# Function to get response from the model
def get_response(input, prompt, url):
    response = model.generate_content([prompt, url, input])
    return response._result.candidates[0].content.parts[0].text

# Function to fetch article content
def fetch_article_content(url):
    loader = UnstructuredURLLoader(urls=[url])
    data = loader.load()
    return data[0].page_content

# Function to fetch news articles
def news_fetching_article(query, start_date, sleep_interval):
    api_key = os.getenv('NEWS_API_KEY')
    newsapi = NewsApiClient(api_key)
    end_date = datetime.now().strftime('%Y-%m-%d')  # Current date

    all_articles = newsapi.get_everything(
        q=query,
        sources='the-times-of-india',
        domains='timesofindia.indiatimes.com',
        from_param=start_date,
        to=end_date,
        language='en',
        sort_by='publishedAt',
        page=1
    )
    sorted_articles = sorted(all_articles.get('articles', []), key=lambda x: x['publishedAt'])

    # Process articles from oldest to newest
    for article in sorted_articles:
        title = article['title']
        url = article['url']
        image_url = article.get('urlToImage', '')  # Get the image URL
        content = fetch_article_content(url)
        timestamp = article['publishedAt']
        response = get_response(content, prompt, url)

        # Display the article in Streamlit
        st.markdown(
            f"""
            <div style="
                border: 2px solid red;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
                margin-bottom: 20px;
            ">
                <h3 style="color: red;">📰 {title}</h3>
                <p style="color: black;">📅 Published At: {timestamp}</p>
                {f'<img src="{image_url}" style="width: 100%; border-radius: 10px; margin-bottom: 10px;">' if image_url else ''}
                <p style="color: red;">🔗 <a href="{url}" target="_blank">Read The Full Article</a></p>
                <b><p style="color: black;">📄 {response}</p></b>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(sleep_interval)

# Function to set background image
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    

# Streamlit app
def main():
    # Set background image
    set_background("https://www.shutterstock.com/image-photo/old-white-paper-background-blank-260nw-2352853257.jpg")  # Replace with your image URL

    st.title("📰 News Summarizer")

    # Sidebar for user preferences
    st.sidebar.header("User Preferences")
    news_source = st.sidebar.radio("Do you want news from State or Cities?", ("State", "City"))

    if news_source == "State":
        states = ["Uttar Pradesh", "Maharashtra", "Karnataka", "Odisha", "Tamil Nadu", "Delhi"]
        selected_state = st.sidebar.selectbox("Select a state", states)
        query = selected_state
    else:
        cities = ["Mumbai", "Bangalore", "Chennai", "Delhi", "Bhubaneswar", "Kolkata"]
        selected_city = st.sidebar.selectbox("Select a city", cities)
        query = selected_city

    # Date selection
    start_date = st.sidebar.date_input("Select start date (at least 4 days behind)", 
                                      value=datetime.now() - timedelta(days=4),
                                      min_value=datetime.now() - timedelta(days=30),
                                      max_value=datetime.now() - timedelta(days=4))

    # Time interval selection
    st.sidebar.header("Time Interval")
    time_interval = st.sidebar.selectbox("Select time interval Hour", [0.5, 1, 2, 3])
    sleep_interval = time_interval * 3600  # Convert hours to seconds

    # Fetch and display news articles
    if st.sidebar.button("Fetch News 🗞️"):
        st.write(f"Fetching news for {query} from {start_date}...")
        news_fetching_article(query, start_date.strftime('%Y-%m-%d'), sleep_interval)

if __name__ == "__main__":
    main()