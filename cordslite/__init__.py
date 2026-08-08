"""Modules:

- `cordslite.skill`: Load this skill when an agent needs to search, summarize, or find information in Discord using cordslite. It covers read-only workflows for connecting to Discord, opening a guild, orienting through channels, searching messages, reading threads, and fetching attachments."""

__version__ = "0.1.1"
from .core import *
from .gateway import *
from .voice import *
from .bot import *
