"""Package DAO (Data Access Objects).

Contient les classes d'acces aux donnees.
Chaque DAO correspond a une table de la base de donnees.

Pattern utilise :
- Chaque methode ouvre un cursor, execute la requete, et le ferme
- Les transactions sont validees avec db.commit() ou annulees avec db.rollback()
- Les resultats sont convertis en objets Model
"""
