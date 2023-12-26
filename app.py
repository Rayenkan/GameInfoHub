from flask import Flask, render_template, request, jsonify , abort
import requests
import re
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
nb = 6

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


def search_games_by_name(game_name):
    api_url = "https://api.rawg.io/api/games"

    params = {
        'key': 'e987444dc539477fb7d6dbf09a611868',
        'search': game_name
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        results = response.json().get("results")

        if results:
            first_game_data = results[0]

            game_info = {
                "name": first_game_data.get('name'),
                "platforms": [platform["platform"]["name"] for platform in first_game_data["platforms"]],
                "stores": [store["store"]["name"] for store in first_game_data["stores"]],
                "release_date": first_game_data.get('released'),
                "image_link": first_game_data.get('background_image'),
                "rating": first_game_data.get('rating'),
                "tags": [tag["name"] for tag in first_game_data["tags"] if re.match("^[a-zA-Z]", tag["name"])]
            }
            game_info["platforms"] = " ".join(game_info["platforms"])
            game_info["stores"] = " ".join(game_info["stores"])
            game_info["tags"] = " ".join(game_info["tags"])

            return [game_info]  # 
        else:
            return None
    else:
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


        for i in range(nb):
            games_info[i]["platforms"] = " ".join(games_info[i]["platforms"])
            games_info[i]["stores"] = " ".join(games_info[i]["stores"])
            games_info[i]["tags"] = " ".join(games_info[i]["tags"])

    return games_info
@app.route('/', methods=['GET'])
def index():

    global nb
    games = getgames(nb)
    games_info = getorderedgames(games)
    nb=len(games_info)
    nb=6
    return render_template('index.html', games=games_info)





@app.route('/loadmore', methods=['POST'])
def loadmore():
    global nb

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
        }

        return jsonify(dataReply)
    else:
        abort(415)  # Return Unsupported Media Type error

@app.route('/search', methods=["POST"])
def search():
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        game_name = data.get('page_data')  # Correctly accessing the 'page_data' key
        response = search_games_by_name(game_name)

        if response is not None:
            return jsonify(response)
        else:
            # Handle the case when the search function returns None (e.g., no results or an error)
            return jsonify({"error": "No results found"})
    else:
        # Handle the case when the request is not in JSON format
        return jsonify({"error": "Invalid request format"})


if __name__ == '__main__':
    app.run( debug=True , threaded=True, port=8080)

