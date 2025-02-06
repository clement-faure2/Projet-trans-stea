import jsonpickle



class jeux:
    def __init__(self, name, tag, image):
        self.name = name
        self.tag = tag
        self.image = image

    def creer_jeux(self):
        with open("game_library.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            liste.append(self)            
            with open("game_library.json","w") as f:
                f.write(jsonpickle.encode(liste))
                print(f"{self.name} à été ajouter avec succès")
        
    def supprimer_jeux(self):
        with open("game_library.json","r") as f:
            retour = f.read()
            liste = jsonpickle.decode(retour)
            for index, game in enumerate(liste):
                print (f"{index + 1}. {game.name}")
            choix = int(input("choisis un jeu à supprimer : "))-1
            if 1 <= choix < len(liste): 
                name_supp = liste[choix]
                liste.remove(liste[choix])                
                with open("game_library.json","w") as f:
                    f.write(jsonpickle.encode(liste))
                print(f"{name_supp.name} à été supprimé avec succès")
            else:
                print("Choix invalide.")





while(True):
    print("1.Bibliothèque")
    print("2.Magasin")
    print("3.quitter")
    menu = input()
    if menu == "1":
        while(True):
            print("1.Créer un jeu")
            print("2.Supprimer un jeu")
            print("3.afficher la liste de tous les jeux")
            print("4.afficher le détail d'un jeu")
            print("5.quitter")
            choice = input()

            if choice == "1" :
                game = jeux(input("name : "), input("tag : "), input("image : "))
                game.creer_jeux()
                
            if choice == "2" :
                game = jeux("", "", "")
                game.supprimer_jeux()


            if choice == "3" :
                with open("game_library.json","r") as f:
                    retour = f.read()
                    liste = jsonpickle.decode(retour)
                    for i in liste:
                        print (i["name"])

            if choice == "4":
                with open("game_library.json","r") as f:
                    retour = f.read()
                    liste = jsonpickle.decode(retour)
                    for index, game in enumerate(liste):
                        print (index + 1, game["name"])
                    choix = int(input("afficher les détails : "))-1
                if 0 <= choix < len(liste): 
                    print (liste[choix]["name"] + " est un jeu " + liste[choix]["tag"] +" " + liste[choix]["image"])


            if choice == "5" :
                print("adieu")
                break
    if menu == "2":
        while(True):
            print("1.Créer un jeu")
            print("2.Supprimer un jeu")
            print("3.afficher la liste de tous les jeux")
            print("4.afficher le détail d'un jeu")
            print("5.")
            print("6.quitter")
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
                if 1 <= choix < len(liste): 
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

            if choice == "3" :
                with open("game_library.json","r") as f:
                    retour = f.read()
                    liste = jsonpickle.decode(retour)
                    for i in liste:
                        print (i["name"])

            if choice == "4":
                with open("game_library.json","r") as f:
                    retour = f.read()
                    liste = jsonpickle.decode(retour)
                    for index, game in enumerate(liste):
                        print (index + 1, game["name"])
                    choix = int(input("afficher les détails : "))-1
                if 0 <= choix < len(liste): 
                    print (liste[choix]["name"] + " est un jeu " + liste[choix]["tag"] +" " + liste[choix]["image"])


            if choice == "6" :
                print("adieu")
                break


    if menu == "3":
        print("adieu")
        break
