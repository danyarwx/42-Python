#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_stream.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/16 15:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/16 15:00:00 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 1 -- POLYMORPHIC ROUTING ("a DataStream of mixed data types")
# ---------------------------------------------------------------------
# Goal: take ONE stream that mixes numbers, text, and log entries,
# and route each item to whichever processor knows how to handle it.
# The router doesn't know (or care) what subclass a processor is --
# it only knows the abstract DataProcessor contract: validate + ingest.
# That's POLYMORPHISM in action.
#
# WHAT POLYMORPHISM BUYS US
#   The DataStream class below has ONE loop that says:
#       "ask each registered processor 'can you take this?' until
#        one says yes; if none does, log an error."
#   We can register Numeric/Text/Log -- or any FUTURE subclass --
#   without ever editing DataStream. The router is closed for
#   modification but open for extension. (This is the "Open/Closed
#   Principle" from the SOLID acronym, if you've heard of it.)
#
# REUSE FROM EX 0
#   The DataProcessor / NumericProcessor / TextProcessor /
#   LogProcessor classes are reproduced verbatim at the top of this
#   file. The subject expects each exercise file to be self-contained
#   for submission, so we duplicate rather than import.
# ---------------------------------------------------------------------

import abc
from typing import Any


# =====================================================================
# === EX 0 CODE (unchanged, reproduced here for self-containment) ====
# =====================================================================
# Comments here are abbreviated; see ex0/data_processor.py for the
# extended explanations of ABC, _store_item, ranks, etc.
# =====================================================================
class DataProcessor(abc.ABC):
    NAME: str = "DataProcessor"

    def __init__(self) -> None:
        # (rank, value) tuples; FIFO buffer drained by output().
        self.__store: list[tuple[int, str]] = []
        # Monotonic rank counter; never resets.
        self.__next_rank: int = 0
        # Lifetime count of ingested items.
        self.__total: int = 0

    def name(self) -> str:
        return self.NAME

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        return self.__store.pop(0)

    def _store_item(self, value: str) -> None:
        self.__store.append((self.__next_rank, value))
        self.__next_rank += 1
        self.__total += 1

    def remaining(self) -> int:
        return len(self.__store)

    def total(self) -> int:
        return self.__total


class NumericProcessor(DataProcessor):
    NAME = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for x in data:
                self._store_item(str(x))
        else:
            self._store_item(str(data))


class TextProcessor(DataProcessor):
    NAME = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for x in data:
                self._store_item(x)
        else:
            self._store_item(data)


class LogProcessor(DataProcessor):
    NAME = "Log Processor"

    def _is_log_dict(self, d: Any) -> bool:
        if not isinstance(d, dict):
            return False
        return all(
            isinstance(k, str) and isinstance(v, str) for k, v in d.items()
        )

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return self._is_log_dict(data)
        if isinstance(data, list):
            return all(self._is_log_dict(x) for x in data)
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for d in items:
            level = d.get("log_level", "")
            message = d.get("log_message", "")
            self._store_item(f"{level}: {message}")


# =====================================================================
# === NEW IN EX 1: DataStream ========================================
# =====================================================================
class DataStream:
    # ------------------------------------------------------------------
    # DataStream: a polymorphic router.
    #   Holds a list of registered DataProcessor instances. When given
    #   a heterogeneous list of inputs (process_stream), it asks each
    #   processor in turn "validate(item)?" and gives the item to the
    #   first one that says yes. If none of them does, an error line
    #   is printed for that item.
    #
    # WHY THIS DESIGN?
    #   - DataStream depends on the ABSTRACT type DataProcessor, NOT
    #     on Numeric/Text/Log. We could plug in a brand new processor
    #     class tomorrow with zero changes here.
    #   - The order of registration matters: the first matching
    #     processor wins. If two processors would both accept the
    #     same input, the earlier one consumes it.
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        # Registry of processors, in registration order.
        # Double underscore name-mangles it: outsiders can't poke it.
        self.__procs: list[DataProcessor] = []

    # ---- register_processor -----------------------------------------
    # Add a processor to the registry. Order matters (see above).
    # ------------------------------------------------------------------
    def register_processor(self, proc: DataProcessor) -> None:
        self.__procs.append(proc)

    # ---- process_stream ---------------------------------------------
    # Polymorphic loop. For each element of the input stream we ask
    # each registered processor's validate(); the first one that
    # returns True gets the item via its ingest(). Unhandled items
    # produce an error line on stdout.
    # ------------------------------------------------------------------
    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            # `handled` tracks whether any processor accepted this item.
            handled = False
            for proc in self.__procs:
                # POLYMORPHIC CALL: proc.validate() dispatches to the
                # subclass's validate -- NumericProcessor.validate,
                # TextProcessor.validate, etc. This is the entire
                # point of the abstract base class.
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    # Once one processor takes the item, we stop --
                    # no double-handling.
                    break
            if not handled:
                # No processor matched; log an error and move on.
                print(
                    f"DataStream error - "
                    f"Can't process element in stream: {item}"
                )

    # ---- print_processors_stats -------------------------------------
    # Diagnostic dump of every registered processor's totals.
    # ------------------------------------------------------------------
    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        # Edge case: no processors registered yet.
        if not self.__procs:
            print("No processor found, no data")
            return
        for proc in self.__procs:
            # Another polymorphic call: each proc reports under its
            # own NAME via name(), and contributes its own counts.
            print(
                f"{proc.name()}: total {proc.total()} items processed, "
                f"remaining {proc.remaining()} on processor"
            )


# =====================================================================
# Test scenario / __main__ block
# =====================================================================
def main() -> None:
    # ------------------------------------------------------------------
    # Walks through the scenario in the subject's example output:
    #   1. Make a DataStream, show stats (empty).
    #   2. Register only Numeric; send a mixed batch -> errors for
    #      Text/Log items, Numeric items accepted.
    #   3. Register Text and Log; resend the SAME batch -> all good.
    #   4. Consume a few items via output() on each processor;
    #      show stats again to see "remaining" drop while "total"
    #      stays put.
    # ------------------------------------------------------------------

    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    # First stats call: no processors yet. Exercises the empty branch.
    stream.print_processors_stats()
    print()

    # Build named processors UP FRONT so we still have handles to
    # call .output() on later. DataStream stores them privately, so
    # without these locals we couldn't reach them from outside.
    num = NumericProcessor()
    txt = TextProcessor()
    log = LogProcessor()

    # Mixed batch reused in two passes.
    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]

    print("Registering Numeric Processor")
    stream.register_processor(num)
    print()

    print(f"Send first batch of data on stream: {batch}")
    # Only Numeric is registered, so Text/Log items will trigger
    # the "can't process" error branch in process_stream.
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()

    print("Registering other data processors")
    stream.register_processor(txt)
    stream.register_processor(log)

    print("Send the same batch again")
    # Now every item finds a home: numbers go to Numeric, strings
    # to Text, dicts/lists-of-dicts to Log.
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()

    # ---- Consume some items via output() ----
    # output() pops the oldest stored item from the processor and
    # returns its (rank, value). We discard the return value here --
    # the demo only needs to show how `remaining` shrinks while
    # `total` stays the same.
    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        txt.output()
    for _ in range(1):
        log.output()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
