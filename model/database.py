import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect("data/energie.db")
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS sources(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE,
            description TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS equipements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            type TEXT NOT NULL,
            puissance_w REAL DEFAULT 0,
            statut TEXT DEFAULT 'Inactif',
            localisation TEXT,
            date_ajout TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS consommation(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipement_id INTEGER NOT NULL,
            valeur_kwh REAL NOT NULL,
            source TEXT,
            date_relevé TEXT,
            FOREIGN KEY(equipement_id) REFERENCES equipements(id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS alertes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            equipement_id INTEGER,
            message TEXT,
            date_creation TEXT,
            statut TEXT DEFAULT 'Active',
            FOREIGN KEY(equipement_id) REFERENCES equipements(id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS coupures(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipement_id INTEGER,
            date_debut TEXT,
            date_fin TEXT,
            durée_minutes INTEGER,
            raison TEXT,
            FOREIGN KEY(equipement_id) REFERENCES equipements(id)
        )
        """)

        self.conn.commit()

    def execute_query(self, query, params=()):
        """Exécuter une requête SELECT"""
        c = self.conn.cursor()
        c.execute(query, params)
        return c.fetchall()

    def execute_insert(self, query, params=()):
        """Exécuter une requête INSERT"""
        c = self.conn.cursor()
        c.execute(query, params)
        self.conn.commit()
        return c.lastrowid

    def execute_update(self, query, params=()):
        """Exécuter une requête UPDATE"""
        c = self.conn.cursor()
        c.execute(query, params)
        self.conn.commit()

    def execute_delete(self, query, params=()):
        """Exécuter une requête DELETE"""
        c = self.conn.cursor()
        c.execute(query, params)
        self.conn.commit()

    def close(self):
        """Fermer la connexion"""
        self.conn.close()
