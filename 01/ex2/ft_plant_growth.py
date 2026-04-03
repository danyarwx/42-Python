#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_plant_growth.py                                   :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/27 23:43:51 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/03 20:11:21 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:
    def __init__(self, name: str, height: float, aged: int, growth: float):
        self.name = name
        self.height = height
        self.aged = aged
        self.growth = growth

    def grow(self):
        self.height += self.growth
        self.height = round(self.height, 1)

    def age(self):
        self.aged += 1

    def show(self):
        print(f"{self.name}: {self.height}cm, {self.aged} days old")


def ft_plant_growth() -> None:
    rose = Plant("Rose", 25.0, 30, 0.8)
    print("=== Garden Plant Growth ===")
    print("=== Day 1 ===")
    start = rose.height
    rose.show()
    for i in range(2, 8):
        print(f"=== Day {i} ===")
        rose.grow()
        rose.age()
        rose.show()
    growth = round(rose.height - start, 1)
    print(f"Growth this week: {growth}cm")


if __name__ == "__main__":
    ft_plant_growth()
