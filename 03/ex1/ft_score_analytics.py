#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_score_analytics.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/26 18:20:16 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/27 10:14:01 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys


def ft_score_analytics() -> None:
    print("=== Player Score Analytics ===")

    scores = []

    for st in sys.argv[1:]:
        try:
            score = int(st)
            scores.append(score)
        except ValueError:
            print(f"Invalid parameter: '{st}'")

    if not scores:
        print(
            "No scores provided. Usage: python3 ft_score_analytics.py "
            "<score1> <score2> ...")
        return

    print(f"Scores processed: {scores}")

    total_players = len(scores)
    total_score = sum(scores)
    average = total_score / total_players
    high_score = max(scores)
    low_score = min(scores)
    score_range = high_score - low_score

    print(f"Total players: {total_players}")
    print(f"Total score: {total_score}")
    print(f"Average score: {average}")
    print(f"High score: {high_score}")
    print(f"Low score: {low_score}")
    print(f"Score range: {score_range}")


if __name__ == "__main__":
    ft_score_analytics()
