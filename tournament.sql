-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE Players (
	player_id serial,
	player_name varchar(50),

	PRIMARY KEY(player_id)
);

CREATE TABLE Matches (
	match_id serial,
	winner_id int references Players (player_id),
	loser_id int references Players (player_id),

	PRIMARY KEY(match_id)
);
