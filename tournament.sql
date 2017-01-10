-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE Matches;
DROP TABLE Players;
DROP SEQUENCE user_id_seq;

CREATE SEQUENCE user_id_seq;

CREATE TABLE Players (
	player_id int DEFAULT NEXTVAL('user_id_seq'),
	player_fname varchar(20),
	player_lname varchar(20),
	wins int DEFAULT 0,
	matches int DEFAULT 0,

	PRIMARY KEY(player_id)
);

CREATE TABLE Matches (
	match_id int,
	winner_id int references Players (player_id),
	loser_id int references Players (player_id),

	PRIMARY KEY(match_id)
);