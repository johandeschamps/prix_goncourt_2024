"""
Ce module configure la connexion à la base de données et initialise les tables définies dans le modèle.

Modules importés:
    create_engine (sqlalchemy): Crée une instance de moteur pour la base de données.
    sessionmaker (sqlalchemy.orm): Crée une classe de session configurée.
    Base (models): Classe de base pour les modèles SQLAlchemy.

Configuration de la base de données:
    Crée une connexion à la base de données MySQL et initialise les tables définies dans le modèle.
    Crée une session pour interagir avec la base de données.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configuration de la base de données
engine = create_engine('mysql+mysqlconnector://johand:prixgoncourt@127.0.0.1/prix_goncourt_2024')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
