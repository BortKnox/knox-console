# KNOX CONSOLE

**A personal command centre for one bench. Audio, media, AI seats, system
telemetry, remote control and sleep — one grid, one accent, no clutter.**

> **Logo and screenshots:** the flat-vector logo and the two V6.4
> captures are staged locally and are **not in this repo yet**. The GitHub
> connector used for this upload only pushes UTF-8 text files, so binary
> PNGs cannot go through it. Upload them in the GitHub web UI — drag
> `knox-console-logo.png` into `assets/` and the two captures into
> `docs/screenshots/` — and the image links in this README will work.
> Nothing here is faked to cover that gap.

```
UNIT     KNOX-CONSOLE
TYPE     DASHBOARD / COMMAND CENTRE
STACK    CUSTOM HTML WIDGETS + CONFIG
STATUS   ACTIVE — V6.4, PERSONAL BUILD, NO INSTALLER
```

[**What it is**](#what-it-is) · [**Pages**](#pages) · [**Config**](#config) ·
[**Screenshots**](#screenshots) · [**Notes**](#notes)

## WHAT IT IS

KNOX Console is the dashboard that runs Bort's bench. It is a full
command centre, not a macro deck — the widgets were rebuilt as custom HTML
on top of the original grid, and it grew past that into its own thing.

It does, from one screen:

- **Audio routing and profiles** — mixer, outputs, push-to-talk, on-air.
- **Media, radio and Spotify** — 50 radio actions, cinema, music, sleep radio.
- **PC telemetry** — CPU / RAM / GPU / temps, network, ping.
- **Remote control and trackpads** — media, browser, Windows, keyboard.
- **App launcher** — VS Code, Terminal, Git Bash, VLC, Task Manager and more.
- **AI seats** — Claude, Codex, Antigravity, OpenCode, with quota tracking.
- **System control, power, VPN and routines** — including charge limits and
  a nightstand with a sleep timer.

The look is deliberate and frozen: AMOLED dark, mint accent `#80d7bd`,
flat style, radius 16, no shadows. Teenage Engineering stripped-down,
one-pixel details. If it does not fit that, it does not ship.

## PAGES

37 pages, 184 widgets, 330 shortcuts. Full inventory:
[docs/PAGES.md](docs/PAGES.md).

| Group | Pages |
|---|---|
| Day and world | Home, Today, Focus, Planner, World, News |
| AI | AI, AI Pulse, AI Quotas, AI Providers |
| Remote | Remote, Media Remote, Browser Remote, Windows Remote, Keyboard |
| Launch | Launchpad, Launch Apps, Launch Tools, Launch Media, Launch Web, Launch Folders, Launch Files |
| Media and audio | Media, Music, Cinema, Radio, Audio, Mic & Live |
| System | Desk, System, Network, Signals, Power, Routines |
| Unwind | Calm, Sleep, Nightstand |

## CONFIG

This repo holds a **sanitised example config**, not a live one:

```
config/KNOX-Personal-Console.example.json
```

It has the same structure as the live V6.4 config — same 37 pages, same
widget counts, same 330 shortcuts — with personal data replaced. See
[docs/CONFIG.md](docs/CONFIG.md) for what each section does and how to
fill the placeholders in.

To use it:

1. Copy the example to your own config file. Do not commit your live copy.
2. Fill in every `REPLACE_ME` — LAN tokens, Spotify client ID — and set
   `weather.city`, `weather.lat` and `weather.lon` to your own city.
3. Fix the shortcut commands: personal Windows paths were replaced with
   bare executable names or `REPLACE_ME`. Point them at your own apps.
4. Import it into your PhoneBox-based console and adjust the layout to
   your own screen. Do not change the design to fit a new widget — fit the
   widget to the design.

The sanitiser that produced the example is in the repo, so the process is
auditable:

```
python scripts/sanitise-config.py <live-config.json> <example-config.json>
```

## SCREENSHOTS

Two captures from the live V6.4 build, 25 November 2026. The PNG files
themselves are pending upload via the GitHub web UI (see the note at the
top of this file) — the connector cannot push binary files.

| File (upload to `docs/screenshots/`) | Shows |
|---|---|
| `nightstand.png` | Nightstand page: clock 2:56 PM, Wednesday 25 November, moon, next-hours forecast, sleep timer. |
| `sleep-wind-down.png` | Sleep page: wind-down radio (Nightride FM, Smooth Chill, Smooth Relax), volume 90%, full moon 100% lit, Goodnight / Screen Off / All Quiet / Mute. |

Provenance and what was left out, and why:
[docs/screenshots/README.md](docs/screenshots/README.md).

## LAYOUT

```
README.md                              # this file
LICENSE                                # MIT
CONTRIBUTING.md                        # how to report, what not to send
.gitignore                             # personal config stays out
assets/
  knox-console-logo.png                # flat vector logo — UPLOAD VIA WEB, see top of README
config/
  KNOX-Personal-Console.example.json   # sanitised V6.4 template (1.1 MB)
docs/
  CONFIG.md                            # every config section, explained
  PAGES.md                             # 37 pages, widget inventory
  screenshots/
    README.md                          # provenance
    nightstand.png                     # Home / Nightstand, V6.4 — UPLOAD VIA WEB
    sleep-wind-down.png                # Sleep, V6.4 — UPLOAD VIA WEB
scripts/
  sanitise-config.py                   # live config -> public example
```


## NOTES

- This is a personal build, shared as is. It was built for one bench
  first, and published so anyone can read, fork or borrow from it.
- The live config is **not** in this repo. It holds LAN tokens, a Spotify
  client ID, a home-city location and personal Windows paths. The example
  replaces all of those — 58 placeholders in total — and the raw file was
  never committed. See [docs/CONFIG.md](docs/CONFIG.md#sanitised).
- Personal project, shared as is. Issues and pull requests may not get a
  reply; forking is welcome.
- The logo and screenshots are Bort's own art and captures. If the
  presentation here falls short of the console's own aesthetic, that is
  known — the copy and the repo are the deliverable; the art is his.

## DIRECTION

Next step, planned not done: port each page to **one single custom HTML
widget** instead of many default widgets jammed together. One widget per
page should give better customisation, faster page changes, and more out
of the canvas — and it will most likely compress the config file by
avoiding heaps of widget snippets. That last part is Bort's call, not a
measured result yet.

## ACKNOWLEDGEMENT

KNOX Console is built on [PhoneBox](https://github.com/ersinkoc/phonebox)
by ersinkoc — its infrastructure, setup and grid. That is the nod, and it
belongs here at the bottom: Bort took it to the level it deserved, and the
work in this repo is his.

## LICENSE

MIT — see [LICENSE](LICENSE).
