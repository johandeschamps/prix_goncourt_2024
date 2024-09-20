"""
Ce module définit les classes de base de données pour un système de gestion de prix littéraire
utilisant SQLAlchemy.

Classes:
    MainCharacter: Représente les personnages principaux dans un livre.
    Jury: Représente les membres du jury.
    Publisher: Représente une maison d'édition.
    Selection: Représente une sélection de livres pour le prix.
    Book: Représente un livre.
    Vote: Représente un vote d'un membre du jury pour un livre.
    Author: Représente un auteur.

Configuration de la base de données:
    Crée une connexion à la base de données MySQL et initialise les tables définies.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DECIMAL, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class MainCharacter(Base):
    __tablename__ = 'maincharacter'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'))

class Jury(Base):
    __tablename__ = 'jury'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    role = Column(Enum('president', 'member'))

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))

class Selection(Base):
    __tablename__ = 'selection'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    type = Column(Enum('First', 'Second', 'Third'))

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    publication_date = Column(Date)
    pages = Column(Integer)
    isbn = Column(String(13))
    publisher_price = Column(DECIMAL(10, 2))
    author_id = Column(Integer, ForeignKey('author.id'))
    publisher_id = Column(Integer, ForeignKey('publisher.id'))

class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    jury_member_id = Column(Integer, ForeignKey('jury.id'))
    votes = Column(Integer)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    biography = Column(Text)

# Configuration de la base de données
engine = create_engine('mysql+mysqlconnector://johand:prixgoncourt@127.0.0.1/prix_goncourt_2024')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
