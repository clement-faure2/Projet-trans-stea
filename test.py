from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Label

class FormApp(App):
    def compose(self) -> ComposeResult:
        yield Label("Entrez votre nom :")
        yield Input(placeholder="Nom", id="name_input")
        yield Button("Créer un jeu", id="submit_button_creejeu")
        yield Button("Supprimer un jeu", id="submit_button_suppjeu")
        yield Button("Afficher la liste de tous les jeux", id="submit_button_afficheliste")
        yield Button("Afficher le détail d'un jeu", id="submit_button_affichedetail")
        yield Button("Quitter", id="submit_button_quitter")
        yield Label("", id="result_label")

    def on_button_pressed(self, event) -> None:
        if event.button.id == "submit_button":
            name_input = self.query_one("#name_input", Input)
            result_label = self.query_one("#result_label", Label)
            result_label.update(f"Bonjour, {name_input.value} !")

if __name__ == "__main__":
    FormApp().run()

''' 
 print("1.Créer un jeu")
    print("2.Supprimer un jeu")
    print("3.afficher la liste de tous les jeux")
    print("4.afficher le détail d'un jeu")
    print("5.quitter")
'''