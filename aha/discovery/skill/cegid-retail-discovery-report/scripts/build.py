#!/usr/bin/env python3
"""Checks a discovery report, then builds its JSON file and its Discovery Publisher link.

Usage: python3 build.py /tmp/discovery.json [/tmp/discovery_sources.txt]
Input: the report as JSON (see SKILL.md, section 6). Fields added automatically:
skill_updated (read from SKILL.md), product (RETAILY2) and lang (fr) if missing.
Checks: quotes found word for word in the sources, no email or phone number,
https source links, summary of 5 lines max, at least one unknown, valid decision.
Output: "FILE: <path>" then "LINK: <url>", or the list of errors to fix (exit code 1).
"""
import base64, json, os, re, sys, unicodedata, zlib

PUBLISHER_URL = "https://berenaud.github.io/cegid-retail/aha/discovery/"
OUTPUT_DIR = "/mnt/user-data/outputs"
HERE = os.path.dirname(os.path.abspath(__file__))
DECISIONS = ("Lancer une feature", "Creuser", "Abandonner")


def skill_version():
    try:
        with open(os.path.join(HERE, "..", "SKILL.md"), encoding="utf-8") as fh:
            m = re.search(r'updated:\s*"?(\d{4}-\d{2}-\d{2})', fh.read())
            return m.group(1) if m else None
    except OSError:
        return None


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\u2019", "'").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def main(path, sources_path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"INVALID JSON in {path}: {e}")
    try:
        with open(sources_path, encoding="utf-8") as fh:
            sources = norm(fh.read())
    except OSError:
        sys.exit(f"NO SOURCES FILE: write the sources to {sources_path} first (section 2).")

    data.setdefault("product", "RETAILY2")
    data.setdefault("lang", "fr")
    version = skill_version()
    if version:
        data["skill_updated"] = version

    errors = []
    for key in ("topic", "status", "sources", "summary", "problems", "recommendation"):
        if not data.get(key):
            errors.append(f"MISSING FIELD: {key}")
    for p in data.get("problems", []):
        for q in p.get("quotes", []):
            if norm(q.get("text", "")) not in sources:
                errors.append(f"QUOTE NOT FOUND IN SOURCES: {q.get('text', '')[:80]}")
        if p.get("evidence") in ("Fort", "Moyen") and not p.get("quotes"):
            errors.append(f"NO QUOTE for a problem with evidence {p.get('evidence')}: {p.get('title')}")
    for l in data.get("source_links", []):
        if not re.fullmatch(r"https://[^\s\"'<>]+", l.get("url", "")):
            errors.append(f"INVALID SOURCE URL (https only, no spaces): {l.get('label')} -> {l.get('url')}")
    text = json.dumps({k: v for k, v in data.items() if k != "source_links"}, ensure_ascii=False)
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
        errors.append("EMAIL FOUND: remove it (anonymization).")
    if re.search(r"(?:\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4}", text):
        errors.append("PHONE NUMBER FOUND: remove it (anonymization).")
    if len(str(data.get("summary", "")).strip().splitlines()) > 5:
        errors.append("SUMMARY TOO LONG: 5 lines max.")
    if not data.get("unknowns"):
        errors.append("NO UNKNOWNS: list at least one open question.")
    if (data.get("recommendation") or {}).get("decision") not in DECISIONS:
        errors.append("INVALID DECISION: use Lancer une feature, Creuser or Abandonner.")
    if errors:
        sys.exit("\n".join(errors))

    # 1. Fichier JSON : la voie de secours, toujours fournie au PM (jamais recopié par Claude)
    ascii_topic = unicodedata.normalize("NFKD", data["topic"]).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_topic.lower()).strip("-")[:50] or "report"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"discovery-{slug}.json")
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
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python3 build.py /tmp/discovery.json [/tmp/discovery_sources.txt]")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "/tmp/discovery_sources.txt")
