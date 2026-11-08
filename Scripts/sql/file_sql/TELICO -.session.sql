----------------------Début d'Analyse des données sur SQL-----------------------------

--We go to insert a data
select * from cafe.cafe_dirty;

--On compte le nombre de lignes par colonnes 
select count(*) from cafe.cafe_dirty;

--On vas compte les null
select 
    count(*) - count(quantity) as Nbre_NULL_Q,
    count(*) - count(price_per_unit) as Nbre_NULL_P,
    count(*) - count(total_spent) as Nbre_Null_T,
    count(*) - count(transaction_date) as Nbre_Null_D
from cafe.cafe_dirty;

--Affichons le montant total 
select round(sum(total_spent), 0) from cafe.cafe_dirty;

--Les Nulls
SELECT * 
from cafe.cafe_dirty
where total_spent IS NULL AND location = 'Unknown';

---------------------------Niveau 1----------------------

--Combien de valeurs distinctes par item, payment_method, location ?
SELECT 
count (DISTINCT item) as Nbre_item, 
count (DISTINCT payment_method) as Nbre_payment,
count(DISTINCT location) as Nbre_location
FROM cafe.cafe_dirty
;

--le chiffre d’affaires par produit-------
SELECT item,
sum(total_spent) as Ca 
FROM cafe.cafe_dirty
WHERE item != 'Unknown'
GROUP BY item
ORDER BY Ca DESC
;

---Question 3 : les quantités vendues par produit
SELECT item, 
sum (quantity) as qte_vendue
FROM cafe.cafe_dirty
WHERE item != 'Unknown'
GROUP BY item
ORDER BY qte_vendue DESC;

--les 10 plus grosses transactions
SELECT transaction_id, total_spent, item
FROM cafe.cafe_dirty
WHERE total_spent IS NOT NULL
ORDER BY total_spent DESC, transaction_id
LIMIT 10
;

--Nous allons chercher le nombre de ticket qui => total_spent à 25
SELECT item, count(*) as Nbre_Items
FROM cafe.cafe_dirty
WHERE total_spent = '25'
GROUP BY item
ORDER BY Nbre_Items DESC
;

--Nous avons salad = 268 qui on un ticket = 25£ et Unknown = 1
--Nous allons voir la quantity et le price_per_unit s'il y'a un prix
--Rep : Nous avons trouver que Unknown a une qté null et Price null 
-- On vas cherche le reconstruire en se fiant a nos propos intuition 
-- sachant que seuls les salad on un total = 25£ donc Unknown correspond à salad
-- vus qu'il sont que deux a s'afficher une fois que la requêtte est lancer. 
SELECT * 
FROM cafe.cafe_dirty
WHERE total_spent = '25' AND item = 'Unknown'
;
--le UPDATE
UPDATE cafe.cafe_dirty
SET quantity = 5 , price_per_unit = 5, item = 'Salad'
WHERE transaction_id = 'TXN_7376255'
;

--Vérification
SELECT item,
count(*) as Nbre_Items,
sum (total_spent) as Ca
FROM cafe.cafe_dirty
WHERE item = 'Salad'
GROUP BY item
ORDER BY Nbre_Items DESC
;

--les transactions sans date 

SELECT 
count(transaction_id) as Nbre_tran,
sum (total_spent) as CA_total
FROM cafe.cafe_dirty
WHERE transaction_date IS NULL
;

-----------Niveau 2 ------------

--le CA par produit et par lieu
SELECT item,location,
sum (total_spent) as CA
FROM cafe.cafe_dirty
GROUP BY item,location
ORDER BY CA DESC
;
