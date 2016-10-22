-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create a tournament table.
CREATE TABLE tournament(
    id integer PRIMARY KEY
    );

-- Create table to register players.
CREATE TABLE players(
    id serial PRIMARY KEY,
    name text,
    registered timestamp default now(),
    tournament integer REFERENCES tournament (id) ON DELETE CASCADE
    );

-- Create table to record matches.
CREATE TABLE matches(
    id serial PRIMARY KEY,
    winner integer REFERENCES players (id) ON DELETE CASCADE,
    loser integer REFERENCES players (id) ON DELETE CASCADE,
    tournament integer REFERENCES tournament (id) ON DELETE CASCADE
    );

-- Create a view to generate a standings table for a given tournament.
CREATE VIEW playerstandings AS
    SELECT players.tournament, players.id, players.name,
    count(wins.winner) AS wins,
    (SELECT count(wins.winner)) +
    (SELECT count(losses.loser)) AS matches
    FROM players
    LEFT JOIN matches as wins
    ON players.id = wins.winner
    LEFT JOIN matches as losses
    ON players.id = losses.loser
    GROUP BY players.id
    ORDER BY wins DESC;














