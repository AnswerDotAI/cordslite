#!/usr/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "cordslite>=0.0.16",  # dc.guilds() is new in 0.0.16
#   "textual>=1.0",
# ]
# ///

"""A cute little TUI for recording Discord voice channels.

Usage:
    uv run recorder_tui.py

Set DISCORD_BOT_TOKEN first; ffmpeg must be on PATH. Browse to a voice channel
(occupants shown live), press Enter to join + record, `s` to stop, `m` to
toggle mixing, `q` to quit. The input at the bottom is the output path
template: {guild}, {channel}, and {ts} are filled in when recording starts.
"""

import asyncio, re, time
from collections import defaultdict
from contextlib import suppress
from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Static, Tree

from cordslite.core import Channel, DiscordClient, GatewayClient, Guild, VoiceClient

INTENTS = (1 << 0) | (1 << 7)  # GUILDS | GUILD_VOICE_STATES


def slug(s): return re.sub(r'[^\w-]+', '_', s).strip('_')


class RecorderTUI(App):
    TITLE = 'cordslite recorder'
    CSS = """
    Tree { height: 1fr; }
    #status { height: 1; padding: 0 1; background: $boost; }
    """
    BINDINGS = [('s', 'stop', 'Stop recording'), ('m', 'toggle_mix', 'Toggle mix'), ('q', 'quit', 'Quit')]

    def __init__(self):
        super().__init__()
        self.dc = self.gc = self.vc = self.rec_start = None
        self.mix, self.rec_label = True, ''
        self.occupants = defaultdict(set)  # channel_id -> {user_id}
        self.user_ch, self.names = {}, {}  # user_id -> channel_id, user_id -> display name
        self.ch_nodes, self.glds = {}, {}  # channel_id -> TreeNode, guild_id -> Guild

    def compose(self) -> ComposeResult:
        yield Header()
        yield Tree('guilds')
        yield Input(value='recordings/{guild}_{channel}_{ts}.mp3', id='out')
        yield Static(id='status')
        yield Footer()

    def status(self, msg): self.query_one('#status', Static).update(msg)

    async def on_mount(self):
        self.status('Connecting to Discord…')
        self.dc = DiscordClient(name='recorder-tui')
        self.gc = GatewayClient(INTENTS, self.dc)
        self.gc.on('GUILD_CREATE', self.on_guild_create)
        self.gc.on('VOICE_STATE_UPDATE', self.on_voice_state)
        await self.gc.start()
        tree = self.query_one(Tree)
        for gld in await self.dc.guilds():
            self.glds[gld.id] = gld
            tree.root.add(gld.name, data=gld)
        tree.root.expand()
        self.set_interval(1, self.tick)
        self.status('Pick a voice channel and press Enter to record')

    # -- guild/channel tree ---------------------------------------------------

    async def on_tree_node_expanded(self, event: Tree.NodeExpanded):
        gld = event.node.data
        if not isinstance(gld, Guild) or event.node.children: return
        for ch in await gld.channels():
            if ch.type != 2: continue  # voice channels only
            self.ch_nodes[ch.id] = event.node.add(f'🔊 {ch.name}', data=ch)
            await self.refresh_members(ch.id)

    async def refresh_members(self, cid):
        node = self.ch_nodes.get(cid)
        if node is None: return
        node.remove_children()
        for uid in sorted(self.occupants.get(cid, ())):
            node.add_leaf(await self.member_name(uid, node.data.guild_id))
        if self.occupants.get(cid): node.expand()

    # NB: don't call this `name` -- that shadows textual's DOMNode.name and breaks App repr
    async def member_name(self, uid, gid):
        if uid not in self.names:
            try:
                m = await self.glds[gid]('GET', f'/guilds/{gid}/members/{uid}')
                u = m.get('user', {})
                self.names[uid] = m.get('nick') or u.get('global_name') or u.get('username') or uid
            except Exception: self.names[uid] = uid
        return self.names[uid]

    # -- voice state tracking -------------------------------------------------

    async def on_guild_create(self, gld):
        for vs in gld.get('voice_states', []): await self.move(vs['user_id'], vs.get('channel_id'))

    async def on_voice_state(self, d):
        m = d.get('member') or {}
        u = m.get('user') or {}
        if nm := (m.get('nick') or u.get('global_name') or u.get('username')): self.names[d['user_id']] = nm
        await self.move(d['user_id'], d.get('channel_id'))

    async def move(self, uid, cid):
        old = self.user_ch.pop(uid, None)
        if old: self.occupants[old].discard(uid)
        if cid:
            self.user_ch[uid] = cid
            self.occupants[cid].add(uid)
        for c in {old, cid} - {None}: await self.refresh_members(c)

    def chain_voice_handler(self):
        # gc.on keeps a single handler per event type, and VoiceClient.__init__ just
        # claimed VOICE_STATE_UPDATE for itself -- chain our occupant tracker back in.
        vc_handler = self.gc.handlers['VOICE_STATE_UPDATE']
        async def both(d): await asyncio.gather(self.on_voice_state(d), vc_handler(d))
        self.gc.on('VOICE_STATE_UPDATE', both)

    # -- recording ------------------------------------------------------------

    def outpath(self, ch):
        gld = self.glds.get(ch.guild_id)
        tmpl = self.query_one('#out', Input).value
        path = Path(tmpl.format(guild=slug(gld.name if gld else ch.guild_id), channel=slug(ch.name),
                                ts=datetime.now().strftime('%Y%m%d_%H%M%S')))
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    async def on_tree_node_selected(self, event: Tree.NodeSelected):
        if isinstance(event.node.data, Channel): self.run_worker(self.record(event.node.data), exclusive=True)

    async def record(self, ch):
        if self.vc: return self.status('Already recording — press s to stop first')
        self.status(f'Joining 🔊 {ch.name}…')
        self.vc = VoiceClient(self.gc, ch.guild_id, ch)
        self.chain_voice_handler()
        try:
            await self.vc.join()
            await asyncio.wait_for(self.vc.sess.wait(), 15)
        except Exception as e:
            self.vc = None
            return self.status(f'Join failed: {e!r}')
        path = self.outpath(ch)
        self.vc.start_recording(str(path))
        self.rec_start, self.rec_label = time.monotonic(), f'🔊 {ch.name} → {path}'

    def action_stop(self): self.run_worker(self.stop(), exclusive=True)

    async def stop(self):
        if not self.vc: return self.status('Not recording')
        vc, self.vc, self.rec_start = self.vc, None, None
        self.status('Finalizing recording…')
        try: res = await vc.stop_recording(mix=self.mix)
        except Exception as e:
            res = None
            self.status(f'Stop failed: {e!r}')
        with suppress(Exception): await vc.leave()
        if res is not None:
            out = res['mixed'] or ', '.join(res['speakers'].values()) or 'no audio captured'
            self.status(f'Saved: {out}')

    def action_toggle_mix(self):
        self.mix = not self.mix
        self.status(f'Mix on stop: {"on" if self.mix else "off (per-speaker files only)"}')

    def tick(self):
        if self.rec_start is not None:
            m, s = divmod(int(time.monotonic() - self.rec_start), 60)
            self.status(f'⏺ REC {m:02d}:{s:02d}  {self.rec_label}  (s to stop)')

    async def action_quit(self):
        if self.vc: await self.stop()
        if self.gc:
            with suppress(Exception): await self.gc.stop()
        if self.dc:
            with suppress(Exception): await self.dc.cli.aclose()
        self.exit()


if __name__ == '__main__': RecorderTUI().run()
