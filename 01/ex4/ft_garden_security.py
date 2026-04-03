#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_garden_security.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/28 15:42:26 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/03 21:12:35 by dzhukov            ###   ########.fr      #
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
        print(f"Plant created: ", end=" ")
        self.show()

    def grow(self):
        self.__height += 0.8
        self.__height = round(self.__height, 1)

    def aging(self):
        self.__age += 1

    def show(self):
        print(f"{self.name}: {self.__height}cm, {self.__age} days old")

    def set_height(self, height):
        if height < 0:
            print("Error: height can't be negative.")
            return
        self.__height = round(height, 1)
        print(f"Height updated: {self.__height}")

    def get_height(self):
        return self.__height

    def set_age(self, age):
        if age < 0:
            print("Error: age can't be negative.")
            return
        self.__age = age
        print(f"Age updated: {age}")

    def get_age(self):
        return self.__age


def ft_garden_security():
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10)
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
