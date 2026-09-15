# Release notes

<!-- do not remove -->

## 0.2.2

### New Features

- strip whitespace from tokens ([#31](https://github.com/AnswerDotAI/cordslite/pull/31)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.2.1

### New Features

- Add DM support: list, read, and search direct messages ([#29](https://github.com/AnswerDotAI/cordslite/pull/29)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.2.0

### New Features

- Make voice support an optional extra ([#28](https://github.com/AnswerDotAI/cordslite/pull/28)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add Member.display_name, gate voice debug prints, skip unmapped SSRCs ([#27](https://github.com/AnswerDotAI/cordslite/pull/27)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add channel/thread helpers, user & message accessors, and attachment saving ([#26](https://github.com/AnswerDotAI/cordslite/pull/26)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add Intent flags, unify token handling, and refresh docs ([#25](https://github.com/AnswerDotAI/cordslite/pull/25)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add voice channel leave/disconnect and extract reusable mix_recording ([#21](https://github.com/AnswerDotAI/cordslite/pull/21)), thanks to [@ncoop57](https://github.com/ncoop57)

### Bugs Squashed

- Fix recording alignment by writing silence padding in real-time ([#24](https://github.com/AnswerDotAI/cordslite/pull/24)), thanks to [@ncoop57](https://github.com/ncoop57)
- Fix ffmpeg recording hangs, voice state filtering, and use UNSET sentinel for optional params ([#23](https://github.com/AnswerDotAI/cordslite/pull/23)), thanks to [@ncoop57](https://github.com/ncoop57)
- Fix message parsing crashes and gateway reconnect loop ([#22](https://github.com/AnswerDotAI/cordslite/pull/22)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add voice channel leave/disconnect and extract reusable mix_recording ([#21](https://github.com/AnswerDotAI/cordslite/pull/21)), thanks to [@ncoop57](https://github.com/ncoop57)
- Fix user token only auth path ([#20](https://github.com/AnswerDotAI/cordslite/pull/20)), thanks to [@KeremTurgutlu](https://github.com/KeremTurgutlu)


## 0.1.0

### New Features

- Refactor: Split core.py into gateway, voice, and bot modules ([#19](https://github.com/AnswerDotAI/cordslite/pull/19)), thanks to [@ncoop57](https://github.com/ncoop57)
- Robust voice/gateway reconnection with backoff, keepalive, and async recording ([#18](https://github.com/AnswerDotAI/cordslite/pull/18)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add Webhook support (create, list, edit, delete, send) and fix Guild.search channel_id access bug ([#17](https://github.com/AnswerDotAI/cordslite/issues/17))



## 0.0.14

### New Features

- Filter out thread messages from search results, handle already-deleted messages, and deduplicate messages in search_and_delete_all ([#16](https://github.com/AnswerDotAI/cordslite/issues/16))

### Bugs Squashed

- Fall back to rotating delete when only one recent message ([#15](https://github.com/AnswerDotAI/cordslite/issues/15))


## 0.0.13

### New Features

- feat(voice): add WebSocket reconnection and resume support ([#14](https://github.com/AnswerDotAI/cordslite/pull/14)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add DAVE E2EE, voice send/receive overhaul, Guild.tree, message context helpers, and Discord skill ([#13](https://github.com/AnswerDotAI/cordslite/pull/13)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.12

### New Features

- Improve WebSocket reconnection handling ([#12](https://github.com/AnswerDotAI/cordslite/pull/12)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.11

### New Features

- Add `search_all` et al; much refactoring ([#11](https://github.com/AnswerDotAI/cordslite/issues/11))


## 0.0.10


### Bugs Squashed

- Fix READY event handler initialization ([#10](https://github.com/AnswerDotAI/cordslite/pull/10)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.9


### Bugs Squashed

- Fix WebSocket resume logic and simplify connection lifecycle ([#8](https://github.com/AnswerDotAI/cordslite/pull/8)), thanks to [@ncoop57](https://github.com/ncoop57)

## 0.0.8

### New Features

- Add reply support to Channel.send() ([#7](https://github.com/AnswerDotAI/cordslite/pull/7)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.7

### New Features

- Add reconnection support to GatewayClient ([#6](https://github.com/AnswerDotAI/cordslite/pull/6)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.6

### New Features

- Add member search and listing methods to Guild ([#5](https://github.com/AnswerDotAI/cordslite/pull/5)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.5

### New Features

- Replace user mention IDs with usernames in message content ([#4](https://github.com/AnswerDotAI/cordslite/pull/4)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.4

### New Features

- Add search functionality for guilds and channels ([#3](https://github.com/AnswerDotAI/cordslite/pull/3)), thanks to [@ncoop57](https://github.com/ncoop57)
- Add helpers for dms and channesl ([#2](https://github.com/AnswerDotAI/cordslite/pull/2)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.3

### New Features

- Add sending and viewing attachments ([#1](https://github.com/AnswerDotAI/cordslite/pull/1)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.2

- Support multiple speakers when recording vc


## 0.0.1

- Initial release
