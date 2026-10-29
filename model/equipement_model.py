class EquipementModel:
    def __init__(self, db):
        self.db = db

    def ajouter_equipement(self, nom, type_e):
        c = self.db.conn.cursor()
        c.execute("INSERT INTO Equipements VALUES (NULL, ?, ?)", (nom, type_e))
        self.db.conn.commit()
