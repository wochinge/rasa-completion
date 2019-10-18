import subprocess
import time
from pathlib import Path
from sys import argv
import re
import json
from typing import Text, List, Dict

max_caching_time = 345_600  # 4 weeks
cache_file_path = Path.home() / ".rasa-autocomplete.json"

EXPECTED_ARGUMENT_ERROR = "expected one argument"


def find_positional_arguments(text: Text) -> List[Text]:
    pattern = r"{(.*)}"
    regex = re.compile(pattern)
    matched = regex.search(text)
    if matched:
        return matched.group(1).strip().split(",")
    else:
        return []


def find_optional_arguments(text: Text) -> List[Text]:
    pattern = r"[^\[](--[^\s]+)"
    regex = re.compile(pattern)
    matched = regex.findall(text)
    return [match.strip() for match in matched]


def call_rasa(command: List[Text]) -> Text:
    command.append("--help")
    return subprocess.check_output(
        command, shell=False, stderr=subprocess.PIPE
    ).decode("utf-8")


def call_rasa_until_valid(command: Text) -> Text:
    command_as_array = command.split()

    try:
        return call_rasa(command_as_array.copy())
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode("utf-8")
        if EXPECTED_ARGUMENT_ERROR in error_output:
            # An argument is expected (e.g. a path, port, etc.)
            return ""
        else:
            return call_rasa(command_as_array[:-1])


def get_cache() -> Dict:
    if cache_file_path.exists():
        content = cache_file_path.read_text(encoding="utf-8")
        return json.loads(content)
    else:
        return {}


def store_cache(command: Text, arguments: List[Text], current_cache: Dict) -> None:
    import os

    if os.environ.get("RASA_AUTOCOMPLETE_CACHING_OFF"):
        return

    current_cache[command] = {"args": arguments, "timestamp": time.time()}
    dumped = json.dumps(current_cache)
    cache_file_path.touch()
    cache_file_path.write_text(dumped, encoding="utf-8")


if __name__ == "__main__":
    current_command = argv[1]

    cached = get_cache()
    cached_result = cached.pop(current_command, None)
    if not cached_result or time.time() - cached_result["timestamp"] > max_caching_time:
        help_input = call_rasa_until_valid(current_command)

        positional_arguments = find_optional_arguments(help_input)
        optional_arguments = find_positional_arguments(help_input)
        possibilities = positional_arguments + optional_arguments
    else:
        possibilities = cached_result["args"]

    store_cache(current_command, possibilities, cached)

    for possibility in possibilities:
        print(possibility)
