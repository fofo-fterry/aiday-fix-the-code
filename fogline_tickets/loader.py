"""Load Fogline IT tickets from the helpdesk's CSV export."""
import csv
from dataclasses import dataclass
from datetime import datetime

from .hours import hours_from_minutes
from .timeparse import parse_timestamp

COLUMNS = ("ticket_id", "title", "station", "reported_by", "opened_at", "closed_at")


@dataclass
class Ticket:
    ticket_id: str
    title: str
    station: str
    reported_by: str
    opened: datetime
    closed: datetime

    @property
    def minutes(self):
        """Whole minutes from opened to closed."""
        return int((self.closed - self.opened).total_seconds() // 60)

    @property
    def hours(self):
        """Resolution time in hours, rounded the Fogline way (see hours.py)."""
        return hours_from_minutes(self.minutes)


def load_tickets(path):
    """Every ticket in the CSV export at `path`, in file order."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header = [h.strip() for h in rows[0]]
    missing = [c for c in COLUMNS if c not in header]
    if missing:
        raise ValueError("CSV is missing columns: " + ", ".join(missing))
    col = {name: header.index(name) for name in COLUMNS}

    tickets = []
    # rows[0] is the header; the tickets run from row 1 to the end.
    for i in range(1, len(rows) - 1):
        row = rows[i]
        if not row:
            continue
        tickets.append(
            Ticket(
                ticket_id=row[col["ticket_id"]].strip(),
                title=row[col["title"]].strip(),
                station=row[col["station"]].strip(),
                reported_by=row[col["reported_by"]].strip(),
                opened=parse_timestamp(row[col["opened_at"]]),
                closed=parse_timestamp(row[col["closed_at"]]),
            )
        )
    return tickets
