#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_garden_analytics.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/03 21:35:32 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/07 18:04:29 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:

    @staticmethod
    def check_age(age: int) -> bool:
        return age > 365

    @classmethod
    def anonymous(cls):
        return cls("Unknown Plant", 0.0, 0)

    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self.stats = Plant.Stats()
        if height < 0:
            print("Error: invalid height. Use set_height() to change.")
            self.__height = 0.0
        else:
            self.__height = round(height, 1)

        if age < 0:
            print("Error: invalid age. Use set_age() to change.")
            self.__age = 0
        else:
            self.__age = age

    class Stats:
        def __init__(self):
            self.stats.grow_calls = 0
            self.stats.age_calls = 0
            self.stats.show_calls = 0

        def display_stats(self):
            print(f"Stats: {self.grow_calls} grow, ", end=" ")
            print(f"{self.age_calls} age, {self.show_calls} show")

    def show(self):
        print(f"{self.name}: {self.__height}cm, {self.__age} days old")
        self.stats.show_calls += 1

    def set_height(self, height):
        if height < 0:
            print("Error: height can't be negative.")
            return
        self.__height = round(height, 1)

    def get_height(self):
        return self.__height

    def set_age(self, age):
        if age < 0:
            print("Error: age can't be negative.")
            return
        self.__age = age

    def get_age(self):
        return self.__age

    def grow(self):
        self.set_height(round(self.get_height() + 2.1, 1))
        self.stats.grow_calls += 1

    def age(self):
        self.set_age(self.get_age() + 1)
        self.stats.age_calls += 1


class Flower(Plant):
    def __init__(self, name, height, age, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = 0

    def bloom(self):
        self.bloomed = 1

    def show(self):
        super().show()
        print(f"-> Color: {self.color}")
        if self.bloomed == 0:
            print("-> " + self.name + " has not bloomed yet")
        else:
            print("-> " + self.name + " is blooming beautifully!")


class Tree(Plant):
    def __init__(self, name, height, age, trunk: float):
        super().__init__(name, height, age)
        self.trunk = trunk

    def show(self):
        super().show()
        print(f"-> Trunk diameter: {self.trunk}cm")

    def produce_shade(self):
        print(f"Tree {self.name} now produces a shade of", end=" ")
        print(f"{self.get_height()}cm long and {self.trunk}cm wide")


class Seed(Flower):
    def __init__(self, name, height, age, color, seeds: int):
        super().__init__(name, height, age, color)
        self.seeds = seeds

    
