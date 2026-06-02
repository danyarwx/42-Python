#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_stream_management.py                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/06/02 16:17:28 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# EX 2 -- STREAM MANAGEMENT (same flow as ex1, but mind the channels):
#   - exception messages go to sys.stderr with a "[STDERR]" prefix,
#     not to stdout, so they can be redirected independently.
#   - user input is read from sys.stdin instead of input().

import sys
import typing


def error(message: str) -> None:
    print(f"[STDERR] {message}", file=sys.stderr)


def prompt_line(prompt: str) -> str:
    # write a prompt to sdtout
    sys.stdout.write(prompt)
    # output the prompt from buffer to the screen, wait for user input
    sys.stdout.flush()
    # read one single line from stdin and remove trailing \n
    return sys.stdin.readline().rstrip("\n")


def transform(data: str) -> str:
    new_lines = []
    for line in data.splitlines():
        new_lines.append(line + "#")
    # \n is the separator which goes between the strings
    return "\n".join(new_lines) + "\n"


def save(content: str) -> None:
    name = prompt_line("Enter new file name (or empty): ")
    if name == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{name}'")
    try:
        out: typing.IO[str] = open(name, "w")
    except OSError as err:
        error(f"Error opening file '{name}': {str(err)}")
        print("Data not saved.")
        return

    out.write(content)
    out.close()
    print(f"Data saved in file '{name}'.")


def ft_stream_management(path: str) -> None:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{path}'")

    try:
        vault: typing.IO[str] = open(path, "r")
    except OSError as err:
        error(f"Error opening file '{path}': {str(err)}")
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
        print("Usage: python ft_stream_management.py <file>")
    else:
        ft_stream_management(sys.argv[1])
