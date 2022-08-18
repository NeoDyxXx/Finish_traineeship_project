create table visa_application_centre (
id 						serial primary key,
country_id 				int not null,
adress 					varchar(200),
email 					varchar(70),
apply_working_hours_1 	varchar(100),
issue_working_hours_2	varchar(100),
phone_number 			varchar(20),
foreign key(country_id) references country(id)
);