#!/usr/bin/env python3
"""Summarize Fogline's IT tickets and print your AI Action Day CTF code.

    python3 run.py --player P-7Q2K

AI Action Day CTF: fictional content.
"""
import argparse
import sys
from decimal import Decimal
from pathlib import Path

from fogline_tickets.checksum import checksum
from fogline_tickets.codes import normalize_player, player_code
from fogline_tickets.loader import load_tickets

HERE = Path(__file__).resolve().parent


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize Fogline's IT tickets and print your CTF code.")
    parser.add_argument("--player", required=True, help="your Player ID from the CTF site, like P-7Q2K")
    parser.add_argument("--csv", default=str(HERE / "data" / "tickets.csv"), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        player = normalize_player(args.player)
    except ValueError as e:
        parser.error(str(e))

    tickets = load_tickets(args.csv)
    for t in tickets:
        if t.minutes < 0:
            print("warning: {} was closed {} minutes before it was opened?".format(t.ticket_id, -t.minutes), file=sys.stderr)
    total = sum((Decimal(str(t.hours)) for t in tickets), Decimal(0))

    print("Tickets:      {}".format(len(tickets)))
    print("Total hours:  {}".format(total))
    print("Player:       {}".format(player))
    print("Your code:    {}".format(player_code(checksum(tickets), player)))
    print("(Trust it only once every test passes: python3 -m unittest)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
