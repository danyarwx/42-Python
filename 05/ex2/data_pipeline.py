#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_pipeline.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/16 15:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/16 15:00:00 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 2 -- THE OUTPUT SIDE: PLUGIN SYSTEM VIA `Protocol` (DUCK TYPING)
# ---------------------------------------------------------------------
# Ex0 built the processors; ex1 routed mixed inputs to them. Now we
# wire up an EXPORT side: pull N items out of each processor and feed
# them to an "export plugin" (CSV, JSON, anything you write later).
#
# DUCK TYPING ("if it quacks like a duck, it IS a duck")
#   In Python, you usually don't ask "is X an instance of class Y?".
#   You just call X.quack() and hope X knows how. Code that works on
#   "anything with a quack()" is a duck-typed API.
#
# `typing.Protocol` puts a STATIC TYPE on duck typing
#   A Protocol is like an interface, but you don't have to declare
#   that your class implements it. Any class with matching method
#   names and signatures counts as a member of the Protocol AS FAR
#   AS THE TYPE CHECKER IS CONCERNED. There's no runtime check
#   unless you decorate with @runtime_checkable.
#
#   Example:
#       class Quacker(Protocol):
#           def quack(self) -> None: ...
#
#       def make_noise(q: Quacker) -> None:
#           q.quack()
#
#       class Duck:
#           def quack(self) -> None: print("quack")
#
#       make_noise(Duck())   # mypy is happy: Duck has quack()
#
#   Compare with abc.ABC: ABCs use NOMINAL typing -- you must
#   inherit from the ABC to count. Protocols use STRUCTURAL typing
#   -- you just need the right methods. We use BOTH in this project:
#       - DataProcessor is an ABC because Numeric/Text/Log all
#         genuinely share implementation (the storage + counters).
#       - ExportPlugin is a Protocol because export classes share
#         nothing but the shape of one method; we don't want to
#         force them to inherit from anything.
#
# WHAT THIS FILE ADDS
#   - ExportPlugin(Protocol) with one method: process_output(data).
#   - CSVPlugin and JSONPlugin -- two plain classes that happen to
#     match the protocol shape (they're "duck-compatible").
#   - DataStream.output_pipeline(nb, plugin) -- consumes up to nb
#     items from each registered processor and hands them to the
#     plugin. nb is "at most"; if a processor has fewer items, we
#     send what's there.
# ---------------------------------------------------------------------

import abc
from typing import Any, Protocol


# =====================================================================
# === EX 0/1 CODE (unchanged, reproduced for self-containment) =======
# =====================================================================
class DataProcessor(abc.ABC):
    NAME: str = "DataProcessor"

    def __init__(self) -> None:
        self.__store: list[tuple[int, str]] = []
        self.__next_rank: int = 0
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
# === NEW IN EX 2: ExportPlugin Protocol + concrete plugins ==========
# =====================================================================

# ---------------------------------------------------------------------
# ExportPlugin: a TYPING Protocol.
#   - Inherits from typing.Protocol.
#   - Declares the method process_output(data) with no body (just `...`).
#   - Any class with a matching process_output() method is
#     "structurally" an ExportPlugin to mypy. No `class Foo(ExportPlugin)`
#     declaration required.
# ---------------------------------------------------------------------
class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        # Body is purely for documentation; protocols never execute it.
        ...


# ---------------------------------------------------------------------
# CSVPlugin: writes one CSV line, values comma-joined, no quoting.
#   Notice we DON'T inherit from ExportPlugin. We just match the
#   shape. mypy will accept a CSVPlugin wherever ExportPlugin is
#   declared, because Python's duck typing + Protocol.
# ---------------------------------------------------------------------
class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        # Build the CSV row. We ignore the rank and just take the
        # string value of each tuple. ",".join joins with commas.
        # A generator expression `(v for r, v in data)` walks the
        # list, unpacking each (rank, value) tuple into r and v.
        row = ",".join(v for _, v in data)
        print("CSV Output:")
        print(row)


# ---------------------------------------------------------------------
# JSONPlugin: writes a flat JSON object {"item_<rank>": "<value>", ...}.
#   We build the JSON string by hand, no `import json`, per the
#   subject. All values are quoted as strings (even numeric-looking
#   ones), matching the expected example output.
# ---------------------------------------------------------------------
class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        # Build a list of '"item_<rank>": "<value>"' strings, then
        # join with ", ", then wrap in braces. Manual but clear.
        # f-strings with embedded double-quotes use single-quote
        # delimiters: f'"item_{r}": "{v}"'.
        parts = [f'"item_{r}": "{v}"' for r, v in data]
        body = ", ".join(parts)
        print("JSON Output:")
        # f"{{ }}" -- doubled braces escape to literal '{' / '}'.
        print(f"{{{body}}}")


# =====================================================================
# === DataStream now has output_pipeline ==============================
# =====================================================================
class DataStream:
    def __init__(self) -> None:
        # Same as ex1: private list of registered processors.
        self.__procs: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.__procs.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        # Same loop as ex1: polymorphic dispatch over validate+ingest.
        for item in stream:
            handled = False
            for proc in self.__procs:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - "
                    f"Can't process element in stream: {item}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.__procs:
            print("No processor found, no data")
            return
        for proc in self.__procs:
            print(
                f"{proc.name()}: total {proc.total()} items processed, "
                f"remaining {proc.remaining()} on processor"
            )

    # ---- output_pipeline (NEW IN EX 2) -------------------------------
    # For each registered processor, pull up to `nb` items via
    # output() and hand them to `plugin.process_output(batch)`.
    # If a processor has fewer than nb items, we send what we have.
    # ------------------------------------------------------------------
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.__procs:
            # Collect up to `nb` items from this processor.
            data: list[tuple[int, str]] = []
            for _ in range(nb):
                # output() raises IndexError on empty buffer. We
                # check remaining() first to stop cleanly.
                if proc.remaining() == 0:
                    break
                data.append(proc.output())
            # Hand the batch to the plugin. Duck typing: we never
            # checked plugin's type at runtime; we just call its
            # process_output() method. If the caller passed something
            # without that method, Python would raise AttributeError
            # here. mypy would have flagged it earlier.
            plugin.process_output(data)


# =====================================================================
# Test scenario / __main__ block
# =====================================================================
def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()
    print()

    # Hold named processors so the demo can poke them if needed.
    num = NumericProcessor()
    txt = TextProcessor()
    log = LogProcessor()

    print("Registering Processors")
    stream.register_processor(num)
    stream.register_processor(txt)
    stream.register_processor(log)
    print()

    # ---- First batch -------------------------------------------------
    batch1: list[Any] = [
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
    print(f"Send first batch of data on stream: {batch1}")
    stream.process_stream(batch1)
    print()
    stream.print_processors_stats()
    print()

    # ---- Export 3 via CSV plugin ------------------------------------
    print("Send 3 processed data from each processor to a CSV plugin:")
    # Build a CSVPlugin and pass it to the pipeline. CSVPlugin does
    # NOT inherit from ExportPlugin -- duck typing makes this fine.
    stream.output_pipeline(3, CSVPlugin())
    print()
    stream.print_processors_stats()
    print()

    # ---- Second batch -----------------------------------------------
    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR",
             "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {batch2}")
    stream.process_stream(batch2)
    print()
    stream.print_processors_stats()
    print()

    # ---- Export 5 via JSON plugin -----------------------------------
    print("Send 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONPlugin())
    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
