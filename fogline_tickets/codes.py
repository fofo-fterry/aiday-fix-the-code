"""Turns the checksum and your Player ID into your CTF code. There is nothing to fix in here."""
import hashlib
import re

from .words import WORDS

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def normalize_player(raw):
    """'p-7q2k', '7Q2K' and ' P-7Q2K ' all mean P-7Q2K."""
    s = re.sub(r"^P[-_ ]?", "", raw.strip().upper())
    s = s.replace("O", "0").replace("I", "1").replace("L", "1")
    if len(s) != 4 or any(c not in CROCKFORD for c in s):
        raise ValueError("Player IDs look like P-7Q2K. Copy yours from the header of the CTF site.")
    return "P-" + s


def player_code(checksum, player):
    """AIDAY{WORD-WORD-NN} from SHA-256 of 'checksum:player'."""
    digest = hashlib.sha256("{}:{}".format(checksum, player).encode("utf-8")).digest()
    first = WORDS[int.from_bytes(digest[0:2], "big") % len(WORDS)]
    second = WORDS[int.from_bytes(digest[2:4], "big") % len(WORDS)]
    return "AIDAY{%s-%s-%02d}" % (first, second, digest[4] % 100)
