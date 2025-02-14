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
            print("6.jouer à un jeu")
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



            if choice == "6" :
                from turtle import *
                from random import choice
                import time
                from random import randint

                ROUGE = "\033[31m"
                JAUNE = "\033[33m"
                VERT = "\033[32m"
                RESET = "\033[0m"
                while(True):
                    print("1.wordle")
                    print("2.morpion")
                    print("3.blackjack")
                    print("4.quitter")
                    print("5.juste prix")

                    choix = input("choisis un jeu : ")


                    if choix == "1":
                        valeurs = ["maison", "chien", "legume", "fruits", "ordinateur", "chaise", "table"]
                        le_mot = choice(valeurs)
                        print(f"Le mot fait {len(le_mot)} caractères")
                        input("Appuyez sur Entrée pour démarrer ⏳")
                        
                        debut = time.time()
                        
                        while True:
                            resultat = ""
                            mot = input("Proposez un mot ou quittez avec 0 : ").lower()
                        
                            if mot == "0":
                                print("Partie terminée.")
                                break
                            
                            if len(mot) != len(le_mot):
                                print(f"Le mot doit contenir {len(le_mot)} caractères")
                                continue
                            
                            if mot == le_mot:
                                for i, lettre in enumerate(mot):
                                    if lettre == le_mot[i]:
                                        resultat += VERT + lettre + RESET
                                print(resultat)
                                print("Bravo, vous avez trouvé le mot 🎉")
                        
                                input("Appuyez sur Entrée pour arrêter le chrono ⏸️")
                                fin = time.time()
                                temps_ecoule = round(fin - debut, 2)
                                print(f"⏱️ Temps écoulé : {temps_ecoule} secondes")
                                break
                            else:
                                for i, lettre in enumerate(mot):
                                    if lettre == le_mot[i]:
                                        resultat += VERT + lettre + RESET
                                    elif lettre in le_mot:
                                        resultat += JAUNE + lettre + RESET
                                    else:
                                        resultat += ROUGE + lettre + RESET
                        
                            print(resultat)
                            if le_mot == mot:
                                break
                    if choix == "2":
                        speed(0)
                        pensize(3)

                        for x in [-50, 50]:
                            up()
                            goto(x, 150)
                            down()
                            goto(x, -150)

                        for y in [-50, 50]:
                            up()
                            goto(-150, y)
                            down()
                            goto(150, y)
                        def cercle():
                            up()
                            rt(90)
                            fd(40)
                            lt(90)
                            down()
                            circle(40)
                        def croix():
                            rt(45)
                            fd(50)
                            bk(50)
                            for i in range(3):
                                lt(90)            
                                fd(50)
                                bk(50)           
                            rt(45)
                        positions = {
                    "7": (-100, 100), "8": (0, 100), "9": (100, 100),
                    "4": (-100, 0),   "5": (0, 0),   "6": (100, 0),
                    "1": (-100, -100),"2": (0, -100),"3": (100, -100)}
                        victoire = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["1", "4", "7"], ["2", "5", "8"], ["3", "6", "9"], ["1", "5", "9"], ["3", "5", "7"]]
                        board = {key: None for key in positions}
                        def gagnant():
                            for combinaison in victoire:
                                if board[combinaison[0]] and board[combinaison[0]] == board[combinaison[1]] == board[combinaison[2]]:
                                    return board[combinaison[0]]
                            return None
                        while(True):
                            hideturtle()
                            choice_O = input("placez un cercle (1-9) ou quittez avec 10 : ")
                            if choice_O in positions and board[choice_O] is None:
                                up()
                                goto(positions[choice_O])
                                down()
                                cercle()      
                                board[choice_O] = 'O'
                                if gagnant() :
                                    print (f"Les {board[choice_O]} ont gagné")
                                    break
                                elif all(value is not None for value in board.values()):
                                    print ( "match nul")
                                    break
                            elif choice_O == "10":
                                break
                            else :
                                print("Choix invalide ou case déjà occupée. Essaie encore.")

                            choice_X = input("placez une croix (1-9) ou quittez avec 10 : ")
                            if choice_X in positions and board[choice_X] is None:
                                up()
                                goto(positions[choice_X])
                                down()
                                croix()    
                                board[choice_X] = 'X'
                                if gagnant() :
                                    print (f"Les {board[choice_X]} ont gagné")
                                    break
                                elif all(value is not None for value in board.values()):
                                    print ( "match nul")
                                    break
                            elif choice_X == "10":
                                break
                            else : 
                                print("Choix invalide ou case déjà occupée. Essaie encore.")
                        done()
                    if choix == "3":
                    
                        valeurs = {
                            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                            "J": 10, "Q": 10, "K": 10, "A": 11  
                        }

                        def calculer_total(main):
                            total = sum(valeurs[carte] for carte in main)
                            as_count = main.count("A")
                            while total > 21 and as_count:
                                total -= 10
                                as_count -= 1
                            return total

                        mainjoueur = [choice(list(valeurs.keys())), choice(list(valeurs.keys()))]
                        maincroupier = [choice(list(valeurs.keys())), choice(list(valeurs.keys()))]

                        print(f'🧑🃏 Vos deux cartes sont : {mainjoueur[0]} et {mainjoueur[1]}')
                        print(f'🤵‍♂️🃏 Une des cartes du croupier est : {maincroupier[0]}')

                        totalmainjoueur = calculer_total(mainjoueur)
                        totalmaincroupier = calculer_total(maincroupier)

                        while totalmainjoueur < 21:
                            print('Que voulez-vous faire :')
                            print('1 : Tirer')
                            print('2 : Rester')
                            tirerourester = int(input('Rentrez le chiffre de votre choix : '))

                            if tirerourester == 1:
                                nouvelle_carte = choice(list(valeurs.keys()))
                                mainjoueur.append(nouvelle_carte)
                                print(f'🃏 Votre nouvelle carte est : {nouvelle_carte}')
                                time.sleep(3)
                                print(f'🧑🃏 Vos cartes sont maintenant : {mainjoueur}')
                                totalmainjoueur = calculer_total(mainjoueur)
                                time.sleep(3)
                                print(f'🧑🃏 Le total de vos cartes est : {totalmainjoueur}')
                            else:
                                print('Vous passez votre tour')
                                break
                            
                        if totalmainjoueur > 21:
                            print('💥 Vous avez dépassé 21 ! Vous perdez 😢')
                            exit()

                        print(f'🤵‍♂️🃏 Les deux cartes du croupier sont : {maincroupier[0]} et {maincroupier[1]}')
                        time.sleep(3)
                        while totalmaincroupier < 17:
                            nouvelle_carte = choice(list(valeurs.keys()))
                            maincroupier.append(nouvelle_carte)
                            totalmaincroupier = calculer_total(maincroupier)
                            print(f'🤵‍♂️🃏 Le croupier tire : {nouvelle_carte}')
                            time.sleep(3)
                            print(f'🤵‍♂️🃏 La main total du croupier est : {totalmaincroupier}')

                        if totalmaincroupier > 21:
                            time.sleep(3)
                            print('🎉 Le croupier a dépassé 21, vous avez gagnez !')
                        elif totalmainjoueur > totalmaincroupier:
                            time.sleep(3)
                            print('🎉 Vous avez gagnez !')
                        elif totalmainjoueur < totalmaincroupier:
                            time.sleep(3)
                            print('😢 Le croupier a gagné.')
                            time.sleep(3)
                        else:
                            print('😐 Égalité !')



                    if choix == "4":
                        break

                    if choix == "5":
                        print('1: Facile    🟩')
                        print('2: Moyen     🟧')
                        print('3: Difficile 🟥')
                        ChoixDiffiPrix = int(input('quel est le numéro de ta difficulté ?'))
                        if ChoixDiffiPrix == 1:
                            print('Vous avez choisi Le Juste Prix 💰 en mode Facile 🟩')
                            print('✨🎮Bon Jeu🎮✨')
                            input("Appuyez sur Entrée pour démarrer ⏳")
                            debut = time.time()
                            prix = randint(10, 100)
                            choix = int(input('quel est le prix ?'))
                            while choix != prix:
                            
                                if choix < prix:
                                    print('Votre estimation est trop basse')
                    
                                else:
                                    print('Votre estimation est trop haute')
                    
                                choix = int(input('quel est la nouvelle estimation ?'))
                        
                        if ChoixDiffiPrix == 2:
                            print('Vous avez choisi Le Juste Prix 💰 en mode Moyen 🟧 ')
                            print('✨🎮Bon Jeu🎮✨')
                            input("Appuyez sur Entrée pour démarrer ⏳")
                            debut = time.time()
                            prix = randint(10, 1000)
                            choix = int(input('quel est le prix ?'))
                            while choix != prix:
                            
                                if choix < prix:
                                    print('Votre estimation est trop basse')
                    
                                else:
                                    print('Votre estimation est trop haute')
                    
                                choix = int(input('quel est la nouvelle estimation ?'))
                        
                        if ChoixDiffiPrix == 3:
                            print('Vous avez choisi Le Juste Prix 💰 en mode Difficile 🟥 ')
                            print('✨🎮Bon Jeu🎮✨')
                            input("Appuyez sur Entrée pour démarrer ⏳")
                            debut = time.time()
                            prix = randint(10, 10000)
                            choix = int(input('quel est le prix ?'))
                            while choix != prix:
                            
                                if choix < prix:
                                    print('Votre estimation est trop basse')
                    
                                else:
                                    print('Votre estimation est trop haute')
                    
                                choix = int(input('quel est la nouvelle estimation ?'))
                    
                        print('Bravo vous avez trouver le juste prix 🎉')
                        input("Appuyez sur Entrée pour arrêter le chrono ⏸️")
                        fin = time.time()
                        temps_ecoule = round(fin - debut, 2)
                        print(f"⏱️ Temps écoulé : {temps_ecoule} secondes")

                    

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