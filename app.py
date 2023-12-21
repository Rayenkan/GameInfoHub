from flask import Flask, render_template, request, jsonify , abort
import requests
import re

from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/loadmore": {"origins": "http://127.0.0.1:8080"}})

nb = 6
btn_value="Show More"
disable = False

def getgames(nb):
    api_url = "https://api.rawg.io/api/games"

    params = {
        'key': 'e987444dc539477fb7d6dbf09a611868',
        'page_size': nb
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        game_data = response.json()
        return game_data.get("results")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def getorderedgames (games):
    games_info = []
    if games:
        for game_data in games:
            games_info.append({
                "name": game_data.get('name'),
                "platforms": [platform["platform"]["name"] for platform in game_data["platforms"]],
                "stores": [store["store"]["name"] for store in game_data["stores"]],
                "release_date": game_data.get('released'),
                "image_link": game_data.get('background_image'),
                "rating": game_data.get('rating'),
                "tags": [tag["name"] for tag in game_data["tags"] if re.match("^[a-zA-Z]", tag["name"])]
            })

        # Convert lists to strings

        for i in range(nb):
            games_info[i]["platforms"] = " ".join(games_info[i]["platforms"])
            games_info[i]["stores"] = " ".join(games_info[i]["stores"])
            games_info[i]["tags"] = " ".join(games_info[i]["tags"])

    return games_info
@app.route('/', methods=['GET'])
def index():

    global btn_value
    global nb
    global disable
    games = getgames(nb)
    games_info = getorderedgames(games)
    nb=len(games_info)
    nb=6
    return render_template('index.html', games=games_info)





@app.route('/loadmore', methods=['POST'])
def loadmore():
    global btn_value
    global nb
    global disable

    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        nb = data.get('page_data')

        try:
            nb = int(nb)
        except ValueError:
            nb = 0
        nb += 6


        games = getgames(nb)
        games_info = getorderedgames(games)

        dataReply = {
            'games': list(games_info),
            'disable': "disable",
            'btn_value': btn_value
        }

        return jsonify(dataReply)
    else:
        abort(415)  # Return Unsupported Media Type error
if __name__ == '__main__':
    app.run( debug=True , threaded=True, port=8080)

