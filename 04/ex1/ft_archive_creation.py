#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_archive_creation.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/16 15:03:20 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 1 -- FILE WRITING
# ---------------------------------------------------------------------
# Goal: create a new text file from scratch and write three lines.
#
# File modes you should know:
#   "r"  -- read (default). File MUST exist.
#   "w"  -- write. Creates the file if missing.
#           !!! TRUNCATES (wipes) the file if it already exists.
#   "a"  -- append. Creates if missing, but writes go to the END
#           instead of erasing existing data. Useful for log files.
#   "x"  -- exclusive create. Creates the file; raises FileExistsError
#           if it already exists. Safer than "w" when you don't want
#           to overwrite.
#   "rb"/"wb"/"ab" -- same as above but BINARY mode (bytes, not text).
#
# .write(text):
#   - Argument MUST be a string (use str(x) if x is a number).
#   - Returns the number of characters written (we ignore it here).
#   - Does NOT add a newline automatically -- you add "\n" yourself.
#   - Writes are usually BUFFERED in memory; the data hits disk on
#     close() or flush(). That's why forgetting close() can leave
#     you with an empty or truncated file on disk.
# ---------------------------------------------------------------------


def ft_archive_creation() -> None:
    # ------------------------------------------------------------------
    # ft_archive_creation:
    #   Creates new_discovery.txt in the current directory and writes
    #   three numbered entries into it. Existing file (if any) is
    #   replaced. Returns None.
    # ------------------------------------------------------------------

    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    print("Initializing new storage unit: new_discovery.txt")

    # ---- open() in write mode ----
    # "w" wipes the file if it already exists, or creates it fresh.
    # The result is a file object stored in `archive`.
    # No try/except needed for "file missing": it gets created.
    archive = open("new_discovery.txt", "w")
    print("Storage unit created successfully...\n")

    print("Inscribing preservation data...")

    entries = [
        "[ENTRY 001] New quantum algorithm discovered",
        "[ENTRY 002] Efficiency increased by 347%",
        "[ENTRY 003] Archived by Data Archivist trainee",
    ]

    for entry in entries:
        print(entry)
        archive.write(entry + "\n")

    # ---- close() ----
    # Two things happen on close:
    #   1. Buffered data in memory is flushed to disk (the actual
    #      bytes finally land in the file).
    #   2. The OS-level file descriptor is released.
    # Forgetting close() can leave the file empty or partially
    # written. ex3 introduces `with` which handles this for you.
    archive.close()

    print("\nData inscription complete. Storage unit sealed.")
    print("Archive 'new_discovery.txt' ready for long-term preservation.")


if __name__ == "__main__":
    ft_archive_creation()
