CREATE TABLE movie_db.movies (movie_id INT PRIMARY KEY NOT NULL, title VARCHAR(255), release_date DATE);

# In order to use LOAD DATA "local-infile" and "loose-local-infile" params must be enabled in my.cnf.
LOAD DATA LOCAL INFILE '/var/lib/mysql-files/u.item'
INTO TABLE movie_db.movies
CHARACTER SET latin1
FIELDS TERMINATED BY '|'
(movie_id, title, @release_date)
SET release_date = STR_TO_DATE(@release_date, '%d-%M-%Y');