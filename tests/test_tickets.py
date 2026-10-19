"""Run with:  python3 -m unittest -v      (from the repo root)

Don't edit these tests. They describe what the code is supposed to do.
"""
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from fogline_tickets.checksum import checksum
from fogline_tickets.codes import normalize_player, player_code
from fogline_tickets.hours import hours_from_minutes
from fogline_tickets.loader import load_tickets
from fogline_tickets.timeparse import parse_timestamp

SAMPLE = Path(__file__).resolve().parent / "fixtures" / "sample.csv"
UTC = timezone.utc


class LoaderTests(unittest.TestCase):
    def test_reads_every_ticket(self):
        ids = [t.ticket_id for t in load_tickets(SAMPLE)]
        self.assertEqual(ids, ["FOG-0001", "FOG-0002", "FOG-0003", "FOG-0004"])

    def test_quoted_titles_keep_their_commas(self):
        self.assertEqual(load_tickets(SAMPLE)[1].title, "Projector in B12 shows only purple, again")


class TimestampTests(unittest.TestCase):
    def test_utc(self):
        self.assertEqual(parse_timestamp("2026-03-14T16:15:00Z"), datetime(2026, 3, 14, 16, 15, tzinfo=UTC))

    def test_negative_offset(self):
        # 09:15 at the Net Loft (UTC-7) is 16:15 UTC.
        self.assertEqual(parse_timestamp("2026-03-14T09:15:00-07:00"), datetime(2026, 3, 14, 16, 15, tzinfo=UTC))

    def test_positive_offset(self):
        # 10:00 at Skerry Systems (UTC+1) is 09:00 UTC.
        self.assertEqual(parse_timestamp("2026-06-02T10:00:00+01:00"), datetime(2026, 6, 2, 9, 0, tzinfo=UTC))

    def test_resolution_time_across_zones(self):
        first = load_tickets(SAMPLE)[0]  # opened 16:00 UTC, closed 11:15 at the Net Loft (18:15 UTC)
        self.assertEqual(first.minutes, 135)


class HoursTests(unittest.TestCase):
    def test_whole_and_half_hours(self):
        self.assertEqual(hours_from_minutes(60), Decimal("1.0"))
        self.assertEqual(hours_from_minutes(90), Decimal("1.5"))

    def test_halves_round_up(self):
        self.assertEqual(hours_from_minutes(135), Decimal("2.3"))  # 2.25 h
        self.assertEqual(hours_from_minutes(9), Decimal("0.2"))  # 0.15 h

    def test_ordinary_rounding(self):
        self.assertEqual(hours_from_minutes(100), Decimal("1.7"))  # 1.666... h
        self.assertEqual(hours_from_minutes(5), Decimal("0.1"))  # 0.083... h


class ChecksumTests(unittest.TestCase):
    def test_sample_checksum(self):
        self.assertEqual(checksum(load_tickets(SAMPLE)), "c1ee68504a4f8e14")


class CodeTests(unittest.TestCase):
    def test_player_ids_are_normalized(self):
        self.assertEqual(normalize_player(" p-7q2k "), "P-7Q2K")
        self.assertEqual(normalize_player("7Q2K"), "P-7Q2K")

    def test_code_is_stable(self):
        self.assertEqual(player_code("0123456789abcdef", "P-7Q2K"), "AIDAY{SPUR-ELVES-51}")


if __name__ == "__main__":
    unittest.main()
