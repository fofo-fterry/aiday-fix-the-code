"""The weekly ticket checksum Priya's dashboard compares against."""
import hashlib
from datetime import timezone


def ticket_line(ticket):
    """One canonical line per ticket: id | opened (UTC, to the minute) | minutes | hours."""
    opened = ticket.opened.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    return "{}|{}|{}|{:.1f}".format(ticket.ticket_id, opened, ticket.minutes, float(ticket.hours))


def checksum(tickets):
    """First 16 hex characters of SHA-256 over every ticket's line, sorted."""
    lines = sorted(ticket_line(t) for t in tickets)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]
