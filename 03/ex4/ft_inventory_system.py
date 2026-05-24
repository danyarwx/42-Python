#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_inventory_system.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 13:39:34 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/08 12:52:01 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys


def add_parameter_to_inventory(inventory: dict, parameter: str) -> None:

    colon_count = 0
    item = ""
    quantity_text = ""

    for character in parameter:
        if character == ':':
            colon_count = colon_count + 1
        elif colon_count == 0:
            item = item + character
        else:
            quantity_text = quantity_text + character

    if colon_count != 1:
        print(f"Error - invalid parameter '{parameter}'")
        return

    if len(item) == 0:
        print(f"Error - invalid parameter '{parameter}'")
        return

    if item in inventory.keys():
        print(f"Redundant item '{item}' - discarding")
        return

    try:
        quantity = int(quantity_text)
    except ValueError as error:
        print(f"Quantity error for '{item}': {error}")
        return

    inventory.update({item: quantity})


def find_most_abundant_item(inventory: dict) -> str:

    items = list(inventory.keys())
    most_item = items[0]

    for item in items:
        if inventory[item] > inventory[most_item]:
            most_item = item

    return most_item


def find_least_abundant_item(inventory: dict) -> str:
    # Start with the first item, then replace it only when a smaller value is found.
    # Because equal values do not replace it, ties keep the first command-line item.
    items = list(inventory.keys())
    least_item = items[0]

    for item in items:
        if inventory[item] < inventory[least_item]:
            least_item = item

    return least_item


def print_percentages(inventory: dict, total_quantity: int) -> None:
    # Go item by item and calculate this item's part of the total inventory.
    for item in inventory.keys():
        percentage = round(inventory[item] / total_quantity * 100, 1)
        print(f"Item {item} represents {percentage}%")


def main() -> None:
    # The dictionary stores each item name together with its integer quantity.
    inventory = {}

    # sys.argv[0] is the script name, so real parameters start at index 1.
    for parameter in sys.argv[1:]:
        add_parameter_to_inventory(inventory, parameter)

    print("=== Inventory System Analysis ===")
    print(f"Got inventory: {inventory}")

    # keys() gives all item names; list() turns them into a printable list.
    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    # values() gives all quantities; sum() adds them together.
    total_quantity = sum(inventory.values())
    print(f"Total quantity of the {len(item_list)} items: {total_quantity}")

    # These steps need at least one item and a non-zero total to avoid bad math.
    if len(item_list) > 0 and total_quantity != 0:
        print_percentages(inventory, total_quantity)

        most_item = find_most_abundant_item(inventory)
        least_item = find_least_abundant_item(inventory)

        print(
            f"Item most abundant: {most_item} with quantity {inventory[most_item]}")
        print(
            f"Item least abundant: {least_item} with quantity {inventory[least_item]}")

    # Add one final item with update(), then display the inventory again.
    inventory.update({'magic_item': 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
