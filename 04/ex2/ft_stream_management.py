#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_stream_management.py                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/08 13:01:20 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 2 -- STDIN / STDOUT / STDERR
# ---------------------------------------------------------------------
# Every running program automatically gets three I/O "channels". They
# are file-like objects you can read from or write to.
#
#   sys.stdin   (file descriptor 0) -- INPUT stream
#       Default source for input(). Connected to the keyboard in an
#       interactive shell. In a pipeline `prog1 | prog2`, prog2's
#       stdin is wired to prog1's stdout.
#
#   sys.stdout  (file descriptor 1) -- standard OUTPUT stream
#       Default destination for print(). For program RESULTS --
#       data your script meaningfully produces.
#
#   sys.stderr  (file descriptor 2) -- ERROR / alert OUTPUT stream
#       A separate output channel for diagnostics: warnings,
#       progress messages, error reports. Still goes to the
#       terminal by default, but it's NOT the same channel as
#       stdout, which lets the user redirect them independently.
#
# Why two output streams?
#   It's about SEPARATION. Run:
#       python3 prog.py > out.txt
#   This redirects stdout into out.txt. stderr still goes to the
#   screen. So if you wrote an alert to stderr, the user sees it
#   live; data lands in the file. Mixing them would mean alerts
#   end up buried in the data file, useless for debugging.
#
# In the shell:
#   python3 prog.py             -- both shown on screen
#   python3 prog.py > out.txt   -- only stdout into out.txt
#   python3 prog.py 2> err.txt  -- only stderr into err.txt (2 is fd)
#   python3 prog.py > o 2> e    -- both, separately, into two files
#   python3 prog.py &> all.txt  -- both merged (bash shortcut)
#
# Choosing the stream:
#   print(...)                       -- defaults to sys.stdout
#   print(..., file=sys.stderr)      -- explicit stderr
#   sys.stdout.write("text")         -- lower-level (no auto-newline)
#   sys.stderr.write("text\n")       -- ditto, useful in libraries
#
# Reading:
#   input("prompt: ")  -- prints prompt to stdout, reads a line from
#                         stdin, returns it WITHOUT the trailing \n.
#   sys.stdin.read()   -- read EVERYTHING from stdin (until EOF).
#                         Useful when the program is the receiver in
#                         a shell pipeline.
# ---------------------------------------------------------------------

# `import sys` makes the sys module available. We need sys.stdout /
# sys.stderr to direct print() to the right channel.
import sys


def ft_stream_management() -> None:
    # ------------------------------------------------------------------
    # ft_stream_management:
    #   1. Reads two lines of user input from stdin.
    #   2. Echoes a status line to stdout.
    #   3. Sends a diagnostic alert to stderr.
    #   4. Confirms completion on stdout.
    #
    # Run with `> out.txt` or `2> err.txt` to see the streams split.
    # ------------------------------------------------------------------

    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")

    # ---- input() -----------------------------------------------------
    # input(prompt) does three things:
    #   a) Writes `prompt` to stdout (without newline).
    #   b) Blocks the program until the user presses Enter on stdin.
    #   c) Returns whatever the user typed (without the trailing \n).
    # The return value is ALWAYS a str. If you need a number, wrap
    # in int(...) or float(...).
    archivist_id = input("Input Stream active. Enter archivist ID: ")
    status = input("Input Stream active. Enter status report: ")

    # Blank line for visual separation in the output.
    print()

    # ---- Standard data via stdout -----------------------------------
    # f"..." is an f-string: any {expr} inside is replaced by the
    # value of expr at runtime. Here we splice in archivist_id and
    # status (both are strings, no conversion needed).
    # file=sys.stdout is the default; we pass it explicitly to make
    # the contrast with stderr below crystal clear.
    print(
        f"[STANDARD] Archive status from {archivist_id}: {status}",
        file=sys.stdout,
    )

    # ---- Alert via stderr -------------------------------------------
    # Same print() call but redirected to stderr. To the eye it
    # still appears on the terminal -- the difference is invisible
    # until someone redirects stdout. Try:
    #   echo "ARCH | nominal" | python3 ft_stream_management.py > /tmp/o
    # The [ALERT] line is still on screen; [STANDARD] lines went
    # into /tmp/o.
    print(
        "[ALERT] System diagnostic: Communication channels verified",
        file=sys.stderr,
    )

    print("[STANDARD] Data transmission complete", file=sys.stdout)
    print("\nThree-channel communication test successful.")


if __name__ == "__main__":
    ft_stream_management()
