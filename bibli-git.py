import jsonpickle
import sqlite3

#partie bd
conn = sqlite3.connect('jeux.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Jeux")
cur.execute("""CREATE TABLE Jeux (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
        tag TEXT
        image TEXT)
        """)
conn.close()

cur.execute("INSERT INTO Jeux(id, name, tag, image) VALUES ('bla', 'elden ring', 15)")
conn.commit()
conn.close()
#1ere partie
while(True):
    print("1.Créer un jeu")
    print("2.Supprimer un jeu")
    print("3.afficher la liste de tous les jeux")
    print("4.afficher le détail d'un jeu")
    print("5.quitter")
    choice = input()

    if choice == "1" :
        liste = []
        name = input("name : ")
        tag = input("tag : ")
        image = input("image : ")
        game = {"name": name, "tag": tag, "image": image}
        with open("game_library.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            liste.append(game)
        encoded_game = jsonpickle.encode(liste)
        with open("game_library.json","w") as f:
            f.write(encoded_game)
        print(game["name"] + "à été ajouté avec succès")
    if choice == "2" :
        with open("game_library.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            for index, game in enumerate(liste):
                print (index + 1, game["name"])
            choix = int(input("choisis un jeu à supprimer : "))-1
        if 0 <= choix < len(liste): 
            with open("game_library.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
                liste.remove(liste[choix])
            encoded_game = jsonpickle.encode(liste)
            with open("game_library.json","w") as f:
                f.write(encoded_game)
            print(game["name"] + "à été supprimé avec succès")
        else:
            print("Choix invalide.")
            

    if choice == "5" :
        print("adieu")
        break

