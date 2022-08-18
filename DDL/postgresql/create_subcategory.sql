create table subcategory (
id 			serial primary key,
name 		varchar(50) unique not null,
category_id int not null,
foreign key (category_id) references category (id)
);