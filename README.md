# Cegid Retail · Outils produit / Product tools

[Français](#français) · [English](#english)

Site : https://berenaud.github.io/cegid-retail/

---

## Français

Pages et skills Claude pour le travail produit chez Cegid Retail. Chaque outil a son propre dossier, qui regroupe sa page et son skill.

### Outils

| Outil | Rôle | Dossier |
|---|---|---|
| Aha! Feature Publisher | Rédiger une feature avec Claude et la publier dans Aha! | [`aha/`](aha/) |

### Structure

```
cegid-retail/
├── index.html          page d'accueil
├── README.md
└── aha/
    ├── index.html      page de l'outil
    ├── README.md       guide de l'outil
    └── skill/          skill Claude associé
```

### Règles du dépôt

- **Le dépôt est public**, historique compris : jamais de token, de mot de passe, d'export de données ou d'exemple contenant de vraies données Cegid. Un skill qui contiendrait des informations sensibles va dans un dépôt privé séparé.
- **Toutes les pages partagent le même stockage navigateur.** Une page du dépôt peut lire ce qu'une autre y enregistre, y compris un token. N'ajouter que des pages écrites ou relues par un mainteneur.
- Préfixer les clés de stockage local par le nom de l'outil (ex. `cegid_aha_…`).

### Ajouter un outil

1. Créer un dossier à la racine (ex. `jira/`) avec son `index.html`, son `README.md` et, si besoin, `skill/`.
2. Ajouter l'outil au tableau ci-dessus et à la page d'accueil `index.html`.
3. Il sera accessible à `https://berenaud.github.io/cegid-retail/<dossier>/`.

---

## English

Pages and Claude skills for product work at Cegid Retail. Each tool has its own folder, holding its page and its skill.

### Tools

| Tool | Purpose | Folder |
|---|---|---|
| Aha! Feature Publisher | Write a feature with Claude and publish it to Aha! | [`aha/`](aha/) |

### Structure

```
cegid-retail/
├── index.html          home page
├── README.md
└── aha/
    ├── index.html      tool page
    ├── README.md       tool guide
    └── skill/          related Claude skill
```

### Repository rules

- **The repository is public**, history included: never commit tokens, passwords, data exports or samples containing real Cegid data. A skill containing sensitive information goes to a separate private repository.
- **All pages share the same browser storage.** A page in this repository can read what another one stores there, tokens included. Only add pages written or reviewed by a maintainer.
- Prefix local storage keys with the tool name (e.g. `cegid_aha_…`).

### Adding a tool

1. Create a folder at the root (e.g. `jira/`) with its `index.html`, its `README.md` and, if needed, `skill/`.
2. Add the tool to the table above and to the `index.html` home page.
3. It will be available at `https://berenaud.github.io/cegid-retail/<folder>/`.
