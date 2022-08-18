create table news (
id 				serial primary key,
country_id 		int not null,
news_details_id int not null,
date 			timestamp,
foreign key (country_id) 		references country (id),
foreign key (news_details_id)	references news_details (id)
);