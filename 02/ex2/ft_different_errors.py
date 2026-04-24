#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_different_errors.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/22 16:56:24 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/24 16:05:32 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def input_temperature(temp_str: str) -> int:
    num = int(temp_str)
    return (num)


def garden_operations(operation_number: int) -> None:

    if operation_number == 0:
        input_temperature("abc")
    elif operation_number == 1:
        a = 10 / 0
    elif operation_number == 2:
        fd = open('./file.txt')
    elif operation_number == 3:
        5 + "hello"
    else:
        print("Operation completed successfully!")
        return


def test_error_types() -> None:

    print("=== Garden Error Types Demo ===")
    for operation_number in range(0, 5):
        try:
            print(f"Testing operation {operation_number}...")
            garden_operations(operation_number)
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error1:
            print(f"Caught ZeroDivisionError: {error1}")
        except FileNotFoundError as error2:
            print(f"Caught FileNotFoundError: {error2}")
        except TypeError as error3:
            print(f"Caught TypeError: {error3}")

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
