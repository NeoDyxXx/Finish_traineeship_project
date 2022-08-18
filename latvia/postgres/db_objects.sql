CREATE TABLE IF NOT EXISTS COUNTRY (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) 
);

CREATE TABLE IF NOT EXISTS CONSULATE (
    ID SERIAL PRIMARY KEY,
    COUNTRY_ID INTEGER REFERENCES COUNTRY (ID),
    ADRESS VARCHAR(200) ,
    EMAIL VARCHAR(70) ,
    WORKING_HOURS VARCHAR(100),
    PHONE_NUMBER_1 VARCHAR(20) ,
    PHONE_NUMBER_2 VARCHAR(20) 
  );

CREATE TABLE IF NOT EXISTS VISA_APPLICATION_CENTRE (
    ID SERIAL PRIMARY KEY,
    COUNTRY_ID INTEGER REFERENCES COUNTRY (ID),
    ADRESS VARCHAR(200),
    EMAIL VARCHAR(70),
    APPLY_WORKING_HOURS_1 VARCHAR(100),
    ISSUE_WORKING_HOURS_2 VARCHAR(100),
    PHONE_NUMBER VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS NEWS_DETAILS (
    ID SERIAL PRIMARY KEY,
    TITLE VARCHAR(70),
    BODY VARCHAR(150),
    LINK VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS NEWS (
    ID SERIAL PRIMARY KEY ,
    COUNTRY_ID INTEGER REFERENCES COUNTRY (ID),
    NEWS_ID INTEGER REFERENCES NEWS_DETAILS (ID),
    DATE timestamp
);

CREATE TABLE IF NOT EXISTS CATEGORY (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS SUB_CATEGORY (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50),
    CATEGORY_ID INT REFERENCES CATEGORY (ID)
);

CREATE TABLE IF NOT EXISTS APPOINTMENT (
    ID SERIAL PRIMARY KEY,
    VAC_ID INT REFERENCES VISA_APPLICATION_CENTRE (ID),
    SUBCAT_ID INT REFERENCES SUB_CATEGORY (ID),
    DATE TIMESTAMP
);