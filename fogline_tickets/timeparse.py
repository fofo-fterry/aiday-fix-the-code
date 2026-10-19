"""Timestamps in the helpdesk export.

They are ISO 8601 with seconds and a UTC offset, for example:

    2026-03-14T16:15:00Z        field-station loggers write UTC
    2026-03-14T09:15:00-07:00   the Net Loft writes local time (-08:00 in winter)
    2026-06-02T10:00:00+01:00   Skerry Systems writes UK time (+00:00 in winter)

All three of those examples are the same kind of thing: an instant. Compare them in UTC.
"""
from datetime import datetime, timezone

FORMAT = "%Y-%m-%dT%H:%M:%S"


def parse_timestamp(value):
    """Parse an export timestamp into a timezone-aware datetime in UTC."""
    value = value.strip()
    stamp = datetime.strptime(value[:19], FORMAT)  # the date and time; the zone comes after
    return stamp.replace(tzinfo=timezone.utc)
