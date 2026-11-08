
#arborescence
from pathlib import Path
RACINE = Path(__file__).resolve().parents[3]
print("La Racine es : ", RACINE)

#Import des fichier brut et clean 
FICHIER_BRUT = RACINE / "database" / "01_dirty_cafe_sales.csv"
FICHIER_CLEAN = RACINE / "database" / "02_dirty_cafe_clean_go_sql.csv"
#Packages 

import pandas as pd
import numpy as np


# Niveau 1 : explorer (sans rien modifier)

#importation de la base de donnees
df=pd.read_csv(FICHIER_BRUT)

#Combien de lignes et de colonnes contient le dataset ?
print("_"*80)
print(f"Le nombre de lignes : {df.shape[0]} est le nombre de colonne : {df.shape[1]} ")
print("_"*80)

#Quel est le type de chaque colonne ? Lesquelles sont mal typées et pourquoi ?
print("Le type de chaque colonne : ")
print(df.dtypes)    # type(str)
print("_"*80)
print(df.head())    # mal typées (Quantity ,Price Per Unit ,Total Spent, Transaction Date)
print("_"*80)       # Pourquoi (par ce que nous avons error , nan , Unknown)

#Combien de NaN par colonne, en nombre et en pourcentage ?
print(df.isna().sum())
print("_"*80)
print((df.isna().sum()/len(df)*100).round(1))
print("_"*80)

#Combien de valeurs ERROR et UNKNOWN par colonne ?
print("Le nombre de valeurs  ERROR et UNKNOWN par colonne : ")
print(df.isin(["ERROR","UNKNOWN"]).sum().sort_values(ascending=False))
print("_"*80)

#Quelle colonne est la plus « sale » une fois les faux NA comptés avec les vrais ?
vrai_Nan=df.isna().sum()
faux_Nan=df.isin(["ERROR","UNKNOWN"]).sum()
total_nan=vrai_Nan + faux_Nan
print(" La colonne la plus sale : ")
print(total_nan.sort_values(ascending=False))
print("_"*80)

#Quelles sont les valeurs uniques de Item, Payment Method et Location ?
print("Le contenue valeurs uniques de Item, Payment Method et Location: ")
print(df["Item"].value_counts(dropna=False)) #UNKNOWN : 344, NaN :333, ERROR :292
print("_"*80)
print(df["Payment Method"].value_counts(dropna=False)) #ERROR :306, UNKNOWN: 293, NaN :2579
print("_"*80)
print(df["Location"].value_counts(dropna=False)) #NaN :3265, ERROR: 358, UNKNOWN :338
print("_"*80)

#Quelle est la plage de dates ? Y a-t-il des dates impossibles ?
copy_col_date=pd.to_datetime(df["Transaction Date"],errors="coerce")
print("La plage de dates : ")
print("La plus petite date est : ")
print(copy_col_date.min()) #2023-01-01
print("La plus grande est de : ")
print(copy_col_date.max()) #2023-12-31
print("_"*80)
print("Le nombre total des dates avec des NAn et avec des UNKNOWN,ERROR :")
# Y a-t-il des dates impossibles ? : oui => "UNKNOWN","ERROR" soit 460
print(df["Transaction Date"].isna().sum() + df["Transaction Date"].isin(["UNKNOWN","ERROR"]).sum()) # 318
print("_"*80)

#-------------------Niveau 2--Nettoyage--------------------------
#Copie de la base
print("On copie la base dans une base pour effectuer le nettoyage : ")
df_clean=df.copy()
print(df_clean.shape)
print("Le nombre de vides :", (df_clean=="").sum())
print("_"*80)

#Remplacer ERROR, UNKNOWN et les chaînes vides par de vrais np.nan. 
#Vérifier que le nombre de NA a augmenté.
df_clean=df_clean.replace(["UNKNOWN","ERROR"],np.nan)
print("Le nombre des NaN : ")
print(df_clean.isna().sum())
NaN_avant=df.isna().sum()
NaN_apres=df_clean.isna().sum()
print("_"*80)
print("La difference entre les NaN df et df_clean : ")
mgr=pd.DataFrame({
    "debut" : df.isna().sum(),
    "fin" : df_clean.isna().sum()
})
mgr["diff"]=mgr["fin"]- mgr["debut"]
print(mgr)
print("_"*80)

#Q9. Convertir Quantity, Price Per Unit et Total Spent en numérique, et Transaction Date en date.
cols_numeric=df_clean[["Quantity","Price Per Unit","Total Spent"]]
for col in cols_numeric : 
    df_clean[col]=pd.to_numeric(df_clean[col], errors="coerce")
df_clean["Transaction Date"]=pd.to_datetime(df_clean["Transaction Date"], errors="coerce")
print(df_clean.dtypes)
print("_"*80)
print(df_clean.isna().sum())
print("_"*80)

#Q10. Y a-t-il des doublons complets ? Des Transaction ID en double ? Est-ce la même chose ?
print(df_clean.duplicated().sum()) # 0
print(df_clean["Transaction ID"].duplicated().sum()) # 0
print("_"*80)

#Q11. Y a-t-il des espaces ou des différences de casse cachés ?
s_avant=df_clean[["Item","Payment Method","Location"]]

for x in ["Item","Payment Method","Location"]:
    df_clean[x]=df_clean[x].str.strip()
s_apres=df_clean[["Item","Payment Method","Location"]]
print("La difference entre avant et apres : ")
print((s_avant != s_apres).sum())
print("_"*80)
print(((s_avant != s_apres) & s_avant.notna()).sum())

print("_"*80)
avant_casse=df_clean[["Item","Payment Method","Location"]].nunique()
print("Casse : ")
print(avant_casse)
print("_"*80)

print("Après_casse : ")
for col in ["Item","Payment Method","Location"] : 
    print(f"{col} : {df_clean[col].str.lower().nunique()}")
print("_"*80)

#Q12. Y a-t-il des valeurs négatives ou nulles dans Quantity, Price Per Unit et Total Spent ?
valeur_negative=df_clean[["Quantity","Price Per Unit","Total Spent"]]
for col in valeur_negative : 
    print(f"{col} : {(df_clean[col]<=0).sum()}")
print("_"*80)

#Q13. Quelles lignes n’ont pas de date ? Faut-il les garder ?
masque=df_clean["Transaction Date"].isna()
print(df_clean[masque].head())
print("_"*80)
print("les ligne qui n'on pas de dates : ")
print(df_clean[masque].shape[0])
masque_1=masque
masque_2=df_clean["Total Spent"].notna()
masque_combine=masque_1 & masque_2
print(masque_combine.sum())
print(df_clean[masque_combine].head())
print("_"*80)

#----------------------------------Niveau 3----Reconstruction et imputation (Q14 à Q22---

#Q14. Si Total Spent est manquant mais que Quantity et Price Per Unit sont connus, le recalculer.
print("le nombre de NaN avant le calcul dans la colonne Total Spent : ")
print(df_clean["Total Spent"].isna().sum())
print("_"*80)
recalcul_total_spent=(df_clean["Total Spent"].isna()
                      & df_clean["Quantity"].notna()
                      & df_clean["Price Per Unit"].notna())

# calcul 
df_clean.loc[recalcul_total_spent, "Total Spent"]= (
    df_clean.loc[recalcul_total_spent, "Quantity"] * df_clean.loc[recalcul_total_spent,"Price Per Unit"])
print ("Le nombre de NaN apres le calcul dans la colonne Total Spent : ")
print(df_clean["Total Spent"].isna().sum())
print("_"*80)
print(df_clean["Total Spent"].head())

#vérification
verif1=(df_clean["Total Spent"].isna() &
        (df_clean["Quantity"].isna() | df_clean["Price Per Unit"].isna())).sum()
print("_"*80)
print("Le nombre de NaN sur le lignes total spent est ")
print(verif1) # 502 à 40 tout ce qui pouvait etre reconstruite on été effectuée le reste est impossible
print("_"*80)

#-------Q15 : retrouver Price Per Unit par division

recalcul_Price_Per=(df_clean["Price Per Unit"].isna()
                    & df_clean["Quantity"].notna()
                    & df_clean["Total Spent"].notna())

df_clean.loc[recalcul_Price_Per, "Price Per Unit"] = (df_clean.loc[recalcul_Price_Per, "Total Spent"]
                                                      / df_clean.loc[recalcul_Price_Per, "Quantity"])
print("Le nombre de NaN remplacer est : ")
print(df_clean["Price Per Unit"].isna().sum())

#Vérification 
verif2=(df_clean["Price Per Unit"].isna() 
        & (df_clean["Quantity"].isna() | df_clean["Total Spent"].isna())).sum()
print(" Le nombre de NaN restant dans  la colonne Price Per Unit :",verif2)

print("_"*80)
#---Q16 : même chose pour Quantity
recalcul_Quantity=(df_clean["Quantity"].isna()
                   & df_clean["Price Per Unit"].notna()
                   & df_clean["Total Spent"].notna())

df_clean.loc[recalcul_Quantity, "Quantity"]=(df_clean.loc[recalcul_Quantity, "Total Spent"] /
                                             df_clean.loc[recalcul_Quantity, "Price Per Unit"])

print("Le nombre de NaN restant la colonne Quantity est : ")
print(df_clean["Quantity"].isna().sum())
print("_"*80)

#verifiactaion 
verif3=(df_clean["Quantity"].isna()
        & (df_clean["Price Per Unit"].isna() | df_clean["Total Spent"].isna())).sum()
print(verif3)
print("_"*80)

#Verifions si on a pas des decimal dans la colonne quantity 
masque3=((df_clean["Quantity"] % 1 !=0)
         & (df_clean["Quantity"].notna())).sum()
print(masque3)
print("_"*80)

#On vas convertir la colonne quantity en entier on utilise la fonction Int64 car presence des NaN 
df_clean["Quantity"]=df_clean["Quantity"].astype("Int64")
print("Le type de la colonne Quantity est : ", df_clean["Quantity"].dtypes)
print("Le nombre de NaN est : ", df_clean["Quantity"].isna().sum())
print("_"*80)

#Q17. Chaque Item a-t-il un prix unique ? Construire la table Item → Price. (en cours)
print("Le prix pour chaque produit : ")
print(df_clean.groupby("Item")["Price Per Unit"].unique())
print("_"*80)
print(df_clean.groupby("Item")["Price Per Unit"].agg(["min", "max", "nunique"]))
print("_"*80)

#Q18. Retrouver un Item manquant à partir du prix. Pour quels prix y a-t-il ambiguïté ?
dic_item={
    1.0: "Cookie", 2.0 : "Coffee",  5.0 : "Salad", 1.5: "Tea"       
}
item_nan=(df_clean["Item"].isna()
          & df_clean["Price Per Unit"].isin(dic_item.keys()))

df_clean.loc[item_nan, "Item"]=df_clean.loc[item_nan, "Price Per Unit"].map(dic_item)
print("Le nombre de item qui on été retouver par le price :", item_nan.sum())
print("Le nombre de nan restant dans Item : ", df_clean["Item"].isna().sum())

#Q19. Retrouver un Price Per Unit manquant à partir de l’Item.
dic_price={
    "Cookie":1.0,  "Coffee" : 2.0,  "Salad" : 5.0,"Tea" : 1.5 , 
    "Smoothie" :  4.0,  "Sandwich ":4.0 , "Juice"  :   3.0, "Cake" : 3.0
}
price_nan=(df_clean["Price Per Unit"].isna()
           & df_clean["Item"].isin(dic_price.keys()))
df_clean.loc[price_nan, "Price Per Unit"] = df_clean.loc[price_nan, "Item"].map(dic_price)

print("Le nombre de NaN qui ont été remplacer grâce a item : ", price_nan.sum())
print("Le nombre de NaN  restant dans la colonnes Price : ", df_clean["Price Per Unit"].isna().sum())
print("_"*80)
print(df_clean.isna().sum())

#Reconstruction du total par le Price Per Unit * Quantity 
masque_total_res=(df_clean["Total Spent"].isna()
                  & df_clean["Quantity"].notna()
                  & df_clean["Price Per Unit"].notna())
print("Le nombre de Nan dans Total Spent après la reconstruction : ")
print(masque_total_res.sum())

print("_"*80)
print("Passons a la reconstruction des 13 true (quantity * Price Per Unit : )")
df_clean.loc[masque_total_res, "Total Spent"]=(df_clean.loc[masque_total_res, "Quantity"] * 
                                    df_clean.loc[masque_total_res, "Price Per Unit"])
print("Les lignes restant est : ", df_clean["Total Spent"].isna().sum())
print("_"*80)

#Reconstruction de Quantity par le Total Spent 
masque_Quantity_res=(df_clean["Quantity"].isna()
                     & df_clean["Price Per Unit"].notna()
                     & df_clean["Total Spent"].notna())

df_clean.loc[masque_Quantity_res, "Quantity"]=(df_clean.loc[masque_Quantity_res, "Total Spent"]/
                                               df_clean.loc[masque_Quantity_res, "Price Per Unit"])
print("Le nombre de Nan qui n'on pas été remplacer dans la colonne Quantity est : ")
print(df_clean["Quantity"].isna().sum())

#Q20. Après toutes ces reconstructions, combien de NA restent par colonne ?
# Vérification 
print("_"*80)
print(df_clean.isna().sum())
print("_"*80)

#Q21. Pour les NA restants : mode, catégorie « Unknown » ou médiane ? Justifier chaque choix.
print("_"*80)
print("Les Statistique : ")
print(df_clean[["Quantity", "Total Spent"]].describe().round(3))

colonne_a_traiter=["Item", "Payment Method","Location"]
for col in colonne_a_traiter :
    df_clean[col]=df_clean[col].fillna("Unknown")

print("Le nombre de NaN restant : ")
print(df_clean.isna().sum())

print("_"*80)
#Nous allons compter combien de fois chaque produit apparaît dans une colonne avec la fonction values_count
print(df_clean["Item"].value_counts())
print(df_clean["Location"].value_counts())
print(df_clean["Payment Method"].value_counts())
print("_"*80)

#Q22. Vérifier la cohérence finale : Quantity × Price Per Unit == Total Spent. Combien d’exceptions ?

masque_test=(df_clean["Quantity"].notna()
             & df_clean["Price Per Unit"].notna()
             & df_clean["Total Spent"].notna())

masque_inc=(df_clean.loc[masque_test,"Quantity"] * df_clean.loc[masque_test,"Price Per Unit"] !=
            df_clean.loc[masque_test,"Total Spent"])

resultat1 = (masque_test).sum()
resultat2 = (masque_inc).sum()

print("Le resultat1 est :",resultat1, "et le resultat2 est : ", resultat2)
print("_"*80)

#Export du fichier nettoyé dans database
df_clean.to_csv(FICHIER_CLEAN, index=False )
#-----------------------------------------------------------------------------------------------------------
