

class  Orders:
    def __init__(self, row):
        self.id = row["id"]
        self.reference = row["reference"]
        self.supplier_id = row["supplier_id"]
        self.departement_id = row["departement_id"]
        self.demandeur = row["demandeur"]
        self.status = row["status"]
        self.date_livraison_prevu = row["date_livraison_prevu"]
        self.created_at = row["created_at"]