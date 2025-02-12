from flask import Flask, request, jsonify 
import jsonpickle
import os

app = Flask(__name__)


@app.route("/", methods = ["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/add", methods=["POST"])
def add_J():
    if not os.path.exists("game_library.json"):
        with open("game_library.json", "w") as f:
            f.write(jsonpickle.encode([]))
    data = request.get_json()
    game = {"name": data.get("name"),"tag": data.get("tag"), "image": data.get("image")}
    with open("game_library.json", "r") as f:
        liste = jsonpickle.decode(f.read())
        liste.append(game)
    with open("game_library.json", "w") as f:
        f.write(jsonpickle.encode(liste))
    return jsonify({"response": f"{game["name"]} ajouté avec succès"}), 200

@app.route("/list", methods = ["GET"])
def list_game():
    with open("game_library.json","r") as f:
        liste = jsonpickle.decode(f.read())
    games = [{"index": index + 1, "name": game["name"], "tag": game["tag"], "image": game["image"]}
    for index , game in enumerate(liste)]
    return jsonify({"games": games}), 200

@app.route("/del", methods=["POST"])
def del_J():
    data = request.get_json()
    with open("game_library.json","r") as f:
        liste = jsonpickle.decode(f.read())
        if 1 <= data.get("index") <= len(liste): 
            name_supp = liste.pop(data.get("index") - 1)                
            with open("game_library.json","w") as f:
                    f.write(jsonpickle.encode(liste))
        return jsonify({"response": f"{name_supp["name"]} supprimé avec succès"}), 200

app.run(host="0.0.0.0", port=5007)