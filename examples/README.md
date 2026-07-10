# cordslite examples

Each example lives in its own folder with a README explaining how to run it.
They are standalone [uv](https://docs.astral.sh/uv/) scripts — no install needed,
just `uv run` the script and uv fetches the dependencies.

All examples need `DISCORD_BOT_TOKEN` set (see the main README for how to create
a bot and invite it to your server).

| Example | Description |
|---|---|
| [`recorder_tui/`](recorder_tui/) | A little Textual TUI: browse your guilds and voice channels (with live occupants), join one, and record it to mp3 |
