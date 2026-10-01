#!/usr/bin/env python3
"""Builds the Aha! Publisher link and the JSON file of a feature.

Usage: python3 build.py /tmp/feature.json
Input: the feature as JSON (see SKILL.md, section 5). Fields added automatically:
skill_updated (read from SKILL.md) and product (RETAILY2 if missing).
Output: "FILE: <path>" then "LINK: <url>", or the list of errors to fix (exit code 1).
"""
import base64, json, os, re, sys, unicodedata, zlib

PUBLISHER_URL = "https://berenaud.github.io/cegid-retail/aha/feature/"
OUTPUT_DIR = "/mnt/user-data/outputs"
HERE = os.path.dirname(os.path.abspath(__file__))


def skill_version():
    try:
        with open(os.path.join(HERE, "..", "SKILL.md"), encoding="utf-8") as fh:
            m = re.search(r'updated:\s*"?(\d{4}-\d{2}-\d{2})', fh.read())
            return m.group(1) if m else None
    except OSError:
        return None


def main(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"INVALID JSON in {path}: {e}")

    data.setdefault("product", "RETAILY2")
    version = skill_version()
    if version:
        data["skill_updated"] = version

    errors = []
    for key in ("name", "context", "objective", "included", "excluded", "criteria", "dependencies", "slices", "mockups"):
        if not data.get(key):
            errors.append(f"MISSING FIELD: {key}")
    name = data.get("name", "")
    if len(name) >= 80:
        errors.append(f"NAME TOO LONG: {len(name)} characters, must be under 80. Shorten FeatureName.")
    if not data.get("personas"):
        errors.append("NO PERSONA: add at least one persona from the library.")
    if not isinstance(data.get("tags", []), list):
        errors.append("TAGS must be a list, one entry per tag.")
    if "discovery" in data and not re.fullmatch(r"[A-Z0-9]+-N-\d+", str(data["discovery"])):
        errors.append("INVALID DISCOVERY REFERENCE: use the note reference shown in Aha! (e.g. RETAILY2-N-7), or remove the key.")
    m = str(data.get("mockups", "")).strip()
    if m.lower().startswith("http") and not re.fullmatch(r"https://[^\s\"'<>]+", m):
        errors.append("INVALID MOCKUPS LINK: must be a single https URL with no text around it.")
    if errors:
        sys.exit("\n".join(errors))

    # 1. Fichier JSON : la voie de secours, toujours fournie au PM (jamais recopié par Claude)
    ascii_name = unicodedata.normalize("NFKD", name.split("|")[-1]).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")[:50] or "feature"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"feature-{slug}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    # 2. Lien compressé, avec une somme de contrôle (c=) pour détecter un lien abîmé
    raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)
    z = base64.urlsafe_b64encode(comp.compress(raw) + comp.flush()).rstrip(b"=").decode()
    crc = format(zlib.crc32(z.encode()), "08x")
    print(f"FILE: {out}")
    print(f"LINK: {PUBLISHER_URL}#c={crc}&z={z}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 build.py /tmp/feature.json")
    main(sys.argv[1])
