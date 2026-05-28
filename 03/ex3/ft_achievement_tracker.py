#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_achievement_tracker.py                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 13:38:59 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/28 13:28:26 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import random


def gen_player_achievements(achievements: set[str]) -> set[str]:
    count = random.randint(5, len(achievements) - 2)

    return set(random.sample(list(achievements), count))


def main() -> None:
    achievements = {'Crafting Genius', 'Strategist', 'World Savior',
                    'Speed Runner', 'Survivor', 'Master Explorer',
                    'Treasure Hunter', 'Unstoppable', 'First Steps',
                    'Collector Supreme', 'Untouchable', 'Sharp Mind',
                    'Boss Slayer', 'Hidden Path Finder'}

    alice = gen_player_achievements(achievements)
    bob = gen_player_achievements(achievements)
    charlie = gen_player_achievements(achievements)
    dylan = gen_player_achievements(achievements)

    distinct = alice.union(bob, charlie, dylan)

    common = alice.intersection(bob, charlie, dylan)

    only_alice = alice.difference(bob.union(charlie, dylan))
    only_bob = bob.difference(alice.union(charlie, dylan))
    only_charlie = charlie.difference(alice.union(bob, dylan))
    only_dylan = dylan.difference(alice.union(bob, charlie))

    alice_missing = achievements.difference(alice)
    bob_missing = achievements.difference(bob)
    charlie_missing = achievements.difference(charlie)
    dylan_missing = achievements.difference(dylan)

    print("=== Achievement Tracker System ===\n")
    print(f"Player Alice: {alice}")
    print(f"\nPlayer Bob: {bob}")
    print(f"\nPlayer Charlie: {charlie}")
    print(f"\nPlayer Dylan: {dylan}")
    print(f"\nAll distinct achievements: {distinct}")
    print(f"\nCommon achievements: {common}")
    print(f"\nOnly Alice has: {only_alice}")
    print(f"Only Bob has: {only_bob}")
    print(f"Only Charlie has: {only_charlie}")
    print(f"Only Dylan has: {only_dylan}")
    print(f"\nAlice is missing: {alice_missing}")
    print(f"Bob is missing: {bob_missing}")
    print(f"Charlie is missing: {charlie_missing}")
    print(f"Dylan is missing: {dylan_missing}")


if __name__ == "__main__":
    main()
