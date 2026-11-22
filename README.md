# Méthode de montage YouTube, pour ton Claude ou ton Codex

Ce dépôt contient toute la méthode de montage des vidéos YouTube de Paul Vengeons (ChatSEO), écrite pour être lue par une IA. Tu le donnes à Claude Code ou à Codex, il comprend la méthode et monte ta vidéo avec : coupe propre, inserts, motion design, sons, sous-titres et appel à l'action.

Il marche pour les chaînes face caméra comme pour les chaînes sans visage, et il commence toujours par récupérer l'identité visuelle de ta chaîne (couleurs, polices, logo) pour que le montage te ressemble.

## Comment t'en servir

1. Ouvre Claude Code (ou Codex) dans le dossier où se trouve ta vidéo brute.
2. Colle-lui ce message :

   > Clone https://github.com/paulv99111/methode-montage-youtube, lis son CLAUDE.md en entier, puis monte ma vidéo `<nom du fichier>`. Ma chaîne : `<lien de ta chaîne YouTube>`.

3. Il te pose quelques questions (chaîne avec ou sans visage, ton lien affilié ChatSEO, ton site), récupère ton branding, puis te montre l'accroche montée avant de faire la suite.

Une question sur la méthode ? Pose-la directement à ton Claude : il a tout le guide.

## Mises à jour

La méthode évolue à chaque vidéo. Ce dépôt est mis à jour automatiquement dès qu'elle change (voir `CHANGELOG.md`). Avant un nouveau montage, demande à ton Claude de faire un `git pull` dans le dossier du dépôt.

## Contenu

- `CLAUDE.md` : la méthode complète (lue par Claude Code)
- `AGENTS.md` : la même méthode (lue par Codex)
- `scripts/branding.py` : récupère les couleurs, la bannière, l'avatar et les miniatures de ta chaîne
- `CHANGELOG.md` : ce qui a changé, et quand
