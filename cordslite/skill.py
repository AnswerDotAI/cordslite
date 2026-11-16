# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
"""Read-only access to Discord through cordslite. Covers connecting, opening a guild, finding your way around its channels, searching messages, reading threads, and fetching attachments.

notation: /why

- read-only: never call a write method (`send`, `typing`, `delete`, `delete_message`, `bulk_delete`, `search_and_delete_all`, `create_dm`, `create_thread`, `create_webhook`)
- `dc = DiscordClient()`; `gld = await dc.guild(guild_id)`; ID unknown: `await dc.guilds()`

## Guild layout

- start: `print(await gld.tree())`; topics hint where a conversation belongs, not exhaustively
- repeated lookups: map `await gld.channels()` by name or ID; `parent_id`: category; kinds: `ch.is_text`, `cordslite.core.ChannelType`
- threads: channels, absent from `gld.channels()`; any by ID: `await dc.thread(id)`; unknown `channel_id`: probably a thread

## Messages

- search: newest first; prefer `'YYYY-MM-DD'` dates to snowflakes (clearer); hits are candidates    /can miss messages, give thin snippets, rank recent weak hits first
- `ch.search` skips that channel's threads: replies matter → `nothread=False`, or search guild
- complete history: `await ch.messages()`; answer depends on replies, decisions or order: read around hits (`await msg.around()`, `.before()`, `.after()`)    /snippets lack context
- `msg.content`: mentions as `@username`; `msg.raw_content`: Discord syntax
- timestamps: strings; sort by `timestamp` before describing a sequence
- bots: `m.author.is_bot`
- `msg.attachments`: `filename`, `size`, `content_type`, `url`; `await att.fetch()` only when bytes are needed

## Tasks

- catching up: guild `search_all(after='YYYY-MM-DD')`, filter locally → busiest channels via `ch.messages`; every channel only if search falls short
- where X was discussed: guild search, most specific term first → synonyms, abbreviations, usernames, filenames, error strings, URLs, likely channels; read around important hits
- what X said about Y: X's `author_id` (`await gld.find_member(name)`) + topic → topic alone    /others may quote or reply to X
- a file: `has='file'` or `has='image'` + likely filenames or topic; check metadata before fetching

## Reporting

- cite each supporting message: markdown link to `msg.url` (guilds, channels: `.url` too), with date, author, channel
- summarise; quote only short fragments where wording matters
- thin evidence: say what you searched (terms, dates, channels, people, attachment filters)    /no result ≠ never happened
"""
from fastcore.utils import patch
from pyskills.core import allow
from cordslite.core import (Attachment, Channel, Channels, DiscordClient, 
                            Guild, Message, Messages)

__all__ = [ 'DiscordClient', 'Guild', 'Channel', 'Channels', 'Message', 'Messages',
            'Attachment']

allow(DiscordClient.__init__,
      {DiscordClient: ['channel', 'thread', 'guild', 'guilds'],
       Guild: ['channels', 'search', 'search_all', 'find_member', 'members', 'tree', 'threads', 'url'],
       Channel: ['messages', 'search', 'search_all', 'threads', 'url'],
       Message: ['before', 'after', 'around', 'attachments', 'url'],
       Attachment: ['fetch']})
