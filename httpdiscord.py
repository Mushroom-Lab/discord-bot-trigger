import hashlib
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_cors import CORS
import requests
import yaml
import os
import json
from bson.json_util import dumps, loads
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
#MONGODB_URI = os.environ['MONGODB_URI']
#COLLECTION = os.getenv("COLLECTION")
#DB_NAME = os.getenv("DATABASE_NAME")
#CERAMIC_BE = os.getenv("CERAMIC_BE")
#CERAMIC_BE_PORT = os.getenv("CERAMIC_BE_PORT")
#cluster = MongoClient(MONGODB_URI)
#levelling = cluster[COLLECTION][DB_NAME]

app = Flask(__name__)
CORS(app)

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
API_ENDPOINT = config['API_ENDPOINT']
# first get the channel_id of the dm
headers = {
    'Authorization': 'Bot {}'.format(DISCORD_TOKEN),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    
@app.route('/roleassign', methods=['POST'])
def roleassign():
    content = request.json
    print(content)
    user_id = content['user_id']
    role_id = content['role_id']
    guild_id = content['guild_id']
    r = requests.put('%s/guilds/%s/members/%s/roles/%s' % (API_ENDPOINT, guild_id, user_id, role_id), headers=headers)
    r.raise_for_status()
    return {'status': 0}

@app.route('/roleremove', methods=['POST'])
def roleremove():
    content = request.json
    print(content)
    user_id = content['user_id']
    role_id = content['role_id']
    guild_id = content['guild_id']
    r = requests.delete('%s/guilds/%s/members/%s/roles/%s' % (API_ENDPOINT, guild_id, user_id, role_id), headers=headers)
    r.raise_for_status()
    return {'status': 0}

# assume the dm is opened, otherwise it would fail
@app.route('/dm/<user_id>', methods=['POST'])
def dm(user_id):
    content = request.json
    data = json.dumps({"recipient_id":user_id})
    r = requests.post('%s/users/@me/channels' % (API_ENDPOINT), data=data, headers=headers)
    r.raise_for_status()
    channel_id = r.json()['id']
    
    content = json.dumps(content)
    r = requests.post('%s/channels/%s/messages' % (API_ENDPOINT, channel_id), data=content, headers=headers)
    r.raise_for_status()
    return r.json()
    

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=6666, ssl_context=('fullchain.pem', 'privkey.pem'))
    app.run(host='0.0.0.0', port=3334)
