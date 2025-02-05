print("hello world")

import jsonpickle

while(True):
    print("1.Créer un jeu")
    print("2.Supprimer un jeu")
    print("3.afficher la liste de toos les jeux")
    print("4.afficher le détail d'un jeu")
    print("5.quitter")
    choice = input()

    if choice == "1" :
        liste = []
        name = input("name : ")
        tag = input("tag : ")
        image = input("image : ")
        game = {"name : ": name, "tag : ": tag, "image : ": image}
        with open("game_library.json","r") as f:
            retour = f.read()
            decoded_retour = jsonpickle.decode(retour)
            liste.append(decoded_retour)
        encoded_game = jsonpickle.encode(liste)
        with open("game_library.json","w") as f:
            f.write(encoded_game)

    if choice == "5" :
        print("adieu")
        break
