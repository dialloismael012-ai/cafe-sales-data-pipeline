--changer le Schema public => vers cafe
--create SCHEMA IF NOT EXISTS cafe ;

--Création des differentes tables 
CREATE TABLE IF NOT EXISTS cafe.cafe_dirty (

    id integer generated always as identity primary key,
    transaction_id varchar(20) not null unique,
    item varchar(20) not null,
    quantity integer null,
    price_per_unit numeric (6,2) null,
    total_spent numeric (6,2) null,
    payment_method varchar(20) not null,
    location varchar(20) not null,
    transaction_date date

);

