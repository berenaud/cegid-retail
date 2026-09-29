# Cegid Retail · Outils produit / Product tools

[Français](#français) · [English](#english)

Site : https://berenaud.github.io/cegid-retail/

---

## Français

Pages et skills Claude pour le travail produit chez Cegid Retail. Chaque outil a son propre dossier, qui regroupe sa page et son skill.

### Outils

| Outil | Rôle | Dossier |
|---|---|---|
| Aha! Discovery Publisher | Synthétiser une discovery avec Claude et publier le rapport dans Aha! | [`aha/discovery/`](aha/discovery/) |
| Aha! Feature Publisher | Rédiger une feature avec Claude et la publier dans Aha! | [`aha/feature/`](aha/feature/) |

### Structure

```
cegid-retail/
├── .nojekyll             sert les fichiers tels quels (ne pas supprimer)
├── index.html            page d'accueil
├── README.md
├── shared/               code commun à toutes les pages outils
│   ├── common.js         connexion Aha!, lecture des liens, versions
│   └── style.css         styles, mode sombre compris
├── aha/                  outils qui publient dans Aha!
│   ├── discovery/        index.html, README.md, skill/
│   └── feature/          index.html, README.md, skill/
└── discovery/            redirection de l'ancienne adresse (à supprimer à terme)
```

`aha/index.html` et `discovery/index.html` redirigent les liens générés avant la réorganisation vers les nouvelles adresses. Ils pourront être supprimés quand tout le monde aura mis à jour ses skills.

### Règles du dépôt

- **Le dépôt est public**, historique compris : jamais de token, de mot de passe, d'export de données ou d'exemple contenant de vraies données Cegid. Un skill qui contiendrait des informations sensibles va dans un dépôt privé séparé.
- **Toutes les pages partagent le même stockage navigateur.** Une page du dépôt peut lire ce qu'une autre y enregistre, y compris un token. N'ajouter que des pages écrites ou relues par un mainteneur.
- Préfixer les clés de stockage local par le nom de l'outil (ex. `cegid_aha_…`).
- Ne pas supprimer `.nojekyll` : sans lui, GitHub Pages transforme les `SKILL.md` en pages HTML et la détection des mises à jour de skill ne fonctionne plus.

### Ajouter un outil

1. Créer un dossier par famille d'outils puis par outil (ex. `azdo/split/`), avec son `index.html`, son `README.md` et, si besoin, `skill/`. La page charge `../../shared/style.css` et `../../shared/common.js`.
2. Ajouter l'outil au tableau ci-dessus et à la page d'accueil `index.html`.
3. Il sera accessible à `https://berenaud.github.io/cegid-retail/<famille>/<outil>/`.

---

## English

Pages and Claude skills for product work at Cegid Retail. Each tool has its own folder, holding its page and its skill.

### Tools

| Tool | Purpose | Folder |
|---|---|---|
| Aha! Discovery Publisher | Synthesize a discovery with Claude and publish the report to Aha! | [`aha/discovery/`](aha/discovery/) |
| Aha! Feature Publisher | Write a feature with Claude and publish it to Aha! | [`aha/feature/`](aha/feature/) |

### Structure

```
cegid-retail/
├── .nojekyll             serves files as is (do not delete)
├── index.html            home page
├── README.md
├── shared/               code shared by all tool pages
│   ├── common.js         Aha! connection, link decoding, versions
│   └── style.css         styles, dark mode included
├── aha/                  tools that publish to Aha!
│   ├── discovery/        index.html, README.md, skill/
│   └── feature/          index.html, README.md, skill/
└── discovery/            redirect from the old address (to be removed eventually)
```

`aha/index.html` and `discovery/index.html` redirect links generated before the reorganization to the new addresses. They can be deleted once everyone has updated their skills.

### Repository rules

- **The repository is public**, history included: never commit tokens, passwords, data exports or samples containing real Cegid data. A skill containing sensitive information goes to a separate private repository.
- **All pages share the same browser storage.** A page in this repository can read what another one stores there, tokens included. Only add pages written or reviewed by a maintainer.
- Prefix local storage keys with the tool name (e.g. `cegid_aha_…`).
- Do not delete `.nojekyll`: without it, GitHub Pages turns `SKILL.md` files into HTML pages and skill update detection stops working.

### Adding a tool

1. Create a folder per tool family, then per tool (e.g. `azdo/split/`), with its `index.html`, its `README.md` and, if needed, `skill/`. The page loads `../../shared/style.css` and `../../shared/common.js`.
2. Add the tool to the table above and to the `index.html` home page.
3. It will be available at `https://berenaud.github.io/cegid-retail/<family>/<tool>/`.
