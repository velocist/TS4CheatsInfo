# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: T:\InGame\Gameplay\Scripts\Server\objects\components\game\game_team_autobalanced.py
# Compiled at: 2015-09-28 22:14:00
# Size of source mod 2**32: 2521 bytes
from objects.components.game.game_team import GameTeam

class GameTeamAutoBalanced(GameTeam):

    def add_player(self, game, sim):
        if game.number_of_teams < game.current_game.teams_per_game.upper_bound:
            game.add_team([sim])
            return
        previous_number_of_players = len(game._teams[0].players)
        for team in reversed(game._teams):
            if len(team.players) <= previous_number_of_players:
                team.players.append(sim)
                return

        game._teams[0].players.append(sim)

    def _rebalance_teams(self, game):
        excess_index = None
        starvation_index = None
        min_value = int(game.number_of_players / game.number_of_teams)
        for i, team in enumerate(game._teams):
            team_length = len(team.players)
            if excess_index is None:
                if team_length > min_value:
                    excess_index = i
                else:
                    if team_length < min_value:
                        starvation_index = i
                if excess_index is not None and starvation_index is not None:
                    game._teams[starvation_index].players.append(game._teams[excess_index].players.pop())
                    break

    def remove_player(self, game, sim):
        for team in game._teams:
            if sim not in team.players:
                continue
            team.players.remove(sim)
            if game.winning_team is None:
                self._rebalance_teams(game)
            if not team.players:
                game._teams.remove(team)