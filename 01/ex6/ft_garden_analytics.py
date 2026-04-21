#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_garden_analytics.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/03 21:35:32 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/21 15:24:59 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:
    @staticmethod
    def check_age(age: int) -> bool:
        return age > 365

    @classmethod
    def anonymous(cls):
        return cls("Unknown plant", 0.0, 0)

    class Stats:
        def __init__(self):
            self.__grow_calls = 0
            self.__age_calls = 0
            self.__show_calls = 0

        def inc_grow(self):
            self.__grow_calls += 1

        def inc_age(self):
            self.__age_calls += 1

        def inc_show(self):
            self.__show_calls += 1

        def display(self):
            print(f"Stats: {self.__grow_calls} grow,", end=" ")
            print(f"{self.__age_calls} age, {self.__show_calls} show")

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

    def show(self):
        print(f"{self.name}: {self.__height}cm, {self.__age} days old")
        self.stats.inc_show()

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
        self.stats.inc_grow()

    def age(self):
        self.set_age(self.get_age() + 1)
        self.stats.inc_age()


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
        self.shade_calls = 0

    def show(self):
        super().show()
        print(f"-> Trunk diameter: {self.trunk}cm")

    def produce_shade(self):
        print(f"Tree {self.name} now produces a shade of", end=" ")
        print(f"{self.get_height()}cm long and {self.trunk}cm wide")
        self.shade_calls += 1


class Seed(Flower):
    def __init__(self, name, height, age, color: str, seeds: int = 42):
        super().__init__(name, height, age, color)
        self.__seeds = 0
        self.__max_seeds = seeds

    def bloom(self):
        super().bloom()
        self.__seeds = self.__max_seeds

    def show(self):
        super().show()
        print(f"-> Seeds: {self.__seeds}")


def display_stats(plant):
    plant.stats.display()
    # Trees carry an extra counter that's not inside Stats
    if isinstance(plant, Tree):
        print(f"-> {plant.shade_calls} shade")


def ft_garden_analytics():
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.check_age(30)}")
    print(f"Is 400 days more than a year? -> {Plant.check_age(400)}")

    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print(f"[statistics for {rose.name}]")
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    print(f"[statistics for {rose.name}]")
    display_stats(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print(f"[statistics for {oak.name}]")
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print(f"[statistics for {oak.name}]")
    display_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 42)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print(f"[statistics for {sunflower.name}]")
    display_stats(sunflower)

    print("\n=== Anonymous")
    unknown = Plant.anonymous()
    unknown.show()
    print(f"[statistics for {unknown.name}]")
    display_stats(unknown)


if __name__ == "__main__":
    ft_garden_analytics()
