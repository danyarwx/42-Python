#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_vault_security.py                                 :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/08 13:01:27 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 3 -- THE `with` STATEMENT (CONTEXT MANAGER)
# ---------------------------------------------------------------------
# Two ways to open a file, side by side:
#
#   1) Manual (ex0/ex1 style):
#        f = open("data.txt", "r")
#        try:
#            do_stuff(f)
#        finally:
#            f.close()
#      You need the try/finally to guarantee close() runs even on
#      errors. Forget the finally and a crash leaks the file handle.
#
#   2) `with` statement (this exercise):
#        with open("data.txt", "r") as f:
#            do_stuff(f)
#      Python automatically calls f.close() when the block ends --
#      normally OR via an exception. Equivalent to the try/finally
#      version, but shorter and harder to mess up.
#
# How does it work under the hood?
#   `with EXPR as NAME:` requires EXPR to evaluate to a "context
#   manager" -- an object with two special methods:
#       __enter__(self)      -- runs at the top of the with block.
#                               Its return value is bound to NAME.
#       __exit__(self, exc_type, exc_value, traceback)
#                            -- runs at the bottom, ALWAYS.
#                               Receives info about any exception that
#                               occurred (or None, None, None on
#                               normal exit). For a file object,
#                               __exit__ calls .close().
#   open() returns a file object that already implements these two
#   methods -- that's why open() works with `with` out of the box.
#
# This is Python's version of the C++ RAII pattern ("Resource
# Acquisition Is Initialization"): tie cleanup to scope exit. The
# pattern is everywhere in idiomatic Python:
#       with open(...) as f:           # files
#       with lock:                     # threading.Lock
#       with conn.cursor() as cur:     # databases
#       with tempfile.NamedTemp...     # temp files (auto-deleted)
#
# Multiple files in one `with`:
#       with open("a") as a, open("b") as b:
#           ...
#   Both get auto-closed at the end of the block.
# ---------------------------------------------------------------------


def ft_vault_security() -> None:
    # ------------------------------------------------------------------
    # ft_vault_security:
    #   Demonstrates the `with` statement for both reading and writing.
    #   1. Reads classified_data.txt and prints its content.
    #   2. Creates security_protocols.txt with one line.
    #   In each case the file is auto-closed at the end of `with`.
    # ------------------------------------------------------------------

    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols\n")

    # ---- SECURE EXTRACTION (read) -----------------------------------
    print("SECURE EXTRACTION:")
    # `with open(path, "r") as vault:` is two operations in one line:
    #   * open the file (mode "r" = read text)
    #   * bind the resulting file object to the name `vault`
    # The indented block below is the "context"; when it ends, the
    # interpreter calls vault.__exit__(...), which calls vault.close().
    with open("classified_data.txt", "r") as vault:
        # .read() returns ALL the content as one string.
        # .strip() removes leading/trailing whitespace (including the
        # trailing "\n" the file usually ends with). Without strip()
        # we'd get an extra blank line before "SECURE PRESERVATION:".
        data = vault.read().strip()
        print(data)
    # <- file is closed here, automatically.

    # ---- SECURE PRESERVATION (write) --------------------------------
    print("\nSECURE PRESERVATION:")
    # Same pattern, mode "w" for writing. As ex1 covered: this
    # creates the file or wipes its contents on open().
    with open("security_protocols.txt", "w") as vault:
        # Storing the string in a variable lets us write it AND print
        # it without duplicating the literal -- one source of truth.
        line = "[CLASSIFIED] New security protocols archived"
        # write() does NOT auto-newline; we add "\n" so the file ends
        # cleanly with one line + newline.
        vault.write(line + "\n")
        print(line)
    # <- file is closed AND flushed here. If write() had raised, the
    # close still runs because __exit__ is guaranteed.

    print("Vault automatically sealed upon completion\n")
    print("All vault operations completed with maximum security.")


if __name__ == "__main__":
    ft_vault_security()
