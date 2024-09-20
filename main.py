from database import session
from models import Author, Book, Selection, Jury, Vote, Publisher

def afficher_livres_par_selection(selection_type):
    try:
        livres = session.query(Book).join(Selection, Book.id == Selection.id).filter(Selection.type == selection_type).all()
        if livres:
            for livre in livres:
                auteur = session.query(Author).filter(Author.id == livre.author_id).first()
                editeur = session.query(Publisher).filter(Publisher.id == livre.publisher_id).first()
                print(f"Titre: {livre.title}\nRésumé: {livre.summary}\nAuteur: {auteur.name if auteur else 'Auteur non trouvé'}\nÉditeur: {editeur.name if editeur else 'Éditeur non trouvé'}\nDate de parution: {livre.publication_date}\nNombre de pages: {livre.pages}\nISBN: {livre.isbn}\nPrix éditeur: {livre.publisher_price}\n")
        else:
            print(f"Aucun livre trouvé pour la sélection {selection_type}.")
    except Exception as e:
        print(f"Erreur lors de l'affichage des livres : {e}")

def ajouter_livre_a_selection(livre_id, selection_type):
    try:
        selection = Selection(date='2024-09-19', type=selection_type)  # Exemple de date, à ajuster
        session.add(selection)
        session.commit()
        print(f"Livre ID {livre_id} ajouté à la sélection {selection_type}.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du livre à la sélection : {e}")

def afficher_votes():
    try:
        votes = session.query(Vote).all()
        if votes:
            for vote in votes:
                livre = session.query(Book).filter(Book.id == vote.book_id).first()
                print(f"Livre: {livre.title if livre else 'Livre non trouvé'}, Votes: {vote.votes}")
        else:
            print("Aucun vote trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'affichage des votes : {e}")

def authentifier_membre(nom, role):
    try:
        membre = session.query(Jury).filter(Jury.name == nom, Jury.role == role).first()
        if membre:
            print(f"Authentification réussie pour {nom} avec le rôle {role}.")
            return membre
        else:
            print("Authentification échouée.")
            return None
    except Exception as e:
        print(f"Erreur lors de l'authentification : {e}")
        return None

def voter(membre_id, livre_id):
    try:
        vote = session.query(Vote).filter(Vote.book_id == livre_id, Vote.jury_member_id == membre_id).first()
        if vote:
            vote.votes += 1
        else:
            vote = Vote(book_id=livre_id, jury_member_id=membre_id, votes=1)
            session.add(vote)
        session.commit()
        print(f"Vote enregistré pour le livre ID {livre_id} par le membre ID {membre_id}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du vote : {e}")

def menu_principal():
    while True:
        print("Bienvenue au Prix Goncourt 2024")
        print("1. Utilisateur")
        print("2. Président du jury")
        print("3. Membre du jury")
        print("4. Quitter")
        choix = input("Veuillez sélectionner votre rôle (1/2/3/4) : ")

        if choix == '1':
            print("Vous avez choisi : Utilisateur")
            selection_type = input("Veuillez entrer le type de sélection à afficher (First/Second/Third) : ")
            afficher_livres_par_selection(selection_type)
        elif choix == '2':
            print("Vous avez choisi : Président du jury")
            nom = input("Veuillez entrer votre nom : ")
            role = 'President'  # Utilisation du rôle 'President'
            membre = authentifier_membre(nom, role)
            if membre:
                action = input("Que voulez-vous faire ? (afficher_livres/ajouter_livre/afficher_votes) : ")
                if action == 'afficher_livres':
                    selection_type = input("Veuillez entrer le type de sélection à afficher (First/Second/Third) : ")
                    afficher_livres_par_selection(selection_type)
                elif action == 'ajouter_livre':
                    livre_id = int(input("Veuillez entrer l'ID du livre à ajouter : "))
                    selection_type = input("Veuillez entrer le type de sélection (First/Second/Third) : ")
                    ajouter_livre_a_selection(livre_id, selection_type)
                elif action == 'afficher_votes':
                    afficher_votes()
                else:
                    print("Action non reconnue.")
            else:
                print("Authentification échouée.")
        elif choix == '3':
            print("Vous avez choisi : Membre du jury")
            nom = input("Veuillez entrer votre nom : ")
            role = 'Member'
            membre = authentifier_membre(nom, role)
            if membre:
                livre_id = int(input("Veuillez entrer l'ID du livre pour lequel vous voulez voter : "))
                voter(membre.id, livre_id)
            else:
                print("Authentification échouée.")
        elif choix == '4':
            print("Merci d'avoir utilisé le système. Au revoir !")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")

if __name__ == "__main__":
    menu_principal()
