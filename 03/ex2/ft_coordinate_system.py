#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_coordinate_system.py                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 12:28:11 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/27 13:33:55 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import math


# def my_split(s: str) -> list[str]:
#     parts = []
#     current = ""

#     for char in s:
#         if char == ",":
#             parts.append(current.strip())
#             current = ""
#         else:
#             current += char

#     parts.append(current.strip())
#     return parts

def get_player_pos() -> tuple[float, float, float]:
    while True:
        text = input("Enter new coordinates as floats in format 'x,y,z': ")

        try:
            nums = text.split(",")

            if len(nums) != 3:
                print("Invalid syntax")
                continue

            x = float(nums[0])
            y = float(nums[1])
            z = float(nums[2])

            return (x, y, z)
        except ValueError as e:
            print(f"Error on parameter: {e}")


def ft_coordinate_system() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    res = get_player_pos()
    print(f"Got a first tuple: {res}")
    print(f"It includes: X={res[0]}, Y={res[1]}, Z={res[2]}")
    dis = round(math.sqrt(res[0] ** 2 + res[1] ** 2 + res[2] ** 2), 4)
    print(f"Distance to center: {dis}")

    print("\nGet a second set of coordinates")
    res2 = get_player_pos()
    x = res2[0] - res[0]
    y = res2[1] - res[1]
    z = res2[2] - res[2]
    dis_2 = round(math.sqrt(x ** 2 + y ** 2 + z ** 2), 4)
    print(f"Distance between the 2 sets of coordinates: {dis_2}")


if __name__ == "__main__":
    ft_coordinate_system()
