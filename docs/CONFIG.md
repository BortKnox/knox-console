# CONFIG

The console is driven by one JSON file. The live file is
`KNOX-Personal-Console_V6.4.json` (1.1 MB, 26 top-level sections). This
repo ships only a sanitised copy of it:

```
config/KNOX-Personal-Console.example.json
```

Same structure, same 37 pages, same 184 widgets, same 330 shortcuts —
personal data replaced. Do not commit your live copy; `.gitignore`
already excludes it.

## SANITISED

What was replaced, and why. The script that did it is
`scripts/sanitise-config.py`, so anyone can check the process.

| Field | Live value | Example value | Why |
|---|---|---|---|
| `lan.token` | a 43-character LAN token | `REPLACE_ME` | Secret. Grants local control. |
| `lan.webhookToken` | a 43-character webhook token | `REPLACE_ME` | Secret. Grants local control. |
| `controls.spotifyClientId` | a 32-character client ID | `REPLACE_ME` | Credential. Identifies the app to Spotify. |
| `photos.immichKey` | empty in V6.4 | empty | Kept as-is; fill in your own if you use Immich. |
| `weather.city` | home city | `YOUR_CITY` | Location. |
| `weather.lat` / `weather.lon` | home coordinates | `0.0` / `0.0` | Location. |
| `weather` world-clock widget | home city label | `Home` | Location, inside an HTML widget. |
| Weather shortcut URL | home-town BOM forecast URL | generic `bom.gov.au/nsw/forecasts/` | Location, inside a shortcut. |
| Shortcut `cmd` paths | `C:\Users\<name>\...` (76 occurrences) | bare executable name, or `REPLACE_ME` | Personal Windows username and folder layout. |

58 `REPLACE_ME` placeholders in total.

Verified before publishing, by grepping the example file:

- 0 occurrences of the Windows username
- 0 occurrences of `C:\Users\`
- 0 occurrences of the home city name
- 0 occurrences of the home coordinates
- 0 occurrences of the live token / client ID values
- Structure identical to live: same 26 top-level keys, same 37 page IDs,
  same widget count on every page

The raw V6.4 file was never committed, and its secret values were never
written into any repo file, chat log or note.

## TOP-LEVEL SECTIONS

| Section | What it does |
|---|---|
| `codexBar` | Rotating AI-provider bar (Claude, Codex, Antigravity), page size, rotation interval, live quota display. |
| `controls` | The control layer: 50 actions (mostly radio streams), 5 profiles, listening / power / radio-logo permissions, Spotify client ID. |
| `weather` | Weather city, coordinates, unit (Celsius) and model. Fill in your own city. |
| `ping` | Latency host (`1.1.1.1`) and the adapters watched (VPN, Tailscale, Wi-Fi). |
| `night` | Night mode: on/off, start and end times, dim brightness. Off in V6.4. |
| `display` | The look, frozen: AMOLED theme, mint accent `#80d7bd`, flat style, sans font at 110%, radius 16, gap 12, padding 14, borders on, shadows off, 12-hour clock with seconds, keep-awake, open on connect. |
| `lan` | Local network control: enabled flag, port 8766, LAN token and webhook token. Both tokens are `REPLACE_ME` here — generate your own. |
| `updates` | Auto-update on, upstream repo `ersinkoc/phonebox`. |
| `claude` | Claude seat: phone approvals, 300-second timeout, share conversation and session titles, only-when-away flag. |
| `cursor` | Cursor seat: session tracking on. |
| `antigravity` | Antigravity seat: session tracking and session titles on. |
| `opencode` | OpenCode seat: phone approvals, session tracking, 90-second timeout, 10-second always-countdown, WSL watch, session titles. |
| `pages` | The 37 pages and their widgets. See [PAGES.md](PAGES.md). Most widgets are custom HTML; the rest are native widget types (clock, media, stat, radio, moon, and so on). |
| `shortcuts` | 330 app / link shortcuts: label, icon, colour, command or URL, toggle flag. Personal Windows paths were sanitised — point them at your own apps. |
| `rules` | 4 automation rules: Harbor (process running), Media (media playing), On air (mic in use), Stumble (mic in use). Each has a trigger, a page, a level, a priority and a cooldown. A fifth rule (Charge Knox Console, matched to the YQ10S tablet) was removed at Bort's call on 25 Nov 2026 — the device is not needed in the public example — along with all Windows audio endpoint GUIDs, replaced with `REPLACE_ME`. |
| `charge` | Charge limits: off in V6.4, min 55%, max 80%, method `shortcuts`. |
| `phones` | Paired phones. Empty in V6.4. |
| `calendars` | Calendar feeds. One entry in V6.4 (Google Cal, URL empty). |
| `feeds` | 6 news feeds: Hacker News, OpenAI, Google, ABC News AU, The Verge, BleepingComputer. All public RSS. |
| `photos` | Photo source: local folder (empty path in V6.4), subfolders on, Immich URL / key / album all empty. |
| `cameras` | Camera sources. Empty in V6.4; ffmpeg path empty. |
| `homeAssistant` | Home Assistant integration. Empty object in V6.4 — not wired yet. |
| `obs` | OBS WebSocket: off in V6.4, `ws://127.0.0.1:4455`. |
| `discord` | Discord integration. Disabled in V6.4. |
| `console` | Console profiles. Empty list in V6.4. |
| `steam` | Steam integration. Disabled in V6.4. |

## USING THE EXAMPLE

1. Copy it to your own filename — never edit the example in place and
   commit it as your live config.
2. Search for `REPLACE_ME` and fill in each one, or delete the feature
   that needs it.
3. Set `weather` to your own city and coordinates.
4. Go through `shortcuts` and point every command at an app that exists
   on your machine.
5. Import it into your PhoneBox-based console. Expect to adjust widget
   sizes for your own screen — the design stays the same.

## SANITISING YOUR OWN COPY

```bash
python scripts/sanitise-config.py <live-config.json> <example-config.json>
```

Then grep the output for your username, your city, your coordinates and
any token value before it goes anywhere public. If a check finds
anything, fix the script, not the output by hand.
