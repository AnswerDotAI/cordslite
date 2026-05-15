"""Load this skill when an agent needs to search, summarize, or find information in Discord using cordslite. It covers read-only workflows for connecting to Discord, opening a guild, orienting through channels, searching messages, reading threads, and fetching attachments.

Connections to Discord use `DiscordClient`: `dc_ = DiscordClient(token=None, user_token=None)`. If `token` is `None`, cordslite reads the bot token from the `DISCORD_BOT_TOKEN` environment variable. `user_token` can be supplied for cordslite operations that support `use_user=True`, or defaults to the `DISCORD_USER_TOKEN` environment variable when present. Once connected, open a guild with `gld_ = await dc_.guild(guild_id)`, where `guild_id` is provided by the user.

This skill treats Discord as a read-only information source. It does not cover posting, editing, deleting, creating threads, or other write operations, even when cordslite exposes those methods.

# Orienting in a guild

Start by getting a compact map of the guild before searching: `print(await guild_tree(gld_))`. Use this to identify likely channels, categories, channel IDs, and topic text.

Discord channel objects include `id`, `name`, `type`, `parent_id`, and sometimes `topic`. Categories have `type == 4`; text channels usually have `type == 0`; `parent_id` links a channel to its category. Use channel topics as hints for where a conversation probably belongs, but do not assume a topic is exhaustive.

For repeated work, build channel maps from `await gld_.channels()`: `chs_ = await gld_.channels()`, then map by name or ID as needed.

# Searching messages

`Channel.messages(limit=...)` calls Discord's channel messages endpoint, which returns newest-to-oldest; cordslite reverses that response, so the returned `Messages` list is chronological within the fetched batch. `Channel.messages(before=..., after=..., around=...)` can also read local context around a message ID or `Message` object, and still returns messages chronologically. Search methods usually return newest-first unless `sort_order` changes them. Sort by `timestamp` before writing timelines or summaries.

Use guild search when the relevant channel is unknown: `msgs_ = await gld_.search(content='term', after='2026-05-01', limit=25)`. Use channel search when `guild_tree` points to a likely channel: `msgs_ = await ch_.search(content='term', after='2026-05-01', limit=25)`.

`before` and `after` accept `'YYYY-MM-DD'` strings for search methods. Prefer date strings over snowflake IDs unless the task specifically involves Discord internals.

Use `search_all` when the first page is too thin or when summarizing activity over a time window: `msgs_ = await gld_.search_all(content='term', after='2026-05-01', limit=100)`. It paginates Discord search results in batches and returns a `Messages` list.

Useful filters include `content`, `author_id`, `channel_id`, `mentions`, `has`, `before`, `after`, and `pinned`. Use `author_id_ = await gld_.find_member('name')` when searching for messages by a person.

Discord search is not proof of absence. If a search returns nothing, try concrete alternate terms: project names, usernames, abbreviations, filenames, error strings, URLs, and likely channel scopes. For "what happened recently," use `guild_tree` to pick likely channels, read recent channel messages where appropriate, and use search to find named topics, people, files, or decisions across the date range.

# Reading messages and threads

Use `await ch_.messages(limit=50)` to read the latest visible flow of a channel or thread. The returned messages are chronological within the fetched batch, making them suitable for catch-up summaries.

Search results may not include enough surrounding context. When a search hit matters, use `await msg_.before(limit=5)`, `await msg_.after(limit=5)`, or `await msg_.around(limit=11)` to inspect nearby messages in the same channel or thread.

When working from a channel object, use `await ch_.messages(before=msg_, limit=5)`, `await ch_.messages(after=msg_, limit=5)`, or `await ch_.messages(around=msg_, limit=11)`. These parameters use message IDs or `Message` objects, not date strings.

Threads are channels. Fetch a known thread with `thread_ = await dc_.thread(thread_id)` and read it with `msgs_ = await thread_.messages(limit=50)`. If a search result's `channel_id` does not match the known guild channel map, treat it as a likely thread and fetch it with `dc_.thread(...)`.

Use `msg_.content` for readable mention-expanded text. Use `msg_.raw_content` when the original Discord syntax matters.

# Attachments

Message attachments are available as metadata through `msg_.attachments`. Inspect `filename`, `size`, `content_type`, and `url` before fetching contents.

Call `data_ = await att_.fetch()` only when the task requires the file bytes. Decode text-like files when appropriate; for images, PDFs, audio, archives, or other binary files, save or display the bytes according to the task environment.

Use attachment searches to find files directly: `msgs_ = await gld_.search(has='file', after='2026-05-01', limit=25)`. Use `has='image'` when looking specifically for image attachments.

# Citations and reporting

Use `msg_.url` for message citations. Guilds and channels also have `.url`, but factual claims should usually cite the specific message or thread message that supports them. Use markdown syntax for links so the full url doesn't overwhelm your report.

When summarizing, include dates, authors, channel names, and message links. Sort relevant messages by `timestamp` before describing a sequence of events.

Prefer concise summaries over pasted chat logs. Quote only short fragments when wording matters; otherwise paraphrase and cite the source message.

If the evidence is thin, say what was searched: terms, date range, channels, people, and attachment filters. Do not turn "no result for this query" into "this never happened."

# Task patterns

For "what happened recently?" / catch-up requests, start with guild search:

    msgs = await gld_.search_all(after='YYYY-MM-DD', limit=500)

Then filter locally for the exact time window if needed. `search_all(after=...)` accepts date strings.

Do not start by scraping every channel with `Channel.messages(...)` unless search is inadequate or you need full non-indexed channel flow. `Channel.messages(after=...)` expects a message ID / snowflake / Message object, not a date string.

For "find where this was discussed," start guild-wide with the most specific term, then retry with synonyms, abbreviations, usernames, filenames, URLs, and likely channel scopes. Use `msg_.around(...)` on important hits before reporting.

For "what did person X say about topic Y," resolve the person with `author_id_ = await gld_.find_member('name')`, search by `author_id` plus topic terms, then widen to topic-only searches in case others quoted or replied to them.

For "find a file/image," search with `has='file'` or `has='image'`, combine with likely filenames or topic terms, inspect attachment metadata, and fetch bytes only when needed.

Search and `.messages()` results include bot metadata in `m.author`. To summarize human activity separately from tool/bot chatter:

    human_msgs_ = [ m for m in msgs_
                    if not (isinstance(m.author, dict) and m.author.get('bot', False))]

# Gotchas

Discord search can miss relevant messages, return thin snippets, or rank recent-but-less-useful hits first. Treat search as a way to gather candidates, not as proof that something exists or does not exist.

Search results may lack surrounding context. Read nearby messages, the relevant channel, or the relevant thread when the answer depends on replies, decisions, or sequence.

`Channel.messages(before=..., after=..., around=..., limit=...)` uses message IDs or `Message` objects, not date strings. Use search `before` and `after` for date windows. Discord requires `limit <= 100`; larger values raise `DiscordError(400): [50035] Invalid Form Body`.

`search(...)` and `search_all(...)` are better for date windows and older material, but they are keyword-driven. For catch-up tasks, combine recent channel reads with targeted searches.

Message timestamps come back as strings, not `datetime` objects.

Many search results may come from threads. Thread IDs often will not appear in `await gld_.channels()`. If a `channel_id` does not resolve, fetch it as a thread:

    thread = await dc_.thread(str(m.channel_id))
    name = thread.name

Some cordslite methods write to Discord. This skill does not use `send`, `delete`, `bulk_delete`, `search_and_delete_all`, `create_dm`, or `create_thread`.
"""
from fastcore.utils import patch
from pyskills.core import allow
from cordslite.core import (Attachment, Channel, Channels, date2snowflake, DiscordClient, 
                            Guild, Message, Messages)

__all__ = [ 'DiscordClient', 'Guild', 'Channel', 'Channels', 'Message', 'Messages',
            'Attachment', 'date2snowflake', 'guild_tree']

async def guild_tree(gld, dc=None, show_ids=True, show_topics=True, include_voice=False,
                     include_empty_categories=False, topic_len=100):
    "Return a tree-style overview of a Discord guild's channel hierarchy."
    if isinstance(gld, str):
        if dc is None: raise ValueError("Pass `dc` when `gld` is a guild ID")
        gld = await dc.guild(gld)

    chs = await gld.channels()
    by_parent,cats = {},[]

    def label(c):
        typ = {0: "#", 2: "voice ", 4: ""}.get(c.type, f"type{c.type} ")
        name = f"{typ}{c.name}"
        if show_ids: name += f" [{c.id}]"
        topic = c.get("topic")
        if show_topics and topic:
            topic = " ".join(topic.split())
            if len(topic) > topic_len: topic = topic[:topic_len-1] + "..."
            name += f" -- {topic}"
        return name

    for c in chs:
        if c.type == 4: cats.append(c)
        elif c.type == 0 or include_voice:
            by_parent.setdefault(c.get("parent_id"), []).append(c)

    lines = [f"{gld.name} [{gld.id}]" if show_ids else gld.name]
    for cat in sorted(cats, key=lambda c: c.get("position", 0)):
        kids = sorted(by_parent.pop(cat.id, []), key=lambda c: c.get("position", 0))
        if not kids and not include_empty_categories: continue
        lines.append(f"|-- {label(cat)}")
        for i,ch in enumerate(kids):
            branch = "`--" if i == len(kids)-1 else "|--"
            lines.append(f"|   {branch} {label(ch)}")

    all_orphans = sorted(by_parent.pop(None, []), key=lambda c: c.get("position", 0))
    all_orphans += sorted([c for cs in by_parent.values() for c in cs], key=lambda c: c.get("position", 0))
    if all_orphans:
        lines.append("|-- Uncategorized")
        for i,ch in enumerate(all_orphans):
            branch = "`--" if i == len(all_orphans)-1 else "|--"
            lines.append(f"|   {branch} {label(ch)}")

    return "\n".join(lines)

allow(guild_tree, date2snowflake,
      {DiscordClient: ['guild', 'channel', 'thread'],
       Guild: ['channels', 'search', 'search_all', 'find_member', 'members'],
       Channel: ['messages', 'search', 'search_all'],
       Message: ['before', 'after', 'around'],
       Attachment: ['fetch']})
