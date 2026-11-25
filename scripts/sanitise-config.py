#!/usr/bin/env python3
"""Sanitise a live KNOX Console config into the public example template.

Usage:
    python scripts/sanitise-config.py <live-config.json> <example-config.json>

Reads a live config (which may hold LAN tokens, a Spotify client ID, a
home-city location and personal Windows paths) and writes a sanitised copy
with the same structure. It never writes the live file back, and it never
prints a secret value — replacements are placeholders only.

Replacements:
  - lan.token / lan.webhookToken / controls.spotifyClientId and any other
    key named *token*, *secret*, *password*, *clientId*, *clientSecret* or
    *apiKey*  -> "REPLACE_ME" (empty stays empty)
  - weather.city / weather.lat / weather.lon  -> "YOUR_CITY" / 0.0 / 0.0
  - any string containing C:\\Users\\<name>  -> the bare executable name
    where one exists, otherwise "REPLACE_ME"
  - any remaining occurrence of the Windows username  -> "YOUR_NAME"
  - the Charge Knox Console rule (matched to the YQ10S tablet, a device
    Bort does not want in the public example)  -> removed entirely
  - Windows audio endpoint GUIDs, values like
    "{0.0.0.00000000}.{...}"  -> "REPLACE_ME"
"""

import json
import os
import re
import sys

SECRET_KEY_PARTS = ("token", "secret", "password", "clientid",
                    "clientsecret", "apikey", "immichkey")
# Widget option keys such as "onair" / "build" are layout keys, not
# credentials, so they are not touched — only the key names above are.
PLACEHOLDER = "REPLACE_ME"


def sanitise_string(value, username):
    """Sanitise one string value. Returns (new_value, changed_bool)."""
    changed = False
    if username and username.lower() in value.lower():
        # Personal Windows paths: keep only a generic executable name.
        if re.search(r"C:\\Users\\", value, re.I):
            base = value.replace("\\", "/").rstrip("/").split("/")[-1]
            if re.search(r"\.(exe|bat|cmd|lnk)$", base, re.I):
                value, changed = base, True
            else:
                value, changed = PLACEHOLDER, True
        else:
            value = re.sub(re.escape(username), "YOUR_NAME", value,
                           flags=re.I)
            changed = True
    return value, changed


def walk(node, username, path=""):
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            key_lower = key.lower()
            if any(part in key_lower for part in SECRET_KEY_PARTS):
                if isinstance(value, str) and value:
                    out[key] = PLACEHOLDER
                else:
                    out[key] = value
                continue
            out[key] = walk(value, username, f"{path}.{key}")
        return out
    if isinstance(node, list):
        return [walk(item, username, path) for item in node]
    if isinstance(node, str):
        new_value, _ = sanitise_string(node, username)
        return new_value
    return node


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        config = json.load(f)

    # The Windows username is taken from shortcut paths, never typed in.
    # Search the loaded values (single backslashes), not the JSON dump.
    username = ""

    def find_username(node):
        if isinstance(node, dict):
            for value in node.values():
                found = find_username(value)
                if found:
                    return found
        elif isinstance(node, list):
            for value in node:
                found = find_username(value)
                if found:
                    return found
        elif isinstance(node, str):
            match = re.search(r"C:\\Users\\([^\\]+)\\", node)
            if match:
                return match.group(1)
        return ""

    username = find_username(config)

    config = walk(config, username)

    # Location: home city and coordinates are personal, not template data.
    weather = config.get("weather", {})
    if isinstance(weather, dict):
        weather["city"] = "YOUR_CITY"
        weather["lat"] = 0.0
        weather["lon"] = 0.0
    # The world-clock widget also names the home city; make it generic.
    # Any zone labelled "<City>=Australia/Sydney" becomes "Home=...".
    config = json.loads(re.sub(
        r"[A-Za-z ]+=Australia/Sydney", "Home=Australia/Sydney",
        json.dumps(config)))
    # A public weather shortcut also names the home town in its URL.
    config = json.loads(re.sub(
        r"https://www\.bom\.gov\.au/nsw/forecasts/[a-z]+\.shtml",
        "https://www.bom.gov.au/nsw/forecasts/",
        json.dumps(config)))

    # The Charge Knox Console rule is tied to one tablet Bort does not
    # want in the public example — drop it, do not just blank it.
    rules = config.get("rules", [])
    if isinstance(rules, list):
        config["rules"] = [r for r in rules
                           if not (isinstance(r, dict)
                                   and r.get("id") == "charge-knox-console")]
    # Windows audio endpoint GUIDs are machine-local IDs, not template
    # data — replace the whole device value, keep the structure.
    audio_guid = re.compile(
        r"^\{0\.0\.[01]\.00000000\}\.\{[0-9a-fA-F-]{36}\}$")

    def scrub_guids(node):
        if isinstance(node, dict):
            return {k: scrub_guids(v) for k, v in node.items()}
        if isinstance(node, list):
            return [scrub_guids(v) for v in node]
        if isinstance(node, str) and audio_guid.match(node):
            return PLACEHOLDER
        return node

    config = scrub_guids(config)

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {dst} (username placeholder applied: "
          f"{'yes' if username else 'none found'})")


if __name__ == "__main__":
    main()
