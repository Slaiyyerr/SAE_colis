

class Parcel:

    def __init__(self, row):
        self.id = row["id"]
        self.numero_suivi = row["numero_suivi"]
        self.order_id = row["order_id"]
        self.status = row["status"]
        self.location = row["location"]
        self.date_recu_iut = row["date_recu_iut"]
        self.date_recu_final = row["date_recu_final"]
        self.commentaires = row["commentaires"]
