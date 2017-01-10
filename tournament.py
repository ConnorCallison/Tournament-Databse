#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    c = connection.cursor()
    c.execute("DELETE FROM Matches;")
    c.execute("UPDATE Players SET matches = 0;")
    c.execute("UPDATE Players SET wins = 0;")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    c = connection.cursor()
    c.execute("DELETE FROM Players;")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    c = connection.cursor()
    c.execute("SELECT count(*) from Players;")
    result = c.fetchone()
    connection.commit()
    connection.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    def escapeApostrophe(string_in):
        if string_in.find("'"):
            return string_in.replace("'", "")
        else:
            return string_in

    first_name = escapeApostrophe(name.split(" ")[0])

    if len(name.split(" ")) > 1:
        last_name = escapeApostrophe(name.split(" ")[1])
    else:
        last_name = ""

    connection = connect()
    c = connection.cursor()
    c.execute("INSERT INTO Players (player_fname, player_lname) VALUES ('" +
              first_name + "','" + last_name + "');")
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    c = connection.cursor()
    c.execute(
        ("SELECT p.player_id AS id, p.player_fname || ' ' || p.player_lname AS"
            " name, p.wins AS wins, p.matches AS matches FROM Players AS p;"))
    connection.commit()
    result = c.fetchall()
    connection.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    c = connection.cursor()
    c.execute(
        ("UPDATE Players SET wins = wins + 1, matches = matches + 1"
            " WHERE player_id =" + str(winner) + ";"))
    c.execute(
        ("UPDATE Players SET matches = matches + 1 "
            "WHERE player_id =" + str(loser) + ";"))
    connection.commit()
    connection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    connection = connect()
    c = connection.cursor()
    c.execute("SELECT * FROM Players;")
    players = c.fetchall()
    connection.close()

    pairs = []
    paired = []

    for player in players:
        if player[0] not in paired:
            for potential_match in players:
                if potential_match[0] not in paired:
                    if (player[3] == potential_match[3] and
                       player[0] != potential_match[0]):
                            pairs.append([player[0], player[1] +
                                          " " + player[2],
                                          potential_match[0],
                                          potential_match[1] +
                                          " " + potential_match[2]])
                            paired.append(player[0])
                            paired.append(potential_match[0])
                            break

    return pairs
