from flask import Flask, redirect, url_for, flash, render_template, session, request
from datetime import timedelta
from plyer import notification
import webbrowser
from bs4 import BeautifulSoup
import requests
import time
import json
import csv
import pickle

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

    return render_template("scrapeit_home.html")


@app.route("/search", methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        URL = request.form['ui']
        try:
            response = requests.get(URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            show_data1 = None
            lines = soup.find_all('p')

            scraped_data = [line.text.strip() for line in soup.find_all('p')]
            data_texts.append(scraped_data)

            return render_template('result.html', scraped_data=scraped_data)
        except Exception as e:
            flash(f"An error occurred: {e}")
            return render_template('scrapeit_home.html')

    return render_template("scrapeit_search.html")


@app.route("/export_data", methods=['POST', 'GET'])
def export_data():
    if request.method == 'POST': 

        button_name = request.form.get('button')
        if button_name == 'export_to_json':
            file_name = "scrape-it_data"
            
            with open(f"{file_name}.json", 'w') as json_file:
                         json.dump(data_texts, json_file)

            return render_template("success_export.html")
            
        elif button_name == 'export_to_csv':
             with open('scrape-it_data.csv', 'w', newline='') as csvfile:
                  csv_writer = csv.writer(csvfile)
                  csv_writer.writerows(data_texts)

             return render_template("success_export.html")
        
        else:
             file = open('scrape-it_data', 'wb')

             pickle.dump(data_texts, file)

             file.close()
             
             return render_template("success_export.html")


    return render_template("export_data.html")


@app.route("/about")
def about():
    pass

if __name__ == "__main__":
    app.run(debug=True)