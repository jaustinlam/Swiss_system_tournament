#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")

def deleteTournament():
    """Remove all the tournament records from the database"""
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor
    c.execute('''
        DELETE from tournament
        ''') # Delete all records from tournament
    conn.commit() # Commit deletion
    conn.close() # Close connection

def deleteATournament(tournament_id):
    """Remove a single tournament record from the database

    Args:
        tournament_id: an integer specifying the tournament number.

    """
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor
    bleach_id = bleach.clean(tournament_id) # Clean id
    c.execute('''
        DELETE from tournament WHERE id = %s
        ''', (bleach_id,)) # Delete a single tournament
    conn.commit() # Commit deletion
    conn.close() # Close connection


def deleteMatches():
    """Remove all the match records from the database."""

    conn = connect() # Create connection
    c = conn.cursor() # Create cursor on connection
    c.execute('''
        DELETE from matches
        ''') # Delete all records from matches
    conn.commit() # Commit deletion

    c.execute('''
        UPDATE standings
        SET wins = 0, matches = 0
        ''') # Reset standings
    conn.commit() # Commit standings

    conn.close() # Close connection

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor on connection
    c.execute('''
        DELETE from players
        ''') # Count all of the players
    conn.commit()
    conn.close() # Close connection


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor on connection
    c.execute('''
        SELECT count(*)
        from players;
        ''') # Count all of the players
    cp = c.fetchall() # all entries in result
    return cp[0][0] # a multi dimensional array
    conn.close() # Close connection

def createTournament(tournament_id):
    """Creates a new tournament record in tournament database.

    Args:
        id: the id of the tournament, needs to be unique.
    """
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor
    bleach_id = bleach.clean(tournament_id) # Clean id
    c.execute('''
        INSERT INTO tournament VALUES(%s)
        ''', (bleach_id,)) # Insert new tournament
    conn.commit() # Commit new record
    conn.close() # Close connection


def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
      tournament_id: the tournament the player is registered to.
    """
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor on connection
    bleach_name = bleach.clean(name) # Clean name
    bleach_id = bleach.clean(tournament_id) # Clean id
    c.execute('''
        INSERT INTO players(name, tournament) VALUES(%s, %s)
        ''', (bleach_name, bleach_id,)) # Insert bleach name and id into database
    conn.commit() # Commit new player

    c.execute('''
        SELECT * FROM players ORDER BY registered DESC LIMIT 1;
        ''') # Find the the player we just registered by most recent
    new_player = c.fetchall()
    new_id = new_player[0][0] # The player's id
    new_name = new_player[0][1] # The player's name
    new_tournament = new_player[0][3] # The tournament the player id registered

    c.execute('''
        SELECT * FROM standings
        WHERE player_id = %i'''% new_id) # Error checking if id already exists
    isplayer = c.fetchall()

    if not isplayer: # If id doesn't already exist enter into standings
        c.execute('''
            INSERT INTO standings
            VALUES(%s, %s, 0, 0, %s)
            ''', (new_id, new_name, new_tournament,)
            ) # Insert new player into standings
        conn.commit() # Commit entry into standings
    conn.close() # Close connection


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tournament_id: The id of the tournament you wish
        to find.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect() # Create connection
    c = conn.cursor() # Create cursor
    bleach_id = bleach.clean(tournament_id) # Clean id
    c.execute('''
        SELECT player_id, player_name, wins, matches
        FROM standings
        WHERE tournament = %s
        ORDER BY wins DESC
        ''', (bleach_id,)) # Retrieve all records that matches tournament
    standings = c.fetchall()
    return standings
    conn.close()

def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_id: the id of the tournament the match is played in
    """

    conn = connect() # Create connection
    c = conn.cursor() # Create cursor on connection
    bleach_winner = bleach.clean(winner) # Cleaning winner
    bleach_loser = bleach.clean(loser) # Cleaning loser
    bleach_id = bleach.clean(tournament_id) # Clean id
    c.execute('''
        INSERT INTO matches(winner, loser, tournament)
        VALUES(%s, %s, %s)
        ''', (bleach_winner, bleach_loser, tournament_id,)) # Insert in matches
    conn.commit() # Commit match

    # For winner
    c.execute('''
        UPDATE standings
        SET wins = wins + 1,
        matches = matches + 1
        WHERE player_id = %s
        AND tournament = %s''' , (bleach_winner, bleach_id,))
    conn.commit()

    # For loser
    c.execute('''
        UPDATE standings
        SET matches = matches + 1
        WHERE player_id = %s
        AND tournament = %s''', (bleach_loser, bleach_id,))
    conn.commit()
    conn.close() # Close connection


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        tournament_id: The id of the tournament

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    cstandings = playerStandings(1) # Current standings
    matches = [] # Empty array to pass in standings

    for p in range(0, len(cstandings), 2):
        m = (cstandings[p][0], cstandings[p][1],
            cstandings[p+1][0], cstandings[p+1][1])
        matches.append(m)
    return matches


