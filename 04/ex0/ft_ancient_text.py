#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_ancient_text.py                                   :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/16 14:59:30 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 0 -- FILE READING (manual close)
# ---------------------------------------------------------------------
# Goal: open a text file, read its contents, print them, close.
# This exercise teaches the LOW-LEVEL way of doing it, without `with`.
# Later exercises will switch to the `with` block which is safer.
#
# Three primitives we use:
#   open(path, mode) -- ask the OS to open a file. Returns a "file
#                       object" that has methods like .read(), .write(),
#                       .close(). Mode "r" = read text (default mode).
#   .read()          -- return the WHOLE content of the file as one
#                       big string. Fine for small files; for huge
#                       files you'd loop line-by-line instead.
#   .close()         -- release the OS-level file handle. The OS
#                       keeps a limited number of file handles open;
#                       leaking them eventually crashes the program.
#                       Closing also flushes buffered writes (but
#                       here we only read, so nothing to flush).
#
# Why try/except here?
#   open() raises FileNotFoundError if the file doesn't exist.
#   Without try/except the script would crash with a traceback.
#   With try/except we can print a friendly message and return.
# ---------------------------------------------------------------------


def ft_ancient_text() -> None:
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    print("Accessing Storage Vault: ancient_fragment.txt")

    try:
        vault = open("ancient_fragment.txt", "r")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
        return

    print("Connection established...\n")
    print("RECOVERED DATA:")

    data = vault.read()
    print(data)

    vault.close()

    print("\nData recovery complete. Storage unit disconnected.")


if __name__ == "__main__":
    ft_ancient_text()
