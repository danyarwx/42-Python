#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_plant_types.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/03 20:10:05 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/03 21:20:27 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
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


class Flower(Plant):
    def __init__(self, name, height, age, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = "has not bloomed yet"

    def bloom(self):
        self.bloomed = "is blooming beautifully!"

    def show(self):
        super().show()
        print(f"-> Color: {self.color}")
        print("-> " + self.name + " " + self.bloomed)


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


class Vegetable(Plant):
    def __init__(self, name, height, age, harvest: str):
        super().__init__(name, height, age)
        self.harvest = harvest
        self.nvalue = 0

    def show(self):
        super().show()
        print(f"-> Harvest season: {self.harvest}")
        print(f"-> Nutritional value: {self.nvalue}")

    def grow(self):
        self.set_height(round(self.get_height() + 2.1, 1))

    def age(self):
        self.set_age(self.get_age() + 1)

    def grow_and_age(self, days: int):
        self.nvalue += days
        for i in range(1, days + 1):
            self.grow()
            self.age()


def ft_plant_types():
    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose = Flower("Rose", 15, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print(f"[asking the oak to produce shade]")
    oak.produce_shade()
    print("\n=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print(f"[make tomato grow and age for 20 days]")
    tomato.grow_and_age(20)
    tomato.show()


if __name__ == "__main__":
    ft_plant_types()
