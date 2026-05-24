#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_data_alchemist.py                                 :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 13:40:06 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/28 13:25:00 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import random


def main() -> None:
    print("=== Game Data Alchemist ===")

    players = ["Alice", "bob", "Charlie", "dylan", "Emma", "Gregory",
               "john", "kevin", "Liam"]

    # This list comprehension normalizes every player name.
    capitalized_players = [player.capitalize() for player in players]

    # This list comprehension keeps only names already capitalized in the first list.
    initial_capitalized_players = [player for player in players
                                   if player == player.capitalize()]

    # This dictionary comprehension gives every normalized player a random score.
    scores = {player: random.randint(0, 1000) for player in capitalized_players}
    average = round(sum(scores[player] for player in scores) / len(scores), 2)

    # This dictionary comprehension keeps only players scoring higher than average.
    high_scores = {player: scores[player] for player in scores
                   if scores[player] > average}

    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {capitalized_players}")
    print(f"New list of capitalized names only: {initial_capitalized_players}")
    print(f"Score dict: {scores}")
    print(f"Score average is {average}")
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
