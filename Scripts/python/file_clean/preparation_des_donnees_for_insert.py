#Pckages
import pandas as pd

#Import depuis le fichier de nettoyage
from pathlib import Path
RACINE = Path(__file__).resolve().parents[3]
print("La Racine es : ", RACINE)
FICHIER_CLEAN = RACINE / "database" / "02_dirty_cafe_clean_go_sql.csv"
print("_"*80)

#-------------- The going to insert the data to database => Sql
#On vérifier l'etat du fichier et on crée une copie
print("_"*80)
print("Relecture du CSV exporté dans df_verif : ") 
df_verif=pd.read_csv(FICHIER_CLEAN)

#On verifier le nombre de colonnes et de lignes 
print(f"The nomber is rows is : {df_verif.shape[0]} and col is : {df_verif.shape[1]}")
print("_"*80)
print("The nomber NaN is : ", df_verif.isna().sum())
print("_"*80)

#Vérifions les types de colonnes 
print("Le type de chacune des colonnes est :  ")
print(df_verif.dtypes)

print("_"*89)
#On vas chercher a  adapter les noms des colonnes de la table qui à été  exporter a la table dans postgres
#Céation d'un dictionnaire 
print(df_verif.columns.tolist())
rename_col={'Transaction ID': 'transaction_id', 'Item' : 'item', 'Quantity' : 'quantity', 
            'Price Per Unit' : 'price_per_unit','Total Spent': 'total_spent','Payment Method' : 'payment_method',
             'Location' : 'location', 'Transaction Date'  : 'transaction_date' }

#On renome les noms des variables directement 
df_verif=df_verif.rename(columns=rename_col)
print("_"*89)
print("Les nom qui ont été renomer sont les suivants : ")
print(df_verif.columns.tolist())
print("_"*89)

#Changeons les types des colonnes 
print(df_verif.dtypes)
print("_"*89)
df_verif["quantity"]=pd.to_numeric(df_verif['quantity'], errors="coerce").astype('Int64')
df_verif['transaction_date']=pd.to_datetime(df_verif['transaction_date'], errors="coerce")

print("Vérification des types des colonnes : ")
print(df_verif.dtypes)
print("_"*89)
print("Le nombre de NaN est : ")
print(df_verif.isna().sum())
print("_"*89)

#--------df_pour_insertion_dans_sql----
print("La table à inserer dans la base MDF => in table cafe_dirty")
df_inserte=df_verif.copy()
print("_"*80)

#Affichons le chiffre d'affaires
print("Le Chiffre d'affaire : ", round(df_inserte["total_spent"].sum()))
print("_"*80)

print(df_inserte[df_inserte["item"] != "Unknown"].groupby("item")["quantity"].sum().sort_values(ascending=False))