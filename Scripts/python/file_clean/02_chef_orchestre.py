#Chef d'orchestre
from sqlalchemy import create_engine

#Import for password
import getpass #Demander le mot de passe
#Dans un cadre ou nous @ ou d'autres caractère spécial dans le mdp (eviter que l'url se coupe)
from urllib.parse import quote_plus #encode

#Source de données à inserer
from preparation_des_donnees_for_insert import df_inserte

#Préparation de la connexion 
utilisateur='postgres'
hote='localhost'
port='5432'
base='MDF'

#Stock du Mdp
mot_de_passe=getpass.getpass('Enter password : ')#Demander le mot de passe
mot_de_passe_encode=quote_plus(mot_de_passe)


#Assemble pour former l'URL 
url=f"postgresql+psycopg2://{utilisateur}:{mot_de_passe_encode}@{hote}:{port}/{base}"
#moteur 
engine=create_engine(url)

#Lançons la connexion 
with engine.connect() as conn:
    print("Connexion is succufull")


#Verifiaction
print("_"*90)
print(f"Vérification rows : {df_inserte.shape[0]}, And  col :{df_inserte.shape[1]}")
print("_"*90)
print(f"Le Nbre de NaN : {df_inserte.isna().sum()}")
print("_"*90)


#Insertion 
df_inserte.to_sql(
    'cafe_dirty',
    engine,
    schema='cafe',
    if_exists="append",
    index=False
)

print("L'ingestion des data en Bacht est terminée : ")
