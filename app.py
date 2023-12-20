from flask import Flask, render_template, request ,jsonify
import requests
import re

app = Flask(__name__)
nb = 6
btn_value="Show More"
disable = False

def getgames():
    global nb
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

    nb=6
    if nb > 36:
        nb = 36

    games_info = []
    games = getgames()
    games_info = getorderedgames(games)

    return render_template('index.html', games=games_info, disable=disable , btn_value=btn_value)





@app.route('/loadmore', methods=['POST'])
def loadmore():
    global btn_value
    global nb
    global disable

    nb = request.get_json().get('page_data')
    try:
        nb = int(nb)
    except ValueError:
        nb = 0
    nb += 6




    disable = (nb >= 36)
    if disable:
        nb = 36
        btn_value = "No More To Show"

    games = getgames()
    games_info = getorderedgames(games)
    dataReply = {
        'games': list(games_info),
        'disable': "disable",
        'btn_value': btn_value
    }
    print(jsonify(dataReply))
    return jsonify(dataReply)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080)

