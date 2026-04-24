#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_finally_block.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/22 16:56:30 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/24 16:56:16 by dzhukov            ###   ########.fr      #
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


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        print(f"Watering {plant_name}: [OK]")
    else:
        raise PlantError("Plant name is not capitalized")


def test_watering_system() -> None:
    print("=== Garden Watering System ===")

    print("\nTesting valid plants...")
    print("Opening watering system")
    try:
        for plant in ("TOMATO", "LETTUCE", "CARROTS"):
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print("...ending tests and returning to main")
        return
    finally:
        print("Closing watering system")

    print("\nTesting invalid plants...")
    print("Opening watering system")
    try:
        for plant in ("tomato", "lettuce", "carrots"):
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print("...ending tests and returning to main")
        return
    finally:
        print("Closing watering system")

    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
