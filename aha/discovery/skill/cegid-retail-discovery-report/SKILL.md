---
name: cegid-retail-discovery-report
metadata:
  updated: "2026-10-01"
description: "Turns raw discovery material (customer interview notes, store visit notes, workshop transcripts, support tickets) into a structured, evidence-based discovery report, then produces a link to the Discovery Publisher page to save it as a note in Aha! (Knowledge > Documents > Discoveries). Use this skill whenever a Cegid Retail PM wants to synthesize interviews or research, write a discovery report, \"faire une synthèse de discovery\", \"analyser des entretiens\", or prepare the evidence before writing a feature. Do not use it to write a feature directly: that is the cegid-retail-feature-generator skill."
---

# Cegid Retail Discovery Report

The skill version is the `metadata.updated` date above (YYYY-MM-DD). It is the single source of truth: use it as is wherever the version is needed below. Maintainers: update this date on every change.

## 0. Version check (silent)

Before the welcome message, check whether a newer version of this skill is published. Run via bash:

```bash
curl -fsSL --max-time 5 https://raw.githubusercontent.com/berenaud/cegid-retail/main/aha/discovery/skill/cegid-retail-discovery-report/SKILL.md \
  | grep -m1 -oE 'updated: *"?[0-9]{4}-[0-9]{2}-[0-9]{2}' | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}'
```

- If the returned date is later than `metadata.updated`, put this line at the very top of the welcome message, with the date in DD/MM/YYYY format:
  "⚠️ Une nouvelle version de ce skill est disponible (publiée le {date}). Pensez à la mettre à jour : [guide d'installation](https://github.com/berenaud/cegid-retail/blob/main/aha/discovery/README.md#installer-le-skill-dans-claude)"
- If the dates are equal, or if the check fails for any reason, say nothing about it and continue normally. Never block the PM because of it.

## 1. Welcome message

Start with this message (in French by default, in English if the PM writes in English):

---

Bonjour ! Je vais transformer ton matériel de discovery en un rapport clair, à partager dans Aha!.

Donne-moi :
- **Le sujet** en quelques mots (ex. « renouvellement des conditions commerciales »)
- **Tes sources** : notes d'entretiens, comptes rendus de visites, transcriptions d'ateliers, tickets… Colle-les ou joins les fichiers, en indiquant pour chacune d'où elle vient (ex. « Entretien 3, Store Manager »).
- **Les noms d'enseignes** : je les garde ou je les anonymise (« Client A », « Client B ») ?

---

## 2. Store the sources (mandatory, silent)

Before analysing, write ALL the source material the PM gave, exactly as given, into `/tmp/discovery_sources.txt` via bash (a heredoc with a quoted delimiter so nothing gets interpreted). If files were attached, extract their text into the same file. Each source starts with a line `=== SOURCE: {label} ===`.

This file is used by the script in section 6 to check that every quote really exists in the sources. If the PM adds material later, append it to the file.

## 3. Analysis rules

- **Problems, not solutions.** "Il manque un bouton export" becomes the underlying need ("Les managers doivent partager les chiffres hors de l'outil"). Solutions go in "Pistes", never in problems.
- **Evidence is weighted.** For each problem, count in how many distinct sources it appears. Frequency is written "{n}/{total} sources". Evidence level:
  - **Fort**: 3 sources or more, from at least 2 different personas or clients.
  - **Moyen**: 2 sources, or several mentions from a single client.
  - **Faible**: a single source. Keep it if relevant, but never present it as a trend.
- **Impact** (Fort / Moyen / Faible): consequence for the user or the business (blocked task, lost time, lost revenue, workaround, compliance risk). Justify it in the problem description.
- **Quotes are verbatim.** Copy them word for word from the sources, short (one or two sentences), with their source label. Never rephrase, merge or invent a quote. If there is no good quote for a problem, lower its evidence level instead.
- **Anonymization.** Never write person names, emails or phone numbers. Refer to people by role and source (e.g. "Entretien 3, Store Manager"). Apply the PM's choice for retailer names.
- **What we do not know.** Always list at least one open question or hypothesis to validate. A discovery with no unknowns is a discovery that did not look hard enough.
- **Recommendation.** One of: "Lancer une feature", "Creuser", "Abandonner". Justify it with the evidence, and give concrete next steps.
- **Personas.** Use the exact names from the library below.

### Retail persona library

Store Cashier, Store Manager, Store Sales Associate, HQ Loyalty Manager, HQ Promotion Manager, HQ Marketing Manager, HQ CRM Analyst, HQ Finance Manager, HQ Customer Service Agent, HQ E-commerce Manager, HQ Regional Manager, Customer, Customer Loyalty, Customer VIP, Customer Online, Technical Administrator, Integration Partner.

This list must stay identical to the one in the cegid-retail-feature-generator skill.

## 4. Report structure

Generate the report in the PM's language (French by default), with these parts:

1. **Sujet (topic)**: short and specific, in English, used for the Aha! folder name (e.g. "Commercial conditions renew"). Not a generic theme like "CRM": what distinguishes this discovery from another on the same theme.
2. **Statut**: "Conclu" or "En cours".
3. **Sources**: type, count, optional detail (e.g. 6 "Entretiens clients", "Store Managers, 4 enseignes").
4. **Résumé**: 5 lines maximum. The main problem, who it affects, the evidence, the recommendation. It must stand on its own: it is often the only part people read.
5. **Problèmes identifiés**: for each one, a title, a description (2-4 sentences), personas, frequency, impact, evidence level, and 1-3 verbatim quotes.
6. **Ce qu'on ne sait pas encore**: open questions and hypotheses to validate.
7. **Pistes**: directions to explore, not final solutions.
8. **Recommandation**: decision, rationale, next steps.

Show the report to the PM in a readable form (headings, a summary table of problems, quotes in blockquotes).

## 5. Iteration and quality check

After each version, ask: "Voilà ! Qu'est-ce que tu veux ajuster ?" Keep iterating until explicit validation ("ok", "c'est bon", "validé", "go").

Before generating the link, silently check:

| Criterion | Rule |
|---|---|
| Summary | 5 lines maximum, stands on its own |
| Problems | At least 1, each phrased as a need, not a solution |
| Evidence | Each problem has frequency, impact and evidence level, consistent with section 3 |
| Quotes | Each problem with evidence "Fort" or "Moyen" has at least 1 verbatim quote |
| Unknowns | At least 1 |
| Recommendation | Decision among the 3 allowed values, rationale, at least 1 next step |
| Anonymization | No person names, emails or phone numbers |

If a criterion fails, say what to fix. If all pass, go to section 6 without mentioning the check.

## 6. Discovery Publisher link

Run this Python snippet via bash, placeholders filled in. It checks the quotes against `/tmp/discovery_sources.txt`, looks for personal data, then compresses the report into the link.

```python
import json, base64, re, sys, zlib, unicodedata

PUBLISHER_URL = "https://berenaud.github.io/cegid-retail/aha/discovery/"

data = {
  "topic":         "{Topic in English}",
  "lang":          "fr",
  "status":        "{Conclu | En cours}",
  "product":       "RETAILY2",
  "skill_updated": "{metadata.updated}",
  "sources":       [{"type": "{Entretiens clients}", "count": 6, "detail": "{optional}"}],
  "summary":       "{5 lines max}",
  "problems": [
    {
      "title":       "{need, not solution}",
      "description": "{2-4 sentences}",
      "personas":    ["{exact persona name}"],
      "frequency":   "{n}/{total} sources",
      "impact":      "{Fort | Moyen | Faible}",
      "evidence":    "{Fort | Moyen | Faible}",
      "quotes":      [{"text": "{verbatim}", "source": "{Entretien 3, Store Manager}"}]
    }
  ],
  "unknowns":       ["{open question}"],
  "leads":          ["{direction to explore}"],
  "recommendation": {"decision": "{Lancer une feature | Creuser | Abandonner}", "rationale": "{why}", "next_steps": ["{step}"]}
}

def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\u2019", "'").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

errors = []
try:
    sources = norm(open("/tmp/discovery_sources.txt", encoding="utf-8").read())
except FileNotFoundError:
    sys.exit("NO SOURCES FILE: write the sources to /tmp/discovery_sources.txt first (section 2).")

for p in data["problems"]:
    for q in p.get("quotes", []):
        if norm(q["text"]) not in sources:
            errors.append(f"QUOTE NOT FOUND IN SOURCES: {q['text'][:80]}")
    if p["evidence"] in ("Fort", "Moyen") and not p.get("quotes"):
        errors.append(f"NO QUOTE for a problem with evidence {p['evidence']}: {p['title']}")

text = json.dumps(data, ensure_ascii=False)
if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
    errors.append("EMAIL FOUND: remove it (anonymization).")
if re.search(r"(?:\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4}", text):
    errors.append("PHONE NUMBER FOUND: remove it (anonymization).")
if len(data["summary"].strip().splitlines()) > 5:
    errors.append("SUMMARY TOO LONG: 5 lines max.")
if not data["unknowns"]:
    errors.append("NO UNKNOWNS: list at least one open question.")
if data["recommendation"]["decision"] not in ("Lancer une feature", "Creuser", "Abandonner"):
    errors.append("INVALID DECISION: use Lancer une feature, Creuser or Abandonner.")

if errors:
    sys.exit("\n".join(errors))

raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
c = zlib.compressobj(9, zlib.DEFLATED, -15)
z = base64.urlsafe_b64encode(c.compress(raw) + c.flush()).rstrip(b"=").decode()
print(f"{PUBLISHER_URL}#z={z}")
print(f"(link length: {len(PUBLISHER_URL) + 3 + len(z)} characters)", file=sys.stderr)
```

If the script reports a quote not found, fix the quote so it matches the source word for word, or remove it. Never modify the sources file to make a quote pass.

Then say: "Et voilà : [Publier dans Aha!](GENERATED_URL)" and add one line: the page lets the PM check the folder name (format `AAAA-MM Sujet`, created in Discoveries) before publishing.

## 7. After publishing

If the recommendation is "Lancer une feature", offer to write the feature right away with the cegid-retail-feature-generator skill, reusing the report: context from the summary and problems, personas from the report. Do not start it without the PM's agreement.
