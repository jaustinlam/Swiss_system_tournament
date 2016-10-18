-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create table to register players.
CREATE TABLE players(
    id serial PRIMARY KEY,
    name text
    registered timestamp default now()
    );

-- Create table to record matches.
CREATE TABLE matches(
    id serial PRIMARY KEY,
    winner integer REFERENCES players (id) ON DELETE CASCADE,
    loser integer REFERENCES players (id) ON DELETE CASCADE
    );

-- Create table to record standings.
CREATE TABLE standings(
    player_id integer REFERENCES players(id) ON DELETE CASCADE,
    player_name text,
    wins integer,
    matches integer
    );








