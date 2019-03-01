# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import pymongo
import Mars_Scraped
import os


app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/Mars_App'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database.
db = client.Mars_App


# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def index(): 

    # Find data
    App_info = dict(db.Mars_Data.__doc__)

    # Return template and data
    print(App_info)
    return render_template("index.html", mars_info=App_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 


    Mars_Scraped.scrape(update_db=True, update_scrape='All')

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)