# Fogline ticket checksum

*AI Action Day CTF: fictional content. The Fogline Institute, its people and its tickets are invented.*

Every Friday, Priya's dashboard checks a checksum of the IT helpdesk's tickets. Bram wrote this
script to compute it. His last commit message says "fixed. probably." Since then the numbers
haven't matched, and the tests have been red for weeks.

## Your mission

There are **three bugs**. Fix them so every test passes, then run:

```
python3 run.py --player P-7Q2K        # use your own Player ID from the CTF site
```

It prints your personal code, `AIDAY{WORD-WORD-NN}`. Submit it on the challenge page.

`run.py` prints a code even while it's broken. That code is wrong: the tests are failing for a reason.

## Getting started

```
cd aiday-fix-the-code                 # the folder you cloned or unzipped
python3 -m unittest -v                # see what fails
claude                                # then ask Claude Code to help
```

Python 3.8 or newer, standard library only, nothing to install. On Windows, use `py` instead of `python3`.

## What the code is supposed to do

- `data/tickets.csv` is the helpdesk export: one header row, then one row per ticket. There are
  42 tickets and every one counts.
- Timestamps are ISO 8601 with a UTC offset: `Z` from the field-station loggers, `-08:00` or
  `-07:00` from the Net Loft, `+00:00` or `+01:00` from Skerry Systems. Convert to UTC before
  doing any arithmetic.
- A ticket's resolution time is the whole minutes from opened to closed. Hours are minutes / 60
  to one decimal place, **rounded half up**: Fogline finance bills 2.25 h as 2.3 h, never 2.2.
- The checksum is SHA-256 over one line per ticket, sorted (`fogline_tickets/checksum.py`).
- Your code comes from the checksum plus your Player ID (`fogline_tickets/codes.py`).

## Rules

Fix the code in `fogline_tickets/`. Don't edit the tests, `data/tickets.csv`, `checksum.py` or
`codes.py`. The code only comes out right when the logic is right, so there's no shortcut there.

## Layout

```
run.py                      prints the summary and your code
fogline_tickets/loader.py   reads the CSV export into Ticket objects
fogline_tickets/timeparse.py  parses timestamps
fogline_tickets/hours.py    minutes to billable hours
fogline_tickets/checksum.py the checksum (correct as is)
fogline_tickets/codes.py    checksum + Player ID to code (correct as is)
fogline_tickets/words.py    the word list codes are made from
data/tickets.csv            the real export
tests/                      unit tests and a small sample export
```
