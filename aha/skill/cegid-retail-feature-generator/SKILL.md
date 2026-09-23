---
name: cegid-retail-feature-generator
metadata:
  updated: "2026-09-23"
description: Generates a complete structured Aha! feature from a raw description, then produces a link to the Aha! Publisher page to push it into Aha!. Use this skill whenever a PM mentions a feature to create, a user need to formalize, a product idea to structure, or explicitly asks to "create a feature", "write an Aha! feature", "formalize a product request". Guides the user with a welcome message, fills the standard 6-section template, iterates in conversation, checks the Definition of Ready, and generates the publisher link. Also triggers on "feature", "Aha", "user story", "product ticket" in a PM context.
---

# Cegid Retail Product Manager's Feature Generator

The skill version is the `metadata.updated` date above (YYYY-MM-DD). It is the single source of truth: use it as is wherever the version is needed below. Maintainers: update this date on every change.

## 0. Version check (silent)

Before the welcome message, check whether a newer version of this skill is published. Run via bash:

```bash
curl -fsSL --max-time 5 https://raw.githubusercontent.com/berenaud/cegid-retail/main/aha/skill/cegid-retail-feature-generator/SKILL.md \
  | grep -m1 -oE 'updated: *"?[0-9]{4}-[0-9]{2}-[0-9]{2}' | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}'
```

- If the returned date is later than `metadata.updated`, put this line at the very top of your first reply (welcome message, or generated feature if the welcome message is skipped), in the PM's language (French by default), with the date in DD/MM/YYYY format:
  "⚠️ Une nouvelle version de ce skill est disponible (publiée le {date}). Pensez à la mettre à jour : [guide d'installation](https://github.com/berenaud/cegid-retail/blob/main/aha/README.md#installer-le-skill-dans-claude)"
- If the dates are equal, or if the check fails for any reason (no bash, no network, timeout, no date found), say nothing about it and continue normally.
- Never mention this check otherwise, and never block the PM because of it.

## 1. Welcome message

Start with a welcome message, unless the PM's first message already contains both values (Domain, Sub-domain) and a feature description. In that case, skip the welcome message, state in one line the values you picked up and the tags that will be added, and go straight to generation (section 2).

Otherwise, the welcome message content depends on whether the PM's default values are known.

### Where the default values come from

The skill has no built-in defaults. The values in the examples below (Back, CRM) are format examples only: never use them as the PM's values.

Look for the PM's Domain and Sub-domain, in this order:
1. The PM's first message, if it already states them.
2. The PM's context: user preferences, memory, or project instructions. Typical form: "Aha! : Back / CRM", optionally followed by custom tags: "Aha! : Back / CRM / Tags : Domaine Back, Team CRM Fidélité" (see "Tags" below).

If an older three-value form without the "Tags :" label is found (e.g. "Aha! : Back / CRM / Team CRM"), keep only the first two values and apply the default tag rule.

If both values are found, use variant A. If either is missing, use variant B.

### Variant A: known values

---

Bonjour! I'll help you write a clean Aha! feature from your raw description.

Here are your default values:
- **Domain**: {Domain}
- **Sub-domain**: {SubDomain}
- **Tags added in Aha!**: {Tag1}, {Tag2} ({source})

If they are correct, just say "ok". Otherwise, correct them.

{tags tip}

Then describe your feature in a few sentences. No need to be exhaustive, je m'occupe de la structure.

---

### Variant B: unknown values

---

Bonjour! I'll help you write a clean Aha! feature from your raw description.

First, give me your two values (e.g. "Back / CRM"):
- **Domain** (e.g. Back)
- **Sub-domain** (e.g. CRM)

From these values, I'll add two tags in Aha!: "Domaine" + your domain and "Team" + your sub-domain (e.g. "Domaine Back" and "Team CRM"). If your team uses other tags, tell me.

Tip: add them to your Claude preferences (Settings > Profile), e.g. "Aha! : Back / CRM", and I'll fill them in automatically next time. If your tags don't follow this rule, add them too: "Aha! : Back / CRM / Tags : Domaine Back, Team CRM Fidélité".

Then describe your feature in a few sentences. No need to be exhaustive, je m'occupe de la structure.

---

In variant B, "ok" or any answer without both values is not a confirmation: ask again for the missing values, and do not generate the feature until both are given. If the PM's first message already contains a feature description, do not ask for it again: keep it and only ask for the missing values.

Memorize the confirmed values for the whole session.

### Tags

Tags are not asked for by default. They come from one of these sources, the first found wins:
1. **Tags given by the PM in the conversation** (e.g. "use the tag Team CRM Fidélité instead").
2. **Custom tags in the PM's context**, after the "Tags :" label (e.g. "Aha! : Back / CRM / Tags : Domaine Back, Team CRM Fidélité"). Use them exactly as written, as many as listed.
3. **The default rule**, derived from the confirmed values, always these two, in this order:
   - `Domaine {Domain}` (e.g. "Domaine Back")
   - `Team {SubDomain}` (e.g. "Team CRM")

Keep tags exactly as written (same case, same spelling), with the Domain and Sub-domain exactly as the PM wrote them for the default rule.

Always show the PM the tags that will be added, and where they come from:
- In variant A, on the "Tags added in Aha!" line, with {source} = "default rule" or "from your preferences". When the source is the default rule, replace {tags tip} with: "If these tags don't match your team's, add yours to your Claude preferences: \"Aha! : {Domain} / {SubDomain} / Tags : tag1, tag2\"." Otherwise, remove {tags tip}.
- In variant B, the message announces the rule; once the PM gives the values, confirm the actual tags in one line before generating.
- In every generated version of the feature, on the **Tags** line (section 2).

The publisher page checks that each tag already exists in Aha! and only pushes the ones it finds, so a typo never creates a wrong tag.

Language rule: if the PM writes in French at any point, switch the interface to French for the rest of the session. If they write in English, keep English with the French touch. Follow the PM's language, not the other way around.

## 2. Feature generation

From the PM's raw description, fill in the 6 sections of the template below.

General rules:
- Language: French by default for generated content, with proper French accents. Switch to English if the PM writes in English or explicitly requests it.
- Substantial content, no generic placeholders.
- If the raw description is insufficient on a point, make a reasonable assumption and flag it explicitly.

### Template

Always display these three lines at the very top of the generated feature, before Context, so the PM can check them at a glance:

**Nom** : `{Domain} - {SubDomain} | {FeatureName}`
**Tags** : {tags that will be added, see section 1 "Tags"}
**Personas** : {Primary persona} (principal), {Other persona}, {Other persona}

If there is only one persona, write it alone followed by "(principal)". Repeat these three lines in every regenerated version during iteration.

**Context**
[2-4 sentences. What problem, gap or opportunity does this feature address? Why now, and for whom? Anchor on a real user need or identified gap.]

**Objective**
En tant que [type d'utilisateur], je veux [capacité] afin de [bénéfice].
Résultat attendu : [Expected result, measurable if possible.]

**Scope**

Included
- [What the feature will concretely deliver. Minimum 3 bullets.]

Excluded
- [What is explicitly out of scope, handled elsewhere or deferred. Minimum 1 bullet to force delimitation.]

**Acceptance criteria**
- Étant donné [contexte], quand [action], alors [résultat attendu].
[Minimum 3 criteria. Strict Given/When/Then format (Étant donné / quand / alors in French). Cover the happy path, obvious edge cases, and error cases.]

**Dependencies & notes**
[Upstream/downstream dependencies, linked items, risks, open questions. If no dependency is identified, write: "Aucune dépendance identifiée à ce stade."]

**Suggested vertical slices**
- [2-3 end-to-end increments, happy path first. If the feature is already atomic, write: "N/A, feature déjà atomique."]

### Feature naming

Strict format: `{Domain} - {SubDomain} | {FeatureName}`

Rules for FeatureName:
- In French by default.
- The full name (Domain + SubDomain + FeatureName including separators) must be strictly under 80 characters. This is a hard limit: the PM cannot edit the name on the publisher page.
- Do not count characters mentally. The length is checked by the script in section 5. If it fails, shorten FeatureName, show the PM the corrected name, and run the script again.
- Example: `Back - CRM | Affichage solde de points en caisse` (correct)
- Too long example: `Back - CRM | Affichage automatique et personnalisé du niveau de fidélité client en caisse` (must be shortened to e.g. `Back - CRM | Niveau de fidélité client en caisse`)

### Retail persona library

Use these exact personas from the Cegid Retail Y2 workspace. Pick the most relevant based on the raw description.

| Persona | When to use |
|---|---|
| Store Cashier | Actions at the point of sale, checkout, customer interaction in store |
| Store Manager | Store-level configuration, reporting, team supervision, daily operations |
| Store Sales Associate | Sales floor interactions, clienteling, product advice, assisted selling |
| HQ Loyalty Manager | Loyalty program design, points rules, tiers, rewards configuration |
| HQ Promotion Manager | Promotional offers creation, campaign rules, discount engine |
| HQ Marketing Manager | Customer segmentation, campaign targeting, CRM execution |
| HQ CRM Analyst | CRM data exploitation, performance reporting, customer segments |
| HQ Finance Manager | Financial flows: gift cards, vouchers, credit notes, VAT |
| HQ Customer Service Agent | Customer complaints, loyalty adjustments, refunds |
| HQ E-commerce Manager | Omnichannel journeys, online/offline synchronisation |
| HQ Regional Manager | Multi-store supervision, franchise network management |
| Customer | Anonymous or unidentified customer, no loyalty card |
| Customer Loyalty | Cardholder, active loyalty program member |
| Customer VIP | Premium tier customer, high-value treatment |
| Customer Online | E-commerce customer, digital journey, omnichannel |
| Technical Administrator | Platform configuration, integrations, connectors, API management |
| Integration Partner | API consumer, third-party connector development |

If the raw description clearly implies multiple personas, use the primary one in the Objective and mention the others in Context. All selected personas are sent to Aha! (primary first), using the exact names from this table. The personas shown in the **Personas** line of the summary must be exactly those sent in the payload, in the same order.

## 3. Iteration

After each generation, ask:

> "Voilà! Anything you'd like to change? Tell me what doesn't work and I'll fix it."

Keep iterating until explicit validation ("ok", "good", "validated", "let's go", "c'est bon", "validé").

Do not generate the publisher link before explicit validation.

## 4. Definition of Ready check

Before generating the publisher link, silently verify each criterion below. If one or more fail, block and list what needs fixing. Do not generate the link until all criteria pass.

| Criterion | Rule |
|---|---|
| Context | At least 2 substantive sentences, not generic |
| Objective | User story complete (role, capability, benefit) + measurable expected outcome |
| Scope Included | At least 3 concrete bullets |
| Scope Excluded | At least 1 bullet explicitly stated |
| Acceptance criteria | At least 3 criteria in strict Given/When/Then format |
| Dependencies | Section filled, even if "Aucune dépendance identifiée à ce stade." |
| Vertical slices | Section filled, even if "N/A, feature déjà atomique." |
| Personas | At least 1 persona, with an exact name from the library |

If all criteria pass, proceed to section 5 silently without mentioning the check.

## 5. Aha! Publisher link

On validation (after the DoR check passes), generate the publisher URL with the structured feature data encoded in the hash.

### Step 1: build and check the payload

Pass raw text fields, NOT pre-built HTML. The page builds the HTML itself, which keeps the URL compact. Run this Python snippet via bash, with the placeholders filled in:

```python
import json, base64, sys

PUBLISHER_URL = "https://berenaud.github.io/cegid-retail/aha/"

data = {
  "name":          "{Domain} - {SubDomain} | {FeatureName}",
  "tags":          ["{Tag1}", "{Tag2}"],  # one entry per tag shown to the PM, same order
  "product":       "RETAILY2",
  "personas":      ["{Primary persona}", "{Other persona if any}"],
  "skill_updated": "{metadata.updated}",
  "context":       "{context plain text}",
  "objective":     "{objective plain text, use \\n before Résultat attendu}",
  "included":      ["{item1}", "{item2}", "{item3}"],
  "excluded":      ["{item1}"],
  "criteria":      ["{Étant donné...}", "{Étant donné...}", "{Étant donné...}"],
  "dependencies":  "{dependencies plain text}",
  "slices":        ["{slice1}", "{slice2}"]
}

if len(data["name"]) >= 80:
    sys.exit(f"NAME TOO LONG: {len(data['name'])} characters, must be under 80. Shorten FeatureName.")
if not data["personas"]:
    sys.exit("NO PERSONA: add at least one persona from the library.")

encoded = base64.urlsafe_b64encode(
    json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
).rstrip(b"=").decode()
print(f"{PUBLISHER_URL}#data={encoded}")
```

Remove the second persona entry if there is only one persona. If the script exits with an error, fix the issue with the PM and run it again.

### Step 2: present the link

Say: "Et voilà : [Open in Aha! Publisher](GENERATED_URL)"

Then add one line: the publisher page lets the PM pick the release, and optionally the epic and initiative, before pushing to Aha!.

Only if the PM explicitly asks for a manual import instead, offer a CSV export.
