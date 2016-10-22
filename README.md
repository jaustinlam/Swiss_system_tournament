# Swiss Style Tournament Database
A database that allows players to sign up for a tournament. Once signed up,
the database will allow to pair off players and then report matches till
all rounds are completed and a winner is found. For more on Swiss Style
Tournaments [Click Here.](https://en.wikipedia.org/wiki/Swiss-system_tournament)

## Installation
1. Go to https://github.com/jaustinlam/Swiss_system_tournament.git and download.
2. Install [Python](https://www.python.org/downloads/)
3. Install [Vagrant](https://www.vagrantup.com)
4. Install [VirtualBox](https://www.virtualbox.org)
5. Launch the Vagrant VM and configure.
6. To import the database navigate to the tournament folder on your machine.
7. Launch psql and enter "create database tournament".
8. Import in the tables and views with \i tournament.sql.

## Usage
1. Create a Python script in a new file. Import all from tournament.py
2. Use the following methods to run your tournament:

* createTournament(tournament_id)
> Creates a new tournament
* registerPlayer(name, tournament_id)
> Register a new player to the tournament.

* deleteTournaments()
> Deletes all tournaments
* deleteATournament(tournament_id)
> Deletes a single tournament
* deleteMatches()
> Deletes all matches
* deletePlayers()
> Deletes all players

* countPlayers()
> Returns a count of players
* playerStandings(tournament_id)
> Returns a table of all players in the current tournaments standings.
* reportMatch(winner, loser, tournament_id)
> Report the result of match between 2 players.
* swissPairings(tournament_id)
> Based of the standings creates match ups of players for the next round.

3. Run your script from the file you created.


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

v1. Our first version

