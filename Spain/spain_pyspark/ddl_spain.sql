CREATE TABLE IF NOT EXISTS Country (
Id SERIAL PRIMARY KEY,
Name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Consulate (
Id SERIAL PRIMARY KEY,
Country_id INTEGER,
Address VARCHAR(200),
Email VARCHAR(70),
Working_hours VARCHAR(100),
Phone_number_1 VARCHAR(20),
Phone_number_2 VARCHAR(20),
FOREIGN KEY (Country_id) REFERENCES Country (Id)
);

CREATE TABLE IF NOT EXISTS Visa_Application_Centre (
Id SERIAL PRIMARY KEY,
Country_id INTEGER,
Address VARCHAR(200),
Email VARCHAR(70),
Apply_working_hours VARCHAR(100),
Issue_working_hours VARCHAR(100),
Phone_number VARCHAR(20),
FOREIGN KEY (Country_id) REFERENCES Country (Id)
);

CREATE TABLE IF NOT EXISTS News_details (
Id SERIAL PRIMARY KEY,
Title VARCHAR(70),
Body VARCHAR(150),
Link VARCHAR(70)
);

CREATE TABLE IF NOT EXISTS News (
Id SERIAL PRIMARY KEY,
Country_id INTEGER,
News_id INTEGER,
Date timestamp,
FOREIGN KEY (Country_id) REFERENCES Country (id),
FOREIGN KEY (News_id) REFERENCES News_details (Id)
);