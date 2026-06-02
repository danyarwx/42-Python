#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_ancient_text.py                                   :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/06/02 15:22:21 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import typing


def ft_ancient_text(path: str) -> None:
    print("=== Cyber Archives Recovery ===\n")
    print("Accessing file: " + path)

    try:
        vault: typing.IO[str] = open(path, "r")
    except OSError as err:
        print(f"ERROR opening file '{path}': {str(err)}")
        return

    print("---\n")

    data = vault.read()
    print(data)

    vault.close()
    print("\n---")

    print(f"\nFile '{path}' closed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ft_ancient_text.py <file>")
    else:
        ft_ancient_text(sys.argv[1])
