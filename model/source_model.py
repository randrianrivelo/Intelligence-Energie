class SourceModel:
    def __init__(self, db):
        self.db = db

    def ajouter_source(self, nom):
        c = self.db.conn.cursor()
        c.execute("INSERT INTO Sources VALUES (NULL, ?)", (nom,))
        self.db.conn.commit()
