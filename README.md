News Summarizer 📢

# Please enable the Light Theme in Streamlit by clicking on the three-dot menu in the top-right corner, selecting Settings, and choosing Light Theme under the Theme section

A News Summarizer built with Streamlit, NewsAPI, and Google Generative AI (Gemini). This application fetches news articles from Times of India, extracts relevant content, and summarizes it to provide a more engaging and concise version for readers.

🚀 Features

Fetch news articles based on State or City using Newsapi.org.

Summarizes the articles using Gemini 1.5 Flash.

Extracts only relevant content, filtering out advertisements and distractions.

Displays articles with title, timestamp, image, link, and summary.

Responsive UI with a background image and easy navigation.

🛠️ Setup Instructions

1️⃣ Clone the Repository

    git clone https://github.com/your-username/news-summarizer.git
    cd AI Hackathon

2️⃣ Install Dependencies

Ensure you have Python 3.8+ installed. Then, install the required dependencies:

    pip install -r requirements.txt

3️⃣ Set Up Environment Variables

Create a .env file in the root directory and add the following:

GOOGLE_API_KEY=your_google_gemini_api_key
NEWS_API_KEY=your_newsapi_key

Replace your_google_gemini_api_key and your_newsapi_key with actual API keys.

🔧 Running the Application

Once the setup is complete, run the application using:

    streamlit run app.py

This will launch the Streamlit app in your browser at http://localhost:8501/.

📦 Deployment

1️⃣ Deploy on Streamlit Cloud

Push your project to GitHub.

Sign in to Streamlit Cloud.

Select your repository and deploy.

📝 License

This project is licensed under the MIT License.

🤝 Contribution

Feel free to open issues or submit pull requests to improve this project.

✨ Happy Summarizing! 🚀