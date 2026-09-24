"""Read-only access to Discord through cordslite. Covers connecting, opening a guild, finding your way around its channels, searching messages, reading threads, and fetching attachments.

Read-only: never use cordslite's write methods (`send`, `delete`, `bulk_delete`, `search_and_delete_all`, `create_dm`, `create_thread`).

`dc = DiscordClient()` (`doc(DiscordClient)`: token sources); `gld = await dc.guild(guild_id)` for the guild the user names; `await dc.guilds()` lists the bot's guilds if the ID is unknown.

# Guild layout

Start with `print(await gld.tree())`: categories, their channels with IDs and topics, members. Topics hint where a conversation belongs but aren't exhaustive. For repeated lookups, map `await gld.channels()` by name/ID; `parent_id` = category, `ch.is_text` = text channel, `cordslite.core.ChannelType` names the rest. Threads are channels but absent from `gld.channels()`: `await gld.threads()`/`await ch.threads()` list active ones, `await dc.thread(thread_id)` fetches any; a message whose `channel_id` isn't in your map is probably in a thread.

# Getting messages

Two ways, with different behaviour:

- Search (`gld.search`, `ch.search`; `search_all` paginates when one page isn't enough): by keyword across dates. `before`/`after` take `'YYYY-MM-DD'` (clearer than snowflakes); filters `content`, `author_id`, `channel_id`, `mentions`, `has`, `pinned`. Newest first unless `sort_order`. Can miss messages, return thin snippets, and rank recent-but-weak hits first: results are candidates. `ch.search` omits that channel's threads; search the guild or the threads when replies matter.
- Channel reads (`await ch.messages(limit=50)`): a channel's or thread's messages, complete, oldest first; paged by message ID, not date. Search snippets lack context: when the answer depends on replies, decisions, or order, read around a hit with `await msg.before()`/`msg.after()`/`msg.around()`.

`msg.content` has mentions expanded to `@username`; `msg.raw_content` keeps Discord syntax. Timestamps are strings: sort by `timestamp` before describing a sequence. `m.author.is_bot` separates bots from humans. `await gld.find_member('name')` returns a user ID for `author_id`, or `None`.

`msg.attachments`: each file's `filename`, `size`, `content_type`, `url`; `await att.fetch()` only when the bytes are needed (decode text; handle binary as the environment allows). `has='file'`/`has='image'` finds messages with attachments.

# Task patterns

- Catching up: guild `search_all(after='YYYY-MM-DD')`, filter locally, then read the busiest channels with `ch.messages`; read every channel only if search falls short.
- Where was X discussed: guild search for the most specific term, then synonyms, abbreviations, usernames, filenames, error strings, URLs, likely channels; read around important hits.
- What person X said about Y: X's `author_id` + topic terms, then the topic alone (others may quote or reply to X).
- Finding a file: `has='file'`/`has='image'` + likely filenames or topic terms; check attachment metadata before fetching.

# Reporting

Cite the supporting message as a markdown link to `msg.url` (guilds/channels have `.url` too). Give dates, authors, channel names. Summarise; quote only short fragments where wording matters. With thin evidence, say what you searched (terms, date range, channels, people, attachment filters): no result doesn't mean it never happened.
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
