"""Modules:

- `cordslite.skill`: Read-only access to Discord through cordslite. Covers connecting, opening a guild, finding your way around its channels, searching messages, reading threads, and fetching attachments."""

__version__ = "0.1.1"
from .core import *
from .gateway import *
from .voice import *
from .bot import *
