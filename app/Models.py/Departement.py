

class Department:

    def __init__(self, row):

        self.id = row["id"]
        self.nom = row["nom"]
        self.batiment = row["batiment"]
        self.salle = row["salle"]
        self.code_interne = row["code_interne"] # Abréviation que l'on a en interne
