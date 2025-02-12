import jsonpickle
import os

class Jeux_B:
    def __init__(self, name, tag, image):
        self.name = name
        self.tag = tag
        self.image = image

    def creer_jeux_B(self):
        if not os.path.exists("game_library.json"):
            with open("game_library.json", "w") as f:
                f.write(jsonpickle.encode([]))
        with open("game_library.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            liste.append(self)            
            with open("game_library.json","w") as f:
                f.write(jsonpickle.encode(liste))
                print(f"{self.name} à été ajouter avec succès")
    @staticmethod    
    def supprimer_jeux_B():
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
    @staticmethod
    def afficher_jeux_B():
        with open("game_library.json","r") as f:
                    retour = f.read()
                    liste = jsonpickle.decode(retour)
                    for game in liste:
                        print (f"{game.name}")
    @staticmethod
    def afficher_details_B():
        with open("game_library.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
        for index, game in enumerate(liste):
            print (f"{index + 1}. {game.name}")
        choix = int(input("afficher les détails : "))-1
        if 0 <= choix < len(liste): 
            print (liste[choix].name + " est un jeu " + liste[choix].tag)

class Jeux_M(Jeux_B):
    def __init__(self, name, tag, image, price):
        super().__init__(name, tag, image)
        self.price = price

    def creer_jeux_M(self): 
        if not os.path.exists("magasin.json"):
            with open("magasin.json", "w") as f:
                f.write(jsonpickle.encode([]))         
        with open("magasin.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            liste.append(self)            
            with open("magasin.json","w") as f:
                f.write(jsonpickle.encode(liste))
                print(f"{self.name} à été ajouter avec succès")
    @staticmethod    
    def supprimer_jeux_M():
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
    @staticmethod
    def afficher_jeux_M():
        with open("magasin.json","r") as f:
                    retour = f.read()
                    liste = jsonpickle.decode(retour)
                    for game in liste:
                        print (f"{game.name}")
    @staticmethod
    def afficher_details_M():
        with open("magasin.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
        for index, game in enumerate(liste):
            print (f"{index + 1}. {game.name}")
        choix = int(input("afficher les détails : "))-1
        if 0 <= choix < len(liste): 
            print (f"{liste[choix].name} est un jeu {liste[choix].tag} qui coutent {liste[choix].price}€")

    @staticmethod    
    def acheter_jeux():
        with open("magasin.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            for index, game in enumerate(liste):
                print (f"{index + 1}. {game.name} {game.price}")
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

while(True):
    print("1.Bibliothèque")
    print("2.Magasin")
    print("3.quitter")
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
            choice = input()

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
