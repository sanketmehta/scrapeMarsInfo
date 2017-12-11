import marsdata as md
import datetime as dt
import numpy as np
import pandas as pd
import pymongo
import pprint


from flask import Flask, render_template, jsonify, redirect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Default Route#
@app.route("/")
def welcome():
    conn = "mongodb://test:test@ds243335.mlab.com:43335/heroku_smxwwn9d"
    client = pymongo.MongoClient(conn)

    db = client.heroku_smxwwn9d
    mars_collection = db.mars_collection

    for record in db.mars_collection.find().sort('time', 1):
        last_record = record

    title_list, url_list = [], []

    for k,v in last_record.items():
        if(k == '_id'):
            pass
        else:
            if(k == 'df_mars'):
                mars_facts = pd.read_json(v).to_html()
            if(k == 'hemisphere_image_urls'):
                for x in v:
                    title_list.append(x['title'])
                    url_list.append(x['img_url'])

    return render_template("index.html", results=last_record, results2=mars_facts, results3=title_list, results4=url_list)

#Route for Scraping latest data#
@app.route("/scrape")
def scrape1():
    conn = "mongodb://test:test@ds243335.mlab.com:43335/heroku_smxwwn9d"
    client = pymongo.MongoClient(conn)

    db = client.heroku_smxwwn9d
    mars_collection = db.mars_collection

    res1 = md.scrape()
    mars_collection.insert_one(res1)

    return redirect("http://localhost:5000/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
