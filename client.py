import requests

base_url = "http://192.168.0.15:5007"

class Jeux:
    def __init__(self, name, tag, image):
        self.name = name
        self.tag = tag
        self.image = image
    
    def add_game(self):
        data = {"name": self.name, "tag": self.tag, "image": self.image}
        response = requests.post(base_url + "/add", json = data)
        if response.status_code == 200:
            print(response.json()["response"])

    def del_game(self, index):

        response = requests.post(base_url + "/del")
        if response.status_code == 200:
            print(response.json()["response"])


choice = input("choisis")


if choice == "1":
    game = Jeux(input("name: "), input("tag : "), input("image : "))
    game.add_game()

if choice == "2":
    game = Jeux("", "", "")
    game.del_game()
    index = input("choisis un jeu: ")