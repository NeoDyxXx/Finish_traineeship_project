create table appointment (
id 			serial primary key,
vac_id 		int not null,
subcat_id 	int not null,
date 		timestamp,
foreign key (vac_id) 	references visa_application_centre (id),
foreign key (subcat_id) references subcategory (id)
);