CREATE DATABASE IF NOT EXISTS weather;
USE weather;

DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE Users (
    user_id int4  AUTO_INCREMENT,
    email varchar(255) UNIQUE,
  CONSTRAINT users_pk PRIMARY KEY (user_id)
);


INSERT INTO Users (email) VALUES ('test@bu.edu');
INSERT INTO Users (email) VALUES ('test1@bu.edu');
