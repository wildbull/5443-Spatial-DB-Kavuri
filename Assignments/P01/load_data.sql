create extension if not exists postgis;
DROP table IF EXISTS ufo;


CREATE TABLE ufo

(Date varchar,Country varchar,City varchar,State varchar, Shape varchar,Summary varchar,lat	float,lon float);


COPY ufo FROM 'C:\Users\Public\ufo_data.csv' WITH  (HEADER TRUE,FORMAT csv ) ;

CREATE INDEX index_all ON ufo (name,lat,lon);

alter table ufo add column distance geometry; 

Update ufo SET distance= ST_Point(lon, lat);



select * from ufo;
