# Release notes

<!-- do not remove -->

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

