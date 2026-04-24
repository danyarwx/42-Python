#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_custom_errors.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/22 16:56:27 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/24 16:35:49 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class GardenError(Exception):
    def __init__(self, message="Unknown Garden Error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message="Unknown Plant Error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message="Unknown Water Error") -> None:
        super().__init__(message)


def inspect_greenhouse(zone: str) -> None:
    if zone == "tomatoes":
        raise PlantError("Tomato leaves detected as yellow and curled")
    if zone == "water_tank":
        raise WaterError("Water tank pressure dropped below safe level")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")

    print("\nTesting PlantError...")
    try:
        inspect_greenhouse("tomatoes")
    except PlantError as error:
        print(f"Caught PlantError: {error}")

    print("\nTesting WaterError...")
    try:
        inspect_greenhouse("water_tank")
    except WaterError as error:
        print(f"Caught WaterError: {error}")

    print("\nTesting catching all garden errors...")

    for zone in ("tomatoes", "water_tank"):
        try:
            inspect_greenhouse(zone)
        except GardenError as error:
            print(f"Caught GardenError: {error}")

    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
