#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_raise_exception.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/21 16:38:42 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/22 16:48:13 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def input_temperature(temp_str: str) -> int:
    num = int(temp_str)
    if num < 0:
        raise ValueError(f"{num}°C is too cold for plants (min 0°C)")
    if num > 40:
        raise ValueError(f"{num}°C is too hot for plants (max 40°C)")
    return (num)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print("\nInput data is '25'")
    try:
        res = input_temperature("25")
        print(f"Temperature is now {res}°C")
    except ValueError as error:
        print(f"Failed! Error message : {error}")

    print("\nInput data is 'abc'")
    try:
        res = input_temperature("abc")
        print(f"Temperature is now {res}°C")
    except ValueError as error:
        print(f"Caught input temperature error: {error}")

    print("\nInput data is '100'")
    try:
        res = input_temperature("100")
        print(f"Temperature is now {res}°C")
    except ValueError as error:
        print(f"Caught input temperature error: {error}")

    print("\nInput data is '-50'")
    try:
        res = input_temperature("-50")
        print(f"Temperature is now {res}°C")
    except ValueError as error:
        print(f"Caught input temperature error: {error}")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
