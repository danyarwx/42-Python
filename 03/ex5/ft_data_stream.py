#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_data_stream.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 13:40:04 by dzhukov             #+#    #+#            #
#   Updated: 2026/05/28 14:08:47 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import random
from typing import Generator


def gen_event() -> Generator[tuple[str, str], None, None]:
    # generator keeps running forever and creates one random event on demand
    players = ["alice", "bob", "charlie", "dylan"]
    actions = ["run", "eat", "sleep", "grab", "move", "climb", "swim",
               "release", "use"]

    while True:
        name = random.choice(players)
        action = random.choice(actions)
        yield (name, action)


def consume(events:
            list[tuple[str, str]]) -> Generator[tuple[str, str], None, None]:
    # pick a random event from the list remove it then give it to the caller
    while len(events) > 0:
        index = random.randrange(len(events))
        event = events[index]
        del events[index]
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    # next asks the generator for one new event each time through the loop
    event_generator = gen_event()
    for i in range(1000):
        event = next(event_generator)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")

    # build a list from a new generator then consume it until it is empty
    list_generator = gen_event()
    events = []

    for i in range(10):
        events.append(next(list_generator))

    print(f"Built list of 10 events: {events}")

    for event in consume(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
