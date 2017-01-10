# Tournament Database Project

This project creates a dtabase for a game tournament, there are tables, Player
and Matches. This project uses PostgreSQL and Python's DB-API.

## Installation

1. Download all files in, or clone this repository.
2. Navigate to the directory containing the files.
3. Run the command 'psql' This will open your PostgreSQL command line.
4. Create the database by typing / pasting in 'CREATE DATABASE tournament'
5. Now you must switch into the database we just created, run '\connect tournament'
6. Run the command '\i tournament.sql'. This will set up all of the tables outlined in tournament.sql.
7. Now your database is ready to go, you may run the test file if you would like by running 'tournament_test.py'.

## Files

* tournament.sql - Creates all functining parts of the database.
* tournament.py - This file contains all of the Python functions to interact with the database such as asdding a player or reporting a match.
* tournament_test.py - This file contins all of the unit tests to make sure that the functions in tournament.py are functioning properly.
