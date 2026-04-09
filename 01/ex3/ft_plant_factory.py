#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_plant_factory.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/28 15:19:30 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/03 21:35:51 by dzhukov            ###   ########.fr      #
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


def ft_plant_factory():
    rose = Plant("Rose", 25.0, 30, 0.8)
    oak = Plant("Oak", 200.0, 365, 1.2)
    cactus = Plant("Cactus", 5.0, 90, 0.5)
    sun = Plant("Sunflower", 80.0, 45, 1.8)
    fern = Plant("Fern", 15.0, 120, 0.5)
    plants = [rose, oak, cactus, sun, fern]
    print("=== Plant Factory Output ===")
    for plant in plants:
        print("Created:", end=" ")
        plant.show()


if __name__ == "__main__":
    ft_plant_factory()
