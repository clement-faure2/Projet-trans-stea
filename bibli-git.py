import jsonpickle
import os
import sqlite3
from flask import Flask, request, jsonify 

app = Flask(__name__)

@app.route("/addB", methods=["POST"])
def add_J_B():
    data = request.get_json()
    game = {"name": data.get("name"),"tag": data.get("tag"), "image": data.get("image")}
    if STORAGE_MODE == "json":
        if not os.path.exists("game_library.json"):
            with open("game_library.json", "w") as f:
                f.write(jsonpickle.encode([]))
        with open("game_library.json", "r") as f:
            liste = jsonpickle.decode(f.read())
            liste.append(game)
        with open("game_library.json", "w") as f:
            f.write(jsonpickle.encode(liste))
    else:
        db.insert_game_HTTP("game_library", game)      
    return jsonify({"response": f"{game["name"]} ajouté avec succès"}), 200    

@app.route("/addM", methods=["POST"])
def add_J_M():
    data = request.get_json()
    game = {"name": data.get("name"),"tag": data.get("tag"), "image": data.get("image"), "price": data.get("price")}
    if STORAGE_MODE == "json":
        if not os.path.exists("magasin.json"):
            with open("magasin.json", "w") as f:
                f.write(jsonpickle.encode([]))
        with open("magasin.json", "r") as f:
            liste = jsonpickle.decode(f.read())
            liste.append(game)
        with open("magasin.json", "w") as f:
            f.write(jsonpickle.encode(liste))
    else:
        db.insert_game_HTTP("magasin", game)      
    return jsonify({"response": f"{game["name"]} ajouté avec succès"}), 200    

class DatabaseManager:
    def __init__(self, db_name="games.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                tag TEXT,
                image TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS magasin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                tag TEXT,
                image TEXT,
                price REAL
            )
        """)
        self.conn.commit()

    def insert_game(self, table, game):
        self.cursor.execute(f"INSERT INTO {table} (name, tag, image) VALUES (?, ?, ?)", (game.name, game.tag, game.image))
        self.conn.commit()

    def insert_game_HTTP(self, table, game):
        self.cursor.execute(f"INSERT INTO {table} (name, tag, image) VALUES (?, ?, ?)", (game["name"], game["tag"], game["image"]))
        self.conn.commit()

    def insert_magasin_game(self, game):
        self.cursor.execute("INSERT INTO magasin (name, tag, image, price) VALUES (?, ?, ?, ?)", (game.name, game.tag, game.image, game.price))
        self.conn.commit()

    def get_all_games(self, table):
        self.cursor.execute(f"SELECT name FROM {table}")
        return [row[0] for row in self.cursor.fetchall()]

    def get_game_details(self, table, index):
        self.cursor.execute(f"SELECT name, tag , price FROM {table}")
        games = self.cursor.fetchall()
        return games[index] if 0 <= index < len(games) else None

    def delete_game(self, table, index):
        self.cursor.execute(f"SELECT id FROM {table}")
        ids = [row[0] for row in self.cursor.fetchall()]
        if 0 <= index < len(ids):
            self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (ids[index],))
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()

def initialize_storage():
    storage_mode = input("Choisissez le mode de sauvegarde (1: JSON, 2: SQLite) : ")
    return "sqlite" if storage_mode == "2" else "json"

STORAGE_MODE = initialize_storage()
db = DatabaseManager() if STORAGE_MODE == "sqlite" else None
class Jeux_B:
    def __init__(self, name, tag, image):
        self.name = name
        self.tag = tag
        self.image = image

    def creer_jeux_B(self):
        if STORAGE_MODE == "json":
            if not os.path.exists("game_library.json"):
                with open("game_library.json", "w") as f:
                    f.write(jsonpickle.encode([]))
            with open("game_library.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
                liste.append(self)            
                with open("game_library.json","w") as f:
                    f.write(jsonpickle.encode(liste))
        else:
            db.insert_game("game_library", self)      
        print(f"{self.name} à été ajouter avec succès")      
    @staticmethod    
    def supprimer_jeux_B():
        if STORAGE_MODE == "json":
            with open("game_library.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
                for index, game in enumerate(liste):
                    print (f"{index + 1}. {game.name}")
                choix = int(input("choisis un jeu à supprimer : "))-1
                if 0 <= choix < len(liste): 
                    name_supp = liste.pop(choix)                
                    with open("game_library.json","w") as f:
                        f.write(jsonpickle.encode(liste))
                    print(f"{name_supp.name} à été supprimé avec succès")
                else:
                    print("Choix invalide.")
        else:            
            library_games = db.get_all_games("game_library")
            for index, game in enumerate(library_games):
                print(f"{index + 1}. {game}")
            choix = int(input("choisis un jeu à supprimer : "))-1
            if 0 <= choix < len(library_games): 
                details = db.get_game_details("game_library", choix)
                if details:
                    db.delete_game("game_library", choix)
                    print(f"{details[0]} à été supprimé avec succès")
            else:
                print("Choix invalide.")
    @staticmethod
    def afficher_jeux_B():
        if STORAGE_MODE == "json":
            with open("game_library.json", "r") as f:
                liste = jsonpickle.decode(f.read())
                for game in liste:
                    print(game.name)
        else:
            for game in db.get_all_games("game_library"):
                print(game)

    @staticmethod
    def afficher_details_B():
        if STORAGE_MODE == "json":
            with open("game_library.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
            for index, game in enumerate(liste):
                print (f"{index + 1}. {game.name}")
            choix = int(input("choisis un jeu pour afficher ces détails : "))-1
            if 0 <= choix < len(liste): 
                print (liste[choix].name + " est un jeu " + liste[choix].tag)
        else:
            library_games = db.get_all_games("game_library")
            for index, game in enumerate(library_games):
                print(f"{index + 1}. {game}")
            choix = int(input("choisis un jeu pour afficher ces détails : "))-1
            if 0 <= choix < len(library_games): 
                details = db.get_game_details("game_library", choix)
                if details:
                    db.get_game_details("game_library", choix)
                    print(f"{details[0]} est un jeu {details[1]}")


class Jeux_M(Jeux_B):
    def __init__(self, name, tag, image, price):
        super().__init__(name, tag, image)
        self.price = price

    def creer_jeux_M(self):
        if STORAGE_MODE == "json":
            if not os.path.exists("magasin.json"):
                with open("magasin.json", "w") as f:
                    f.write(jsonpickle.encode([]))         
            with open("magasin.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
                liste.append(self)            
                with open("magasin.json","w") as f:
                    f.write(jsonpickle.encode(liste))
        else:
            db.insert_magasin_game(self)
        print(f"{self.name} à été ajouter avec succès")
    @staticmethod    
    def supprimer_jeux_M():
        if STORAGE_MODE == "json":
            with open("magasin.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
                for index, game in enumerate(liste):
                    print (f"{index + 1}. {game.name}")
                choix = int(input("choisis un jeu à supprimer : "))-1
                if 0 <= choix < len(liste): 
                    name_supp = liste.pop(choix)                
                    with open("magasin.json","w") as f:
                        f.write(jsonpickle.encode(liste))
                    print(f"{name_supp.name} à été supprimé avec succès")
                else:
                    print("Choix invalide.")
        else:
            magasin_games = db.get_all_games("magasin")
            for index, game in enumerate(magasin_games):
                print(f"{index + 1}. {game}")
            choix = int(input("choisis un jeu à supprimer : "))-1
            if 0 <= choix < len(magasin_games): 
                details = db.get_game_details("magasin", choix)
                if details:
                    name_supp = Jeux_B(details[0], details[1], "Image par défaut") 
                    db.delete_game("magasin", choix)
                    print(f"{details[0]} à été supprimé avec succès")
            else:
                print("Choix invalide.")
    @staticmethod
    def afficher_jeux_M():
        if STORAGE_MODE == "json":
            with open("magasin.json", "r") as f:
                liste = jsonpickle.decode(f.read())
                for game in liste:
                    print(game.name)
        else:
            for game in db.get_all_games("magasin"):
                print(game)

    @staticmethod
    def afficher_details_M():
        if STORAGE_MODE == "json":
            with open("magasin.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
            for index, game in enumerate(liste):
                print (f"{index + 1}. {game.name}")
            choix = int(input("afficher les détails : "))-1
            if 0 <= choix < len(liste): 
                print (f"{liste[choix].name}  est un jeu  {liste[choix].tag} qui coutent {liste[choix].price}€")
        else:
            magasin_games = db.get_all_games("magasin")
            for index, game in enumerate(magasin_games):
                print(f"{index + 1}. {game}")
            choix = int(input("choisis un jeu pour afficher ces détails : "))-1
            if 0 <= choix < len(magasin_games): 
                details = db.get_game_details("magasin", choix)
                if details:
                    db.get_game_details("magasin", choix)
                    print(f"{details[0]} est un jeu {details[1]} qui coûtent {details[2]} €")
    @staticmethod    
    def acheter_jeux():
        if STORAGE_MODE == "json":
            with open("magasin.json","r") as f:
                retour = f.read()
                liste = jsonpickle.decode(retour)
                for index, game in enumerate(liste):
                    print (f"{index + 1}. {game.name} {game.price}€")
                choix = int(input("quelle jeu voulez vous acheter : "))-1
                if 0 <= choix < len(liste):  
                    with open("game_library.json","r") as f:
                        retour = f.read()
                        library = jsonpickle.decode(retour)
                        library.append(liste[choix])             
                    with open("game_library.json","w") as f:
                        f.write(jsonpickle.encode(library))
                    print(f"{game.name} à été acheté avec succès")
                else:
                    print("Choix invalide.")
        else:  
            magasin_games = db.get_all_games("magasin")
            for index, game in enumerate(magasin_games):
                print(f"{index + 1}. {game}")
            choix = int(input("Quel jeu voulez-vous acheter : ")) - 1
            if 0 <= choix < len(magasin_games):
                details = db.get_game_details("magasin", choix)
                if details:
                    new_game = Jeux_B(details[0], details[1], "Image par défaut") 
                    db.insert_game("magasin", new_game)
                    print(f"{details[0]} a été acheté avec succès")
            else:
                print("Choix invalide.")
while(True):
    print("1.Bibliothèque")
    print("2.Magasin")
    print("3.quitter")
    print("4.HTTP")
    menu = input("Que choisissez vous ? ")
    if menu == "1":
        while(True):
            print("1.Créer un jeu")
            print("2.Supprimer un jeu")
            print("3.afficher la liste de tous les jeux")
            print("4.afficher le détail d'un jeu")
            print("5.quitter")
            choice = input("Que voulez vous faire ? ")

            if choice == "1" :
                game = Jeux_B(input("name : "), input("tag : "), input("image : "))
                game.creer_jeux_B()
                
            if choice == "2" :
                Jeux_B.supprimer_jeux_B()


            if choice == "3" :
                Jeux_B.afficher_jeux_B()

            if choice == "4":
                Jeux_B.afficher_details_B()


            if choice == "5" :
                print("au revoir")
                break
    if menu == "2":
        while(True):
            print("1.Créer un jeu")
            print("2.Supprimer un jeu")
            print("3.afficher la liste de tous les jeux")
            print("4.afficher le détail d'un jeu")
            print("5.acheter un jeu")
            print("6.quitter")
            choice = input("Que voulez vous faire ? ")

            if choice == "1" :
                game = Jeux_M(input("name : "), input("tag : "), input("image : "), float(input("price : ")))
                game.creer_jeux_M()
            if choice == "2" :
                Jeux_M.supprimer_jeux_M()

            if choice == "3" :
                Jeux_M.afficher_jeux_M()

            if choice == "4":
                Jeux_M.afficher_details_M()

            if choice == "5":
                Jeux_M.acheter_jeux()

            if choice == "6" :
                print("au revoir")
                break


    if menu == "3":
        print("au revoir")
        break

    if menu == "4":
        app.run(host="0.0.0.0", port=5007)