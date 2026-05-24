#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_crisis_response.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/08 13:01:33 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 4 -- EXCEPTION HANDLING (try / except) + `with`
# ---------------------------------------------------------------------
# When something goes wrong in Python, the interpreter creates an
# "exception" -- an object describing what failed -- and starts
# unwinding the call stack looking for something that catches it.
# If nothing catches it, the program prints a traceback and exits.
#
# Basic syntax:
#     try:
#         risky_thing()                 # the code that might fail
#     except SomeError:
#         handle_it()                   # runs only if SomeError raised
#     except (OtherError, ThirdError):  # tuple = catch any of these
#         handle_them()
#     except Exception as e:            # catch everything else; bind to e
#         fallback(e)
#     else:
#         on_success()                  # runs only if NO exception
#     finally:
#         always_run()                  # cleanup that must happen no
#                                       # matter what
#
# IMPORTANT: ORDER MATTERS.
# Exception classes form a hierarchy:
#       BaseException
#         |--- Exception
#                |--- OSError
#                        |--- FileNotFoundError
#                        |--- PermissionError
#                        |--- IsADirectoryError
#                        ...
# `except` matches by class OR any subclass. So if you wrote
# `except Exception` first, it would swallow FileNotFoundError before
# the more specific branch ever ran. RULE: put SPECIFIC exceptions
# at the top, generic ones at the bottom.
#
# Exception categories you'll see in this exercise:
#   - FileNotFoundError -- path doesn't exist on disk
#   - PermissionError   -- OS refuses access (e.g. chmod 000)
#   - Exception         -- catch-all safety net for anything else
#
# Why is the `with` statement INSIDE the try?
# Two reasons:
#   1. If open() itself fails, no file ever opened, so there's
#      nothing to close. The exception jumps straight to except.
#   2. If open() succeeds but read() inside the block raises,
#      `with` STILL closes the file before the exception propagates
#      out to `except`. So we get both safe cleanup AND graceful
#      handling. Best of both worlds.
# ---------------------------------------------------------------------


def crisis_handler(filename: str, routine: bool = False) -> None:
    # ------------------------------------------------------------------
    # crisis_handler(filename, routine=False):
    #   Tries to open and read `filename`. Reports the outcome with
    #   a single-line message. Never raises -- every exception path
    #   is converted into a printed status, so the calling code can
    #   keep running through more scenarios.
    #
    # Parameters:
    #   filename -- path to the file we want to read.
    #   routine  -- when True, the access is expected to be normal
    #               (label "ROUTINE ACCESS"); when False, we're
    #               testing a known-risky path ("CRISIS ALERT").
    #               This is purely cosmetic; both branches go through
    #               the same try/except logic.
    # ------------------------------------------------------------------

    # Ternary expression: VALUE_IF_TRUE if CONDITION else VALUE_IF_FALSE.
    # Equivalent to:
    #   if routine:
    #       label = "ROUTINE ACCESS"
    #   else:
    #       label = "CRISIS ALERT"
    label = "ROUTINE ACCESS" if routine else "CRISIS ALERT"
    print(f"{label}: Attempting access to '{filename}'...")

    try:
        # ---- The risky operation -----------------------------------
        # `with` is INSIDE the try (see top-of-file note).
        # If open() raises (file missing / permission denied) the
        # `with` block never starts and we drop straight to except.
        # If open() succeeds, the file is auto-closed on block exit,
        # even if .read() raises.
        with open(filename, "r") as vault:
            # .read()      -- get the entire file as one string.
            # .strip()     -- remove leading/trailing whitespace,
            #                 including the trailing "\n".
            content = vault.read().strip()
        # If execution reaches here, the try block completed without
        # any exception. The success messages live OUTSIDE the with
        # block but INSIDE the try, which is fine: they only run on
        # the no-exception path.
        print(f"SUCCESS: Archive recovered - ``{content}''")
        print("STATUS: Normal operations resumed")

    except FileNotFoundError:
        # MOST SPECIFIC exception first. Raised by open() when the
        # path does not exist on disk.
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")

    except PermissionError:
        # Also a subclass of OSError. Raised when the OS refuses
        # access to an existing file (e.g. read-protected by chmod).
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")

    except Exception as e:
        # Catch-all SAFETY NET. Anything that's still an Exception
        # (e.g. UnicodeDecodeError, IsADirectoryError, ...) lands here.
        # `as e` binds the exception object to the name `e` so we
        # can inspect it. We print type(e).__name__ -- the CLASS
        # name of the exception -- so the user knows what went wrong
        # without seeing a full traceback.
        # Note: bare `except:` (no class) would also catch system-exit
        # signals like KeyboardInterrupt, which you almost never want.
        # `except Exception` is the polite catch-all.
        print(f"RESPONSE: Unexpected anomaly ({type(e).__name__})")
        print("STATUS: Crisis handled, integrity preserved")


def ft_crisis_response() -> None:
    # ------------------------------------------------------------------
    # ft_crisis_response:
    #   Top-level demo. Calls crisis_handler() three times to exercise
    #   each of the three branches (FileNotFound, PermissionError,
    #   success). Each call prints its own block of status lines;
    #   we print() between them for visual separation.
    # ------------------------------------------------------------------

    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")

    # --- Scenario 1: file does NOT exist -> FileNotFoundError branch.
    # The 'lost_archive.txt' file is intentionally not created, so
    # open() will raise FileNotFoundError and the except matches.
    crisis_handler("lost_archive.txt")
    print()

    # --- Scenario 2: file exists but is unreadable -> PermissionError
    # branch. We pre-created classified_vault.txt with chmod 000 so
    # the OS denies read access. open() raises PermissionError.
    crisis_handler("classified_vault.txt")
    print()

    # --- Scenario 3: normal happy path -> success branch.
    # standard_archive.txt was generated by data_generator.py;
    # routine=True flips the label to "ROUTINE ACCESS" so the alarm
    # tone in the messaging doesn't sound like a crisis.
    crisis_handler("standard_archive.txt", routine=True)
    print()

    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    ft_crisis_response()
