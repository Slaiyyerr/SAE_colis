

class Supplier:

    def __init__(self, row):
        self.id = row["id"]  # row prends la ligne en question dans la base
        self.nom = row["nom"]
        self.contact_interlocuteur = row["contact_interlocuteur"]
        self.numero = row["numero"]
        self.email = row["email"]
        self.notes = row["notes"]
