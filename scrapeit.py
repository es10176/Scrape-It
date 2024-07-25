from flask import Flask, redirect, url_for, flash, render_template, session, request
from datetime import timedelta
from plyer import notification
import webbrowser
from bs4 import BeautifulSoup
import requests
import time

# You can change the end tags to whatever sources you want to receive in your web results.
end_tags_coding = [': GeeksforGeeks', ': Stack Overflow', ': W3 Schools']

# setting up the app
data_texts = []
data_links = []

app = Flask(__name__)
app.secret_key = "flask_key743"
app.permanent_session_lifetime = timedelta(days=5)

@app.route("/home", methods=['GET', 'POST'])
def home():
    notification.notify(
        title = 'ScrapeIt',
        message = 'Welcome to my webscraping project!',
        app_icon = None,
        timeout = 3,
    )
 
    if request.method == 'POST':
        URL = request.form['ui']

        try:
            response = requests.get(URL)
            response.raise_for_status()  # Raise an exception for non-200 response codes
            soup = BeautifulSoup(response.content, 'html.parser')

            show_data1 = None  # Initialize outside the loop
            lines = soup.find_all('p')

            scraped_data = [line.text.strip() for line in soup.find_all('p')]

            return render_template('result.html', scraped_data=scraped_data)
        except Exception as e:
            flash(f"An error occurred: {e}")
            return render_template('scrapeit_home.html')

    return render_template("scrapeit_home.html")


@app.route("/about")
def about():
    return render_template("scrapeit_about.html")


if __name__ == "__main__":
    app.run(debug=True)