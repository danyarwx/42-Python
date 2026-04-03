#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_garden_security.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/28 15:42:26 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/03 19:59:26 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:
    def __init__(self, name: str, height: float, age: int, growth: float):
        self.name = name
        if height < 0:
            print("Error: invalid height. Use set_height() to change.")
            self._height = 0.0
        else:
            self._height = round(height, 1)

        if age < 0:
            print("Error: invalid age. Use set_age() to change.")
            self._age = 0
        else:
            self._age = age
        self.growth = growth
        print(f"Plant created: ", end = " ")
        self.show()

    def grow(self):
        self._height += self.growth
        self._height = round(self._height, 1)

    def aging(self):
        self._age += 1

    def show(self):
        print(f"{self.name}: {self._height}cm, {self._age} days old")

    def set_height(self, height):
        if height < 0:
            print("Error: height can't be negative.")
            return
        self._height = round(height, 1)
        print(f"Height updated: {self._height}")

    def get_height(self):
        return self._height

    def set_age(self, age):
        if age < 0:
            print("Error: age can't be negative.")
            return
        self._age = age
        print(f"Age updated: {age}")

    def get_age(self):
        return self._age

def ft_garden_security():
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10, 1.2)
    print()
    rose.set_height(25)
    rose.set_age(30)
    print()
    rose.set_height(-25)
    rose.set_age(-30)
    print()
    print("Current state:", end=" ")
    rose.show()

if __name__ == "__main__":
    ft_garden_security()
