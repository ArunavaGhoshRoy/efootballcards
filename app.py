from flask import Flask, render_template, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import requests
from bs4 import BeautifulSoup

uri = "mongodb+srv://arunavaghoshroy4:Sb9ugRXRHSuokZsB@cluster0.kjglago.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.pesdb

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/player', methods = ['POST'])
def player_post():
    url = request.form['url_give']
    rating = request.form['rating_give']
    comment = request.form['comment_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    description = soup.select_one('meta[name="description"]')['content']
    name = title.split(' -')[0]

    count = db.players.count_documents({})
    num = count + 1

    db.players.insert_one({
        'number':num,
        'image': image,
        'name': name,
        'description': description,
        'rating': rating,
        'comment': comment
    })
    return jsonify({'msg':'Player card saved!'})

@app.route("/delete", methods=["POST"])
def delete_card():
    num = request.form['num_give']
    db.players.delete_one({'number': int(num)})
    return jsonify({'msg': 'Player card deleted!'})

@app.route('/player', methods = ['GET'])
def player_get():
    player_list = list(db.players.find({}, {'_id':False}))
    return jsonify({'players':player_list})

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug=True)