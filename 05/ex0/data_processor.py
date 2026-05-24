#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/16 15:00:00 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/16 15:00:00 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# ---------------------------------------------------------------------
# EX 0 -- ABSTRACT BASE CLASSES (ABC) + METHOD OVERRIDING
# ---------------------------------------------------------------------
# Goal: build a family of "data processors" that all share the same
# INTERFACE but each handle a different kind of data (numbers, text,
# log entries). The shared interface is captured in an ABSTRACT
# BASE CLASS; the differences live in subclasses.
#
# WHY ABSTRACT?
#   In ex5/ex6 of project 01 we used plain inheritance: Plant ->
#   Flower / Tree / ... You COULD instantiate Plant directly, even
#   though "a plant with no specific type" doesn't really make sense.
#   An abstract class says: "this class is INCOMPLETE on purpose.
#   You can't make one directly. Subclasses must finish it."
#
# THE `abc` MODULE
#   abc.ABC          -- base class to inherit from to make YOUR class
#                       abstract.
#   @abc.abstractmethod
#                    -- decorator that marks a method as abstract.
#                       Any subclass MUST override it, or trying to
#                       instantiate the subclass raises TypeError.
#
# WHAT WE BUILD
#   DataProcessor (abstract)
#     |-- validate(data) -> bool   (abstract: subclass decides)
#     |-- ingest(data)   -> None   (abstract: subclass decides)
#     +-- output()       -> tuple[int, str]   (concrete: shared)
#
#   NumericProcessor : DataProcessor    -- handles int, float, lists
#   TextProcessor    : DataProcessor    -- handles str and lists
#   LogProcessor     : DataProcessor    -- handles dict[str,str] etc.
#
# DESIGN DECISIONS
# - Internal storage is a list of (rank, value_string) tuples,
#   populated by ingest() and drained by output(). `rank` is a
#   monotonically increasing integer (0, 1, 2, ...) that records the
#   INGESTION ORDER. It never resets, even after output(), so the
#   stream stays traceable.
# - I expose a protected helper `_store_item(value: str)` on the
#   base class. Subclasses call it after they've validated and
#   converted their inputs. This keeps the storage logic (next rank,
#   total counter) in ONE PLACE.
# - validate(data) MUST accept Any and return bool, never raise.
#   ingest(data) MAY raise if the data doesn't pass validation --
#   callers are expected to validate first.
# ---------------------------------------------------------------------

# `abc` gives us ABC + @abstractmethod.
# `typing.Any` is the "I don't constrain the type" placeholder, used
# in signatures where literally any value is acceptable (validate).
import abc
from typing import Any


# =====================================================================
# DataProcessor -- the abstract base
# =====================================================================
class DataProcessor(abc.ABC):
    # ------------------------------------------------------------------
    # __init__:
    #   Runs when a SUBCLASS instance is created. Because Python calls
    #   the parent's __init__ via super().__init__() (or implicitly
    #   when subclasses don't define one), this runs first and sets
    #   up the shared internal state.
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        # __store: the buffer of items waiting to be output().
        # Each entry is (rank, value_string). Double underscore means
        # the attribute name gets MANGLED to _DataProcessor__store --
        # subclasses can't accidentally collide with the name. They
        # interact with this list only through the helpers below.
        self.__store: list[tuple[int, str]] = []
        # __next_rank: counter for the next rank to assign.
        # Starts at 0, never decreases, even when items are output().
        # Two different items NEVER share a rank.
        self.__next_rank: int = 0
        # __total: total items ever ingested. Used by ex1's statistics.
        # `remaining` is just len(__store); `total - remaining` =
        # items that were already extracted via output().
        self.__total: int = 0

    # ------------------------------------------------------------------
    # name():
    #   Human-readable label. Each subclass sets a class-level NAME
    #   string; this method returns it polymorphically. (We could use
    #   a property; a method keeps things consistent with output().)
    # ------------------------------------------------------------------
    # Class-level attribute. Subclasses OVERRIDE it (see below). Type
    # annotation ClassVar would be more correct; for an exercise this
    # is sufficient.
    NAME: str = "DataProcessor"

    def name(self) -> str:
        return self.NAME

    # ------------------------------------------------------------------
    # validate(data) -- ABSTRACT.
    #   Each subclass must implement this. Returns True iff the data
    #   "shape" is something this processor can handle. Pure check:
    #   no side effects, no exceptions.
    # ------------------------------------------------------------------
    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        # The body of an abstract method is intentionally empty.
        # `...` (Ellipsis) is the conventional placeholder; `pass`
        # works too. The decorator is what makes it abstract, not
        # the body -- Python lets abstract methods have a real body
        # which subclasses can opt to call via super().
        ...

    # ------------------------------------------------------------------
    # ingest(data) -- ABSTRACT.
    #   Each subclass must implement this. Convert `data` into one or
    #   more string items and store them via self._store_item(...).
    #   If `data` is not valid, raise an exception -- never silently
    #   accept bad data.
    # ------------------------------------------------------------------
    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    # ------------------------------------------------------------------
    # output() -- CONCRETE / shared.
    #   Pop the OLDEST stored item (FIFO) and return (rank, value).
    #   We intentionally don't make this abstract: all processors
    #   store strings the same way, so the extraction logic is shared.
    # ------------------------------------------------------------------
    def output(self) -> tuple[int, str]:
        # list.pop(0) removes and returns the first element. It's
        # O(n) on a list, but the queues are tiny so it's fine. A
        # collections.deque would be O(1) if performance mattered.
        # If the store is empty, pop(0) raises IndexError -- exactly
        # what we want, because "output from empty" is a bug.
        return self.__store.pop(0)

    # ------------------------------------------------------------------
    # _store_item(value) -- PROTECTED helper for subclasses.
    #   Single underscore = "internal, but subclasses may touch".
    #   Appends one (rank, value) entry and bumps the counters.
    # ------------------------------------------------------------------
    def _store_item(self, value: str) -> None:
        self.__store.append((self.__next_rank, value))
        self.__next_rank += 1
        self.__total += 1

    # ------------------------------------------------------------------
    # remaining() / total() -- read-only views of the counters.
    #   Used by ex1's DataStream for statistics.
    # ------------------------------------------------------------------
    def remaining(self) -> int:
        # How many items are CURRENTLY in the buffer.
        return len(self.__store)

    def total(self) -> int:
        # How many items have EVER been ingested.
        return self.__total


# =====================================================================
# NumericProcessor -- handles int, float, and lists of either
# =====================================================================
class NumericProcessor(DataProcessor):
    # Override the class-level NAME so name() returns the right label.
    NAME = "Numeric Processor"

    # ---- validate -----------------------------------------------------
    # Accepts:
    #   * a single int or float
    #   * a list whose elements are all int or float
    # Rejects everything else (str, dict, None, mixed lists, ...).
    # ------------------------------------------------------------------
    def validate(self, data: Any) -> bool:
        # isinstance(x, (T1, T2)) returns True if x is T1 OR T2.
        # Note: in Python `bool` is a subclass of `int`, so True/False
        # would pass. We accept this -- the spec doesn't forbid it
        # and excluding bool adds noise.
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            # all(iterable) returns True only if EVERY element is
            # truthy. With a generator expression we check each
            # element of the list is a number.
            return all(isinstance(x, (int, float)) for x in data)
        return False

    # ---- ingest -------------------------------------------------------
    # Signature uses `int | float | list[int | float]` (Python 3.10+
    # union syntax) to document what's accepted. mypy can use it.
    # Subject: "The overriding ingest method signature must reflect
    # the accepted types."
    # ------------------------------------------------------------------
    def ingest(self, data: int | float | list[int | float]) -> None:
        # Defensive check: if a caller skipped validate(), refuse the
        # input loudly. We re-use validate() so the rules live in
        # one place.
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            # Each element of the list becomes its own stored item.
            # str(x) converts numbers to their printable form:
            #   str(42) -> '42', str(3.14) -> '3.14', str(-1) -> '-1'.
            for x in data:
                self._store_item(str(x))
        else:
            # Single number: store one item.
            self._store_item(str(data))


# =====================================================================
# TextProcessor -- handles str and lists of str
# =====================================================================
class TextProcessor(DataProcessor):
    NAME = "Text Processor"

    def validate(self, data: Any) -> bool:
        # A plain string is fine.
        if isinstance(data, str):
            return True
        # A list whose every element is a string is also fine.
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for x in data:
                # No conversion needed: strings stay strings.
                self._store_item(x)
        else:
            self._store_item(data)


# =====================================================================
# LogProcessor -- handles dict[str, str] and lists of such dicts
# =====================================================================
class LogProcessor(DataProcessor):
    NAME = "Log Processor"

    # Helper to check "this dict has only string keys and string
    # values". Marked with leading underscore (protected) -- it's an
    # implementation detail of LogProcessor.
    def _is_log_dict(self, d: Any) -> bool:
        if not isinstance(d, dict):
            return False
        # d.items() yields (key, value) pairs. We require every key
        # AND every value to be a string.
        return all(
            isinstance(k, str) and isinstance(v, str) for k, v in d.items()
        )

    def validate(self, data: Any) -> bool:
        # Single dict?
        if isinstance(data, dict):
            return self._is_log_dict(data)
        # List of dicts where every dict passes the check?
        if isinstance(data, list):
            return all(self._is_log_dict(x) for x in data)
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        # Normalize: always work on a list of dicts. If a single dict
        # came in, wrap it in a one-element list so the loop below
        # handles both cases.
        items = data if isinstance(data, list) else [data]
        for d in items:
            # Format each log entry as "LEVEL: message". The test
            # data always carries the keys 'log_level' and
            # 'log_message'; we rely on that convention here.
            # dict.get(key, default) avoids KeyError if a key is
            # missing -- we fall back to empty strings to stay safe.
            level = d.get("log_level", "")
            message = d.get("log_message", "")
            self._store_item(f"{level}: {message}")


# =====================================================================
# Test scenario / __main__ block
# =====================================================================
def main() -> None:
    # ------------------------------------------------------------------
    # Demonstrates each subclass: validate good/bad input, raise on
    # bad ingest, then ingest a batch and extract a few items.
    # ------------------------------------------------------------------
    print("=== Code Nexus - Data Processor ===\n")

    # ---- Numeric -----------------------------------------------------
    print("Testing Numeric Processor...")
    num = NumericProcessor()
    # validate() doesn't mutate state, so we can call it freely.
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")

    # Show that ingest() refuses bad input. We pass a string to a
    # numeric processor and expect ValueError. The `type: ignore`
    # comment tells mypy "yes, I'm intentionally passing a wrong
    # type here to exercise the runtime check" -- the subject asks
    # for this deliberate mypy warning.
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")  # type: ignore[arg-type]
    except Exception as e:
        # type(e).__name__ would be 'ValueError'; we just print the
        # message to match the example output.
        print(f"Got exception: {e}")

    print("Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for _ in range(3):
        # output() returns (rank, value). We unpack the tuple
        # directly into two named variables -- Python tuple unpacking.
        rank, value = num.output()
        print(f"Numeric value {rank}: {value}")

    # ---- Text --------------------------------------------------------
    print("\nTesting Text Processor...")
    txt = TextProcessor()
    print(f"Trying to validate input '42': {txt.validate(42)}")

    print("Processing data: ['Hello', 'Nexus', 'World']")
    txt.ingest(["Hello", "Nexus", "World"])

    print("Extracting 1 value...")
    rank, value = txt.output()
    print(f"Text value {rank}: {value}")

    # ---- Log ---------------------------------------------------------
    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")

    log_batch = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {log_batch}")
    log.ingest(log_batch)

    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
