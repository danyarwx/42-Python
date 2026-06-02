#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_archive_creation.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/06/02 15:21:53 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import sys
import typing


def transform(data: str) -> str:
    new_lines = []
    for line in data.splitlines():
        new_lines.append(line + "#")
    # \n is the separator which goes between the strings
    return "\n".join(new_lines) + "\n"


def save(content: str) -> None:
    name = input("Enter new file name (or empty:) ")
    if name == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{name}'.")
    out: typing.IO[str] = open(name, "w")
    out.write(content)
    out.close()
    print(f"Data saved in file '{name}'.")


def ft_archive_creation(path: str) -> None:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{path}'\n")

    try:
        vault: typing.IO[str] = open(path, "r")
    except OSError as err:
        print(f"ERROR opening file '{path}': {str(err)}")
        return

    print("---\n")
    data = vault.read()
    print(data)
    vault.close()

    print("---")
    print(f"File '{path}' closed.\n")

    print("Transform data:")
    print("---\n")
    new_content = transform(data)
    print(new_content)
    print("---")

    save(new_content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ft_archive_creation.py <file>")
    else:
        ft_archive_creation(sys.argv[1])
