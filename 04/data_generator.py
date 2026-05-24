#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_generator.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 12:57:28 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/08 13:14:38 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #


"""
Cyber Archives Training Data Generator

Generates structured test data for file operation exercises with comprehensive
error handling, type safety, and extensible architecture.
"""

# ---------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------
# json     -- serialize/deserialize Python objects <-> JSON text.
# sys      -- access the interpreter (argv, exit codes, streams).
# wraps    -- helper used when writing decorators, see below.
# Path     -- modern object-oriented file paths (replaces os.path).
# typing   -- "type hints" (Dict, List, Optional, ...) for clarity
#             and tools like mypy. They are NOT enforced at runtime.
# datetime -- timestamps (used to mark when files were generated).
# ---------------------------------------------------------------------
import json
import sys
from functools import wraps
from pathlib import Path
from typing import Dict, List, Optional, Union, Callable, Any
from datetime import datetime


# ---------------------------------------------------------------------
# CONCEPT: DECORATORS
# ---------------------------------------------------------------------
# A decorator is a function that TAKES a function and RETURNS a new
# function. The `@decorator` syntax above a `def` is just a shortcut:
#
#     @handle_file_errors
#     def foo(): ...
#
# is equivalent to:
#
#     def foo(): ...
#     foo = handle_file_errors(foo)
#
# So `handle_file_errors` receives the original function (`func`),
# builds a `wrapper` around it that adds error-catching, and returns
# `wrapper` as the new `foo`. From the outside calling foo() actually
# calls wrapper(), which calls the original.
#
# @wraps(func) copies the original function's name and docstring onto
# the wrapper -- without it, foo.__name__ would become "wrapper".
# ---------------------------------------------------------------------
def handle_file_errors(func: Callable) -> Callable:
    """Decorator for consistent file operation error handling."""
    @wraps(func)
    # *args / **kwargs let wrapper accept ANY arguments and forward
    # them to the wrapped function. *args = positional, **kwargs =
    # keyword. This makes the decorator usable on any signature.
    def wrapper(*args, **kwargs):
        try:
            # Run the real function and return whatever it returns.
            return func(*args, **kwargs)
        # If any of these errors happen during the call, we catch
        # them here, print a friendly message, and return None so
        # the caller can detect failure without a crash.
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return None
        except PermissionError as e:
            print(f"Error: Permission denied - {e}")
            return None
        except IOError as e:
            print(f"Error: I/O operation failed - {e}")
            return None
        except Exception as e:
            # Catch-all for anything else. We include the function
            # name in the message because this decorator is shared
            # by many functions and we want to know which one broke.
            print(f"Unexpected error in {func.__name__}: {e}")
            return None
    return wrapper


# Same decorator pattern, but this one VALIDATES inputs before
# letting the call proceed. It's narrower: it only works on methods
# whose first non-self arguments are (filename, content).
def validate_output(func: Callable) -> Callable:
    """Decorator to validate generated content before writing."""
    @wraps(func)
    # Note `self` is in the signature: this decorator targets METHODS,
    # not free functions. `self` is the instance, then filename/content.
    def wrapper(self, filename: str, content: str, *args, **kwargs):
        # Reject empty/whitespace-only content. .strip() removes
        # leading/trailing whitespace; if nothing's left the file
        # would be useless.
        if not content or not content.strip():
            raise ValueError(f"Empty content for {filename}")
        # Cap the size to avoid runaway writes. Arbitrary 10 KB limit
        # picked because training files are tiny.
        if len(content) > 10000:
            raise ValueError(f"Content too large for {filename}")
        # Validation passed -- forward to the real method.
        return func(self, filename, content, *args, **kwargs)
    return wrapper


class DataTemplates:
    """Centralized template definitions with metadata."""

    # ------------------------------------------------------------------
    # @staticmethod: this method belongs to the class but doesn't take
    # `self` or `cls`. It's basically a normal function grouped under
    # the class for organization. You call it as
    # DataTemplates.get_templates(). The return type is a Dict mapping
    # str -> nested Dict.
    # ------------------------------------------------------------------
    @staticmethod
    def get_templates() -> Dict[str, Dict[str, Union[str, List[str]]]]:
        """Returns all available data templates."""
        # A big dict literal: each key is the template name, each
        # value is a nested dict with content + metadata. Putting
        # all the source-of-truth data in one place makes it easy
        # to add a new template later -- just add a new key here.
        return {
            "ancient_fragment": {
                # `content` is a list of lines; the writer joins them
                # with "\n" later. Keeping them as a list keeps the
                # source readable (no big multi-line string).
                "content": [
                    "[FRAGMENT 001] Digital preservation protocols "
                    "established 2087",
                    "[FRAGMENT 002] Knowledge must survive the entropy "
                    "wars",
                    "[FRAGMENT 003] Every byte saved is a victory against "
                    "oblivion"
                ],
                "type": "historical_data",
                "encoding": "utf-8"
            },
            "classified_data": {
                "content": [
                    "[CLASSIFIED] Quantum encryption keys recovered",
                    "[CLASSIFIED] Archive integrity: 100%"
                ],
                "type": "security_data",
                "classification": "restricted"
            },
            # Some templates have content as a single string instead of
            # a list. The writer handles both shapes (see _format_content).
            "security_protocols": {
                "content": "[CLASSIFIED] New security protocols archived",
                "type": "protocol_data",
                "version": "3.1.0"
            },
            "standard_archive": {
                "content": "Knowledge preserved for humanity",
                "type": "standard_data",
                "status": "active"
            },
            "corrupted_archive": {
                "content": "DATA_CORRUPTION_ERROR_0x7F4A",
                "type": "error_simulation",
                "error_code": "0x7F4A"
            }
        }


class ArchiveDataGenerator:
    """Main data generation class with comprehensive file operations."""

    # ------------------------------------------------------------------
    # __init__: the constructor. Runs every time we do
    # ArchiveDataGenerator(...). Sets up per-instance state.
    # `base_path: Optional[str]` means it can be a string OR None.
    # The default `None` lets callers do ArchiveDataGenerator() with
    # no args, in which case we fall back to "." (current directory).
    # ------------------------------------------------------------------
    def __init__(self, base_path: Optional[str] = None) -> None:
        """Initialize generator with optional base path."""
        # Ternary: pick Path(base_path) if given, else Path(".").
        # Path is from pathlib -- a modern way to handle file paths.
        # Path("a") / "b" gives Path("a/b") regardless of OS.
        self.base_path = Path(base_path) if base_path else Path(".")
        # Cache the templates dict on the instance so we don't call
        # the static method again every time we need a template.
        self.templates = DataTemplates.get_templates()
        # Track which files we've successfully written. Initialized
        # empty; populated by _write_file.
        self.generated_files: List[str] = []

        # Make sure the target directory exists. parents=True creates
        # missing intermediate folders; exist_ok=True means "no error
        # if it already exists". Wrapped in try because mkdir can
        # fail (e.g. permissions) and we don't want a crash here.
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create base directory: {e}")

    # ------------------------------------------------------------------
    # Decorator stack reads BOTTOM-UP (closest to def runs first):
    # 1. @handle_file_errors wraps _write_file with error handling.
    # 2. @validate_output then wraps THAT with input validation.
    # So at call time: validate_output -> handle_file_errors -> body.
    # The leading underscore (_write_file) is a Python convention
    # meaning "intended for internal use only".
    # ------------------------------------------------------------------
    @validate_output
    @handle_file_errors
    def _write_file(self, filename: str, content: str) -> bool:
        """Write content to file with comprehensive error handling."""
        # Build the full path: base_path/filename. The `/` operator
        # on Path objects joins path components in a portable way.
        file_path = self.base_path / filename

        # `with` ensures the file gets closed even if write() raises.
        # encoding="utf-8" makes us explicit about text encoding so
        # accented characters/emoji round-trip safely.
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        # Bookkeeping + user feedback.
        self.generated_files.append(filename)
        print(f"Generated: {filename}")
        return True

    # ------------------------------------------------------------------
    # Helper: take a template's "content" field and produce a single
    # string ready to be written to disk. Handles different shapes:
    # list of lines, single string, or anything else (fallback).
    # ------------------------------------------------------------------
    def _format_content(self, template_data: Dict[str, Any]) -> str:
        """Format template content into string representation."""
        # .get("content", "") returns the value or "" if missing --
        # safer than template_data["content"] which would KeyError.
        content = template_data.get("content", "")

        # Branch on the runtime type of content.
        if isinstance(content, list):
            # Join the list with newlines: ["a","b"] -> "a\nb".
            return "\n".join(content)
        elif isinstance(content, str):
            # Already a string -- return as-is.
            return content
        else:
            # Defensive fallback: cast anything else (number, etc.)
            # to its string form.
            return str(content)

    # ------------------------------------------------------------------
    # The next five methods follow the same pattern: pick a template,
    # format it, and write it under a fixed filename. The decorator
    # turns any unexpected exception into a clean None return.
    # Optional[bool] means "either bool or None" (None on error).
    # ------------------------------------------------------------------
    @handle_file_errors
    def generate_ancient_fragment(self) -> Optional[bool]:
        """Generate ancient fragment training file."""
        template = self.templates["ancient_fragment"]
        content = self._format_content(template)
        return self._write_file("ancient_fragment.txt", content)

    @handle_file_errors
    def generate_classified_data(self) -> Optional[bool]:
        """Generate classified data training file."""
        template = self.templates["classified_data"]
        content = self._format_content(template)
        return self._write_file("classified_data.txt", content)

    @handle_file_errors
    def generate_security_protocols(self) -> Optional[bool]:
        """Generate security protocols training file."""
        template = self.templates["security_protocols"]
        content = self._format_content(template)
        return self._write_file("security_protocols.txt", content)

    @handle_file_errors
    def generate_standard_archive(self) -> Optional[bool]:
        """Generate standard archive training file."""
        template = self.templates["standard_archive"]
        content = self._format_content(template)
        return self._write_file("standard_archive.txt", content)

    @handle_file_errors
    def generate_corrupted_archive(self) -> Optional[bool]:
        """Generate corrupted archive simulation file."""
        template = self.templates["corrupted_archive"]
        content = self._format_content(template)
        return self._write_file("corrupted_archive.txt", content)

    # ------------------------------------------------------------------
    # Special generator: produces a JSON config file describing all
    # the templates and test scenarios. Demonstrates building a
    # nested dict in code and turning it into JSON text.
    # ------------------------------------------------------------------
    @handle_file_errors
    def generate_sample_json(self) -> Optional[bool]:
        """Generate JSON configuration with metadata and scenarios."""
        # Build a nested dict that will be serialized to JSON. JSON
        # natively supports str/int/float/bool/None/list/dict, which
        # is exactly what we use here.
        sample_data = {
            "metadata": {
                "version": "2.1.0",
                # Current time as an ISO-8601 string, e.g.
                # "2026-05-08T12:34:56.789012". JSON has no native
                # datetime type, so we use string representation.
                "generated": datetime.now().isoformat(),
                "generator": "ArchiveDataGenerator"
            },
            "file_types": [
                "ancient_fragment",
                "classified_data",
                "standard_archive"
            ],
            "test_scenarios": [
                {
                    "name": "basic_recovery",
                    "files": ["ancient_fragment.txt"],
                    "description": "Basic file reading operations"
                },
                {
                    "name": "secure_access",
                    "files": ["classified_data.txt"],
                    "description": "Secure file handling with context "
                                   "managers"
                },
                {
                    "name": "crisis_response",
                    "files": [
                        "standard_archive.txt",
                        "corrupted_archive.txt"
                    ],
                    "description": "Error handling and exception "
                                   "management"
                }
            ],
            # Dict comprehension: build a dict by iterating over
            # self.templates.items(). For each (name, template) pair,
            # produce a key=name with a small summary value.
            # Equivalent to a for-loop that does result[name] = {...}.
            "templates": {
                name: {
                    "type": template.get("type", "unknown"),
                    # bool(...) converts truthy/falsy to True/False.
                    # Empty string or missing -> False; non-empty -> True.
                    "has_content": bool(template.get("content"))
                }
                for name, template in self.templates.items()
            }
        }

        try:
            # json.dumps converts the dict into a JSON-formatted str.
            # indent=2 pretty-prints with 2-space indentation.
            # ensure_ascii=False keeps non-ASCII chars as-is instead
            # of escaping them to \uXXXX.
            json_content = json.dumps(
                sample_data,
                indent=2,
                ensure_ascii=False
            )
            return self._write_file("sample_data.json", json_content)
        except (TypeError, ValueError) as e:
            # TypeError: non-serializable object (rare here).
            # ValueError: invalid value in serialization.
            # Tuple of exceptions catches either with one branch.
            print(f"Error serializing JSON data: {e}")
            return None

    # ------------------------------------------------------------------
    # Orchestrator: runs all the individual generators in sequence
    # and reports which succeeded.
    # ------------------------------------------------------------------
    def generate_all_files(self) -> Dict[str, bool]:
        """Generate all training files and return success status."""
        print("=== CYBER ARCHIVES - DATA GENERATOR ===")
        print("Generating training files...")
        print()

        # List of (function_object, description) tuples. We store
        # the function ITSELF (no parens) so we can call it later in
        # the loop. Treating functions as data is a powerful Python
        # idiom -- functions are first-class objects.
        generators = [
            (self.generate_ancient_fragment, "Ancient fragment data"),
            (self.generate_classified_data, "Classified security data"),
            (self.generate_security_protocols,
             "Security protocol definitions"),
            (self.generate_standard_archive, "Standard archive content"),
            (self.generate_corrupted_archive, "Corrupted data simulation"),
            (self.generate_sample_json, "JSON configuration sample")
        ]

        results = {}
        successful = 0

        # Loop over the generators. Each one returns True on success
        # or None (via the decorator) on failure.
        for generator_func, description in generators:
            try:
                # () actually calls the function we stored above.
                result = generator_func()
                # `is not None`: the decorator returns None on errors,
                # so non-None means it ran to completion.
                results[generator_func.__name__] = result is not None
                if result:
                    successful += 1
            except Exception as e:
                # Belt-and-suspenders: even if a decorator missed
                # something, the loop won't crash mid-batch.
                print(f"Failed to generate {description}: {e}")
                results[generator_func.__name__] = False

        print()
        print(f"Generation complete: {successful}/{len(generators)} "
              f"files created successfully")

        if successful == len(generators):
            print("All training files ready for Data Archivist exercises")
        else:
            print("Some files failed to generate - check error messages "
                  "above")

        return results

    # ------------------------------------------------------------------
    # Simple accessor. Returns a COPY (.copy()) so callers can't
    # accidentally mutate our internal list. This is a small
    # defensive-coding habit -- mutable internal state should never
    # leak by reference unless intentional.
    # ------------------------------------------------------------------
    def get_generated_files(self) -> List[str]:
        """Return list of successfully generated files."""
        return self.generated_files.copy()

    # ------------------------------------------------------------------
    # Cleanup helper: deletes every file we created. Useful for tests
    # or when you want to regenerate from scratch. Returns the count
    # of files actually deleted.
    # ------------------------------------------------------------------
    def cleanup_generated_files(self) -> int:
        """Remove all generated files and return count of deleted files."""
        deleted_count = 0

        for filename in self.generated_files:
            try:
                # Path / filename builds the full path again.
                file_path = self.base_path / filename
                # .exists() returns True if the file is still there.
                # Avoids unlink() raising FileNotFoundError.
                if file_path.exists():
                    # .unlink() is the Path equivalent of os.remove.
                    file_path.unlink()
                    deleted_count += 1
            except Exception as e:
                print(f"Could not delete {filename}: {e}")

        # Empty the tracking list since the files are gone.
        self.generated_files.clear()
        return deleted_count


# ---------------------------------------------------------------------
# Entry point: gets called when the script is run directly.
# Encapsulates argument parsing, generation, and exit codes.
# Wrapped in a function (rather than top-level code) so it can be
# imported and called from elsewhere without side-effects.
# ---------------------------------------------------------------------
def main() -> None:
    """Main entry point with command-line argument handling."""
    try:
        # sys.argv is the list of command-line args. argv[0] is the
        # script name, so the first user-supplied arg is argv[1].
        # If no arg, default base_path to None (= current directory).
        base_path = sys.argv[1] if len(sys.argv) > 1 else None

        # Build the generator and run all generators.
        generator = ArchiveDataGenerator(base_path)
        results = generator.generate_all_files()

        # all() returns True only if EVERY value is truthy. Pick an
        # exit code: 0 = success, 1 = failure (Unix convention).
        # Shell scripts rely on this to know whether the run worked.
        if all(results.values()):
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        # Ctrl-C raises KeyboardInterrupt. We catch it so the user
        # gets a clean message instead of a scary traceback.
        # 130 is the conventional exit code for "killed by SIGINT".
        print("\nGeneration interrupted by user")
        sys.exit(130)
    except Exception as e:
        # Last-resort catch for anything not handled deeper. Without
        # this, an unexpected error would print a traceback, which
        # is ugly for end users (debugging-wise it's still helpful).
        print(f"Fatal error: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------
# The classic `if __name__ == "__main__":` guard. When this file is
# executed directly (python3 data_generator.py), __name__ equals
# "__main__" and main() runs. When the file is imported as a module
# (import data_generator), __name__ equals "data_generator" and
# main() does NOT run -- the importer just gets the classes.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
