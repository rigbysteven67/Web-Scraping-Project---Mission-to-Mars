from flask import Flask, render_template, redirect
import pymongo

#Instantiate Flask app
app = Flask(__name__)

# Setup splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

# connect to mongodb
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# connect to mars_app database
db = client.mars_app

# connect to mars collection
mars_coll = db.mars

@app.route("/")
def index():
    mars_data = mars_coll.find_one()
    return(render_template('index.html', mars_data = mars_data))
    
@app.route("/scrape")
def scrape():
    
    # this is the py script with all of the scraping functions
    import scrape_mars

    # gather document to insert
    nasa_document = scrape_mars.scrape_all()
    
    # insert
    #mars.insert_one(data_document)
    
    # upsert
    mars_coll.mars.update_one({}, {'$set': nasa_document}, upsert=True)
    
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)