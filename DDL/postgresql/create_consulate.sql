create table consulate (
id 				serial primary key,
country_id 		int not null,
adress 			varchar(200),
email 			varchar(70),
working_hours 	varchar(100),
phone_number_1 	varchar(20),
phone_number_2	varchar(20),
foreign key(country_id) references country(id)
);