from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)
nb = 9  # Initialize nb as a global variable

def getgames():
    global nb  # Declare nb as a global variable within the function
    api_url = "https://api.rawg.io/api/games"

    params = {
        'key': 'e987444dc539477fb7d6dbf09a611868',
        'page_size': nb  # Specify the number of games to retrieve
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        game_data = response.json()
        return game_data.get("results")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global nb  # Declare nb as a global variable within the function
    games_info = []

    if request.method == 'POST':
        if 'btn' in request.form:
            nb += 9
    disable = (nb >= 36)
    games = getgames()

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

    return render_template('index.html', games=games_info, disable=disable)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080)
