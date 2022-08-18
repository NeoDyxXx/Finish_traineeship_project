CREATE TABLE news(
        id SERIAL PRIMARY KEY,
        country_id INTEGER NOT NULL,
        news_id INTEGER NOT NULL,
        date TIMESTAMP);
CREATE TABLE country(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE news_details(
        id SERIAL PRIMARY KEY,
        title VARCHAR(70) NOT NULL,
        body VARCHAR(150) NOT NULL,
        link VARCHAR(70) NOT NULL);
CREATE TABLE consulate(
        id SERIAL PRIMARY KEY,
        country_id INTEGER NOT NULL,
        address VARCHAR(200) NOT NULL,
        email VARCHAR(70),
        working_hours VARCHAR(100),
        phone_number_1 VARCHAR(20),
        phone_number_2 VARCHAR(20));
CREATE TABLE visa_application_centre(
        id SERIAL PRIMARY KEY,
        country_id INTEGER NOT NULL,
        address VARCHAR(200) NOT NULL UNIQUE,
        email VARCHAR(70) UNIQUE,
        apply_working_hours VARCHAR(100),
        issue_working_hours VARCHAR(100),
        phone_number VARCHAR(20));
CREATE TABLE appointment(
        id SERIAL PRIMARY KEY,
        VAC_id INTEGER NOT NULL,
        date TIMESTAMP NOT NULL,
        subcat_id INTEGER);
CREATE TABLE sub_category(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        category_id INTEGER);
CREATE TABLE category(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE);
ALTER TABLE news ADD CONSTRAINT fk_country_id FOREIGN KEY (country_id) REFERENCES country (id) ON DELETE CASCADE,
ADD CONSTRAINT fk_news_id FOREIGN KEY (news_id) REFERENCES news_details (id) ON DELETE CASCADE;
ALTER TABLE consulate ADD CONSTRAINT fk_country_id FOREIGN KEY (country_id) REFERENCES country (id) ON DELETE CASCADE;
ALTER TABLE visa_application_centre ADD CONSTRAINT fk_country_id FOREIGN KEY (country_id) REFERENCES country (id) ON DELETE CASCADE;
ALTER TABLE appointment ADD CONSTRAINT fk_vac_id FOREIGN KEY (vac_id) REFERENCES visa_application_centre (id) ON DELETE CASCADE,
ADD CONSTRAINT fk_subcat_id FOREIGN KEY (subcat_id) REFERENCES sub_category (id) ON DELETE CASCADE;
ALTER TABLE sub_category ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES category (id) ON DELETE CASCADE;