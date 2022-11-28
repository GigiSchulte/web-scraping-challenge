from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrapeMars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    #access info from database
    mars_data = mongo.db.marsData.find_one()
    #print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #reference to database collection
    marsTable = mongo.db.marsData

    #drop table if exists
    mongo.db.marsData.drop()

    #call scrape mars script
    mars_data = scrapeMars.scrape_all()
    
    #load dict into mongodb
    marsTable.insert_one(mars_data)

    return redirect("/")

if __name__ == "__main__":
    app.run()