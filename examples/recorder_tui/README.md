# recorder_tui

A cute little terminal UI for recording Discord voice channels, built with
[Textual](https://textual.textualize.io/) and cordslite.

Browse every guild your bot is in, expand one to see its voice channels and who
is currently in them (updated live), hit Enter to join and start recording, and
`s` to stop and finalize the mp3s.

## Requirements

- `DISCORD_BOT_TOKEN` set in your environment
- `ffmpeg` on PATH (recording is piped through ffmpeg)
- [uv](https://docs.astral.sh/uv/) (the script declares its own dependencies)
- The bot invited to your server with permission to connect to voice channels.
  No privileged intents needed — the app uses only the `GUILDS` and
  `GUILD_VOICE_STATES` gateway intents.

## Run it

```sh
uv run recorder_tui.py
```

## Keys

| Key | Action |
|---|---|
| Enter (on a voice channel) | Join and start recording |
| `s` | Stop recording, finalize files, leave the channel |
| `m` | Toggle mixing on/off for the next stop |
| `q` | Quit (stops any active recording first) |

## Output files

The input field at the bottom is the output path template. Placeholders:
`{guild}`, `{channel}`, and `{ts}` (timestamp), e.g. the default

    recordings/{guild}_{channel}_{ts}.mp3

The template path is a *base* name: cordslite writes one file per speaker with
an `_<user_id>` suffix, plus a single `_mixed` file combining everyone (unless
you toggled mixing off with `m`). Speakers who never talk produce no file.
