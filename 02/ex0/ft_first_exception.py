#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_first_exception.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/21 16:03:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/21 16:36:58 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #


def input_temperature(temp_str: str) -> int:
    num = int(temp_str)
    return (num)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print("\nInput data is : '25'")
    try:
        res = input_temperature("25")
        print(f"Temperature is now {res}°C")
    except ValueError as error:
        print(f"Failed! Error message : {error}")

    print("\nTest data is : 'abc'")
    try:
        res = input_temperature("abc")
        print(f"Temperature is now {res}°C")
    except ValueError as error:
        print(f"Caught input temperature error: {error}")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
