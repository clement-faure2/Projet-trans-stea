import requests

base_url = "http://172.25.1.37:5007"

class JeuxB:
    def __init__(self, name, tag, image):
        self.name = name
        self.tag = tag
        self.image = image
    
    def add_gameB(self):
        data = {"name": self.name, "tag": self.tag, "image": self.image}
        response = requests.post(base_url + "/addB", json = data)
        if response.status_code == 200:
            print(response.json()["response"])

class JeuxM(JeuxB):
    def __init__(self, name, tag, image, price):
        super().__init__(name, tag, image)
        self.price = price
            
    def add_gameM(self):
        data = {"name": self.name, "tag": self.tag, "image": self.image, "price": self.price}
        response = requests.post(base_url + "/addM", json = data)
        if response.status_code == 200:
            print(response.json()["response"])

while(True):
    print("1.ajouter un jeu à la bibliothèque")
    print("2.ajouter un jeu au magasin")
    print("3.quitter")
    choice = input("Que choisissez vous ? ")
    if choice == "1":
        game = JeuxB(input("name: "), input("tag : "), input("image : "))
        game.add_gameB()
    if choice == "2":
        game = JeuxM(input("name: "), input("tag : "), input("image : "), float(input("price : ")))
        game.add_gameM()
    if choice == "3":
        break
                