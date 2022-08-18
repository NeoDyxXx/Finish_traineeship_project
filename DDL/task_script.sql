create table country (
        id 		serial primary key,
        name 	varchar(50) unique not null
);

insert into country values (0, 'spain');

create table news_details (
        id 		serial primary key,
        title 	varchar(70),
        body 	varchar(150),
        link 	varchar(100)
);

create table news (
        id 				serial primary key,
        country_id 		int not null,
        news_details_id int not null,
        date 			timestamp,
        foreign key (country_id) 		references country (id),
        foreign key (news_details_id)	references news_details (id)
);

create type news_t as (description text, image text, sourceName varchar(100), time text, title text, url text);

CREATE OR REPLACE FUNCTION select_from_json (doc text)
RETURNS TABLE (title varchar(70), body varchar(150), link varchar(100), date timestamp) AS
$BODY$ 
        select substring(title for 70)::varchar(70) as title, concat(substring(description for 147), '...')::varchar(150) as body, substring(url for 100)::varchar(100) as link, 
        to_timestamp(concat(substring(time for 10), ' ', substring(time from 14 for 19)), 'dd.mm.yyyy hh24:mi') as date from json_populate_recordset(null::news_t, doc::json)
$BODY$
LANGUAGE 'sql';

create or replace procedure insert_data(doc text)
LANGUAGE plpgsql
AS $BODY$
DECLARE
    curr cursor for select * from select_from_json(doc);
    i_nd int;
    i_n int;
    id_country int;
    counter int;

    title_t varchar(70);
    body_t varchar(150);
    link_t varchar(100);
    date_t timestamp;
BEGIN
    open curr;
    select COALESCE(max(id), 0) into i_nd from news_details;
    i_nd := i_nd + 1;

    select COALESCE(max(id), 0) into i_n from news;
    i_n := i_n + 1;

    select id into id_country from country where name = 'spain';

    loop
        fetch curr into title_t, body_t, link_t, date_t;
        IF NOT FOUND THEN EXIT; END IF;

        select count(*) into counter from news_details
        where title = title_t;

        IF counter > 0 then
            begin
                update news_details set body = body_t, link = link_t
                where title = title_t;
            end;
        else
            begin
                insert into news_details values(i_nd, title_t, body_t, link_t);
                insert into news values(i_n, id_country, i_nd, date_t);
            end;
        end if;

        i_n := i_n + 1;
        i_nd := i_nd + 1;
    end loop;

    close curr;
END;
$BODY$;