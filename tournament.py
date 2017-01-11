#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    connection, c = connect()

    c.execute("TRUNCATE Matches CASCADE;")

    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection, c = connect()

    c.execute("TRUNCATE Players CASCADE;")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection, c = connect()

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
    connection, c = connect()

    c.execute("INSERT INTO Players (player_name) VALUES (%s);", ((name,)))
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
    connection, c = connect()

    query = '''SELECT t1.player_id, t1.player_name, coalesce(t4.wins,0) AS wins,
            coalesce(t4.matches,0) AS matches FROM (SELECT p.player_id AS
            player_id, p.player_name AS player_name FROM Players AS p) t1
             LEFT JOIN (SELECT t3.player_id AS player_id,
             coalesce(t2.wins,0) as wins,
            t3.matches AS matches FROM (SELECT p.player_id AS player_id,
            count(match_id) AS matches FROM Players AS p,
            Matches AS m WHERE
            m.winner_id = p.player_id OR m.loser_id = p.player_id
            GROUP BY p.player_id) t3 LEFT JOIN
            (SELECT p.player_id AS player_id,
            count(m.winner_id) as wins FROM Players AS p,Matches AS m WHERE
            m.winner_id = p.player_id GROUP BY p.player_id) t2 ON
            t2.player_id = t3.player_id) t4 ON t1.player_id = t4.player_id;'''

    c.execute(query)
    result = c.fetchall()
    connection.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection, c = connect()

    c.execute(
        "INSERT INTO Matches (winner_id,loser_id) VALUES (%s,%s);",
        (winner, loser))
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
    players = playerStandings()
    pairs = []
    paired = []

    for player in players:
        if player[0] not in paired:
            for potential_match in players:
                if potential_match[0] not in paired:
                    if (player[2] == potential_match[2] and
                            player[0] != potential_match[0]):
                        pairs.append([player[0],
                                      player[1],
                                      potential_match[0],
                                      potential_match[1]])
                        paired.append(player[0])
                        paired.append(potential_match[0])
                        break

    return pairs
