# Méthode de montage YouTube (vidéos longues)

Ce guide est la méthode de montage des vidéos YouTube de Paul Vengeons (ChatSEO), écrite pour toi, l'IA (Claude Code ou Codex) d'un créateur. Tu ne lis que ce guide et les scripts du dépôt : tout ce qu'il te faut y est. Tu parles au créateur dans SA langue, en mots simples ; les chiffres de ce guide (secondes, dB, LU, px, %, fps) sont des seuils exacts, ne les arrondis pas.

## Comment utiliser ce guide

Ce que tu fais, dans l'ordre, de la prise brute au fichier final :

1. **Questions de départ** (section 1) : chaîne avec ou sans visage, lien de la chaîne, site, lien ou code affilié ChatSEO du créateur.
2. **Étape 0, l'identité visuelle** (section 2) : `scripts/branding.py`, validation du créateur.
3. **La coupe propre** (section 3) : début, fin, silences, ratés, reprises, puis la liste des répétitions à vérifier que le créateur tranche.
4. **L'audio** (section 4) : Adobe Podcast Enhance sur toute la coupe.
5. **Le plan des inserts** (sections 5 et 6) : la liste de tout ce qui passera à l'écran, montrée au créateur par type, validée avant toute fabrication.
6. **La fabrication par morceaux** (section 7) : l'accroche seule d'abord, puis des morceaux de ~5 minutes, chacun vérifié puis montré au créateur.
7. **Le son, le mouvement, les zooms, les sous-titres** (sections 8 à 11), appliqués à chaque morceau.
8. **Le rendu final** (section 12) une seule fois, après le dernier accord, puis les vérifications de livraison.
9. **Les questions du créateur** (section 14), à tout moment.

Règle de conduite : tu ne fabriques rien que le créateur n'a pas validé, et chaque remarque qu'il fait devient une règle écrite (section 13) pour ne jamais refaire la même erreur.

## Ce qu'il faut installer

| Outil | Rôle | macOS | Windows |
|---|---|---|---|
| Python 3.10+ | tous les scripts | `brew install python` | `winget install Python.Python.3.12` |
| ffmpeg / ffprobe | coupe, analyse audio, rendu, contrôles | `brew install ffmpeg` | `winget install Gyan.FFmpeg` |
| yt-dlp | branding, vidéos de référence | `brew install yt-dlp` | `winget install yt-dlp.yt-dlp` |
| Pillow, numpy | images, mesures | `pip install Pillow numpy` | `pip install Pillow numpy` |
| faster-whisper (modèle `small` pour le français) | transcription mot à mot | `pip install faster-whisper` | `pip install faster-whisper` |
| ou whisper.cpp | même rôle, sans Python | `brew install whisper-cpp` | binaires sur github.com/ggerganov/whisper.cpp |
| MediaPipe | visage (cadrage, lèvres, regard), masque de la personne | `pip install mediapipe opencv-python` | idem |
| ou rembg | masque de la personne | `pip install "rembg[cpu]"` | idem |
| ou macOS Vision | masque de la personne (gratuit, natif) | inclus dans macOS (Swift, `VNGeneratePersonSegmentationRequest`) | non disponible |
| Node.js 20+ | moteur de motion | `brew install node` | `winget install OpenJS.NodeJS.LTS` |
| Remotion ou HyperFrames | cartes animées, textes, sous-titres | `npx create-video@latest` (Remotion) ou `npx hyperframes init` | idem |
| pyloudnorm | mesures de loudness (LU) | `pip install pyloudnorm` | idem |
| Adobe Podcast Enhance | nettoyage de la voix | web : podcast.adobe.com/enhance, compte gratuit | idem |
| Pexels, Mixkit, Pixabay, Coverr | B-roll et effets sonores gratuits | web | web |

Sur un Mac Apple Silicon, vérifie que `node` et `python3` sont des binaires arm64 (`file $(which node)`) : un binaire x64 fait échouer les outils de rendu.

---

## 1. Questions de départ

Avant tout, pose ces questions au créateur, une fois, en un seul message :

1. **Chaîne avec ou sans visage ?** Face caméra (il parle à la caméra, même en partie) ou sans visage (voix sur enregistrements d'écran, slides, images d'illustration, avatar, ou rien). La réponse change plusieurs étapes : chaque section a un encadré « Sans visage ». Une vidéo mixte (visage dans l'accroche, écran ensuite) suit les règles visage sur les parties où il est à l'image.
2. **Le lien de sa chaîne YouTube**, et son site s'il en a un (pour l'étape 0).
3. **Son lien affilié ou son code ChatSEO.** Tu ne l'inventes jamais, tu n'en proposes aucun par défaut : sans lui, l'appel à l'action reste en attente.
4. **Les fichiers** : la prise brute (et l'enregistrement d'écran séparé s'il existe), la langue de la vidéo, le plan ou script s'il en a un.
5. **Ses vidéos de référence** s'il en a (un style qu'il aime) : tu peux les regarder avec yt-dlp + ffmpeg (une image toutes les 2 à 4 s) pour mesurer leur rythme.

Ouvre ensuite dans le dossier du projet un fichier local `regles-chaine.md` avec une section « Règles de cette chaîne » (section 13). Tu le relis au début de chaque session.

## 2. Étape 0 : l'identité visuelle (avant tout montage)

**Quoi** : récupérer les couleurs, les polices et le logo de la chaîne, et les faire valider. **Pourquoi** : un montage aux couleurs de quelqu'un d'autre se voit tout de suite ; c'est la chaîne du créateur, pas la nôtre. **Comment** :

1. Lance `python3 scripts/branding.py <lien de la chaîne> [--site <son site>]`. Il écrit `branding/` : avatar, bannière, miniatures récentes, `palette.png`, et `branding.json` (palette, `accent_guess`, neutres, polices du site, points à confirmer).
2. Regarde toi-même `palette.png`, la bannière et 3 ou 4 miniatures, puis montre au créateur : la palette, l'accent proposé (et la couleur principale), les polices trouvées (titre et texte ; à défaut une police lourde proche de ses miniatures, gratuite sur Google Fonts), et demande son logo (fichier PNG ou SVG fourni par lui ; il n'est jamais deviné).
3. Il valide ou corrige. Écris ses choix dans `branding/branding.json` (ajoute des champs `accent`, `primary`, `text_dark`, `text_light`, `font_heading`, `font_body`, `logo`).
4. **À partir de là, `branding/branding.json` est la SEULE source de couleurs et de polices** de toute la vidéo : cartes animées, surlignages, texte derrière la tête, sous-titres, plaques, agenda. Aucune couleur ni police tapée en dur ailleurs.

Correspondance avec la méthode : partout où elle disait « jaune », c'est l'accent de la marque. Si la marque n'a pas d'accent net, garde les valeurs par défaut du guide (jaune `#FEDF00` sur fond sombre, ambre `#A86A00` sur fond clair). Le rouge des cadres dessinés à la main reste rouge, sauf s'il jure avec la marque (accent rouge, ou fond rouge) : alors prends une couleur bien contrastée de la palette et dis-le au créateur. Une police chargée par nom seul retombe souvent en silence sur une police système : charge-la vraiment (Google Fonts, `@remotion/google-fonts`, fichier local) et vérifie sur une image rendue.

## 3. La coupe propre

But : une vidéo qui s'ouvre sur le premier mot, finit sur le dernier, sans blanc, sans raté, sans mot coupé. Tous les temps à partir de l'étape suivante sont pris sur la coupe propre, jamais sur la prise brute.

### 3.1 Transcrire

- Extrais l'audio (`ffmpeg -i prise.mov -vn -ac 1 -ar 16000 audio.wav`) et transcris mot à mot avec faster-whisper modèle `small` (`word_timestamps=True`), langue forcée si la vidéo est courte. **Pourquoi `small`** : les gros modèles inventent plus volontiers (phrase répétée en boucle, mot de liaison jamais dit), et une phrase hallucinée est pire qu'une faute de frappe.
- Les horodatages de Whisper sont des indices, pas des preuves : ils peuvent être en avance de 0,3 à 0,5 s, un mot peut s'étirer sur tout le silence qui le suit, et Whisper écrit le texte VOULU, pas ce qui a été dit (il efface les faux départs).

### 3.2 Trouver les silences sur le son, jamais sur les mots

- **Un silence est proposé par une mesure du son**, jamais par un écart entre deux mots Whisper (qui peut lire 0,00 s sur un vrai silence d'une seconde).
- **Le seuil vient de l'enregistrement, pas d'un dB fixe** : calcule l'enveloppe RMS par pas de 20 ms (passe-haut 80 Hz d'abord), balaie les seuils et prends le milieu du plus large plateau (la plage de seuils qui donnent tous les mêmes silences). Pas de plateau : reviens à `silencedetect=noise=-35dB`. Pourquoi : -35 dB peut manger la voix sur un enregistrement calme, ou ne jamais rien trouver sur un enregistrement bruité.
- **Fusionne deux silences séparés de 0,06 s ou moins** avant de filtrer par longueur : un clic ou une respiration coupe sinon une vraie pause en morceaux trop courts pour être coupés.
- Un mot daté à l'intérieur d'un silence mesuré est déplacé à la fin de ce silence, sinon la coupe l'avale. Chaque mot compte comme barrière, y compris les mots de durée nulle (ils se groupent en début de phrase).
- Réglages vidéo longue : silence coupé à partir de **1,0 s**, on garde **0,12 s** après le dernier mot et **0,30 s** avant le mot qui reprend (Whisper date les reprises en retard). Une pause de **0,80 s ou plus** est un point de montage : on ne garde que **0,05 s / 0,08 s**. Aucune coupe de moins de **0,05 s** (une coupe de 0,06 s ne s'entend pas mais fait sauter l'image). Une pause entre phrases plus courte reste : c'est le rythme de la parole. Ne descends jamais sous **0,30 s** de seuil (l'espace normal entre mots français fait 0,15 à 0,25 s).

### 3.3 Début et fin

- **La vidéo s'ouvre sur le premier mot**, rien devant par défaut. Le début se lit sur les lèvres (MediaPipe FaceMesh : les lèvres se ferment pour un « P » environ 0,5 s avant le son), puis se vérifie sur la forme d'onde : l'image démarre **0,15 s** avant l'attaque de la voix. La fin : **0,25 s** après le dernier son (0,5 s après la bouche fermée au plus), jamais jusqu'au moment où il se lève ou tend la main pour arrêter la caméra.
- Aucune coupure de prise ne vient après le dernier mot.
- **Chaque point de coupe se lit sur la forme d'onde**, jamais sur un horodatage Whisper seul : un début posé sur du silence est avancé jusqu'à l'attaque de la voix moins son avance, une fin jusqu'à la retombée plus la marge. Pourquoi : sinon la vidéo s'ouvre sur une seconde de vide.

### 3.4 Ce qui part toujours

- **Un morceau gardé de moins de 1,5 s sans aucun mot Whisper est un bruit**, pas de la parole : il part. Un mot sans lettre (« ... ») n'est pas un mot. Pourquoi : deux bouts de 0,3 s font sauter la tête avant une phrase.
- **Une pause où il lit son plan part en entier, bruits compris** : tout morceau de moins de 1 s sans mot, coincé entre deux silences de plus de 1,5 s, est retiré. Puis détecte le regard baissé sur la coupe : inclinaison de la tête (FaceMesh) au-dessus de **0,40** pendant plus de **0,5 s**, et coupe chaque passage qui n'est pas sous un insert plein écran. Pourquoi : le spectateur le voit regarder son ordinateur en silence.
- Un morceau sans aucun mot entre deux changements de prise part entier : ses deux coupes deviennent une seule.

### 3.5 Les reprises (raté, silence, il recommence)

- Un silence de **0,7 s** ou plus, dont les 3 mots suivants (2 s'ils ne sont pas des mots-outils) recommencent quelque chose dit juste avant, dans la même prise et au plus **15 s** en arrière : c'est une reprise. On coupe le raté, on garde la reprise. Liste chaque reprise coupée avec son texte, et écoute tout long silence que tu n'as pas expliqué.
- **Whisper replie parfois un essai raté en un seul mot** qui court du premier essai au second : retranscris séparément les deux côtés de tout long silence traversé par un seul mot, puis cherche la reprise. Refuse tout mot de **0,9 s** ou plus qui traverse un changement de prise.
- **La jointure d'une reprise est une phrase complète** : le mot de liaison qui ouvrait la reprise juste pour recommencer (« donc », « et », « alors », « bon », « du coup », « en fait ») part avec la coupe. S'il est collé au mot suivant sur la forme d'onde, garde les mots communs du PREMIER essai et reprends après eux dans le second. Retranscris la jointure et lis-la comme une phrase avant de la garder.

### 3.6 Les jointures

- **Une jointure ne colle jamais deux mots** : le silence entendu à travers toute coupe vaut au moins la pause médiane du créateur dans sa prise, jamais moins de **0,25 s**, pris dans le silence de la partie retirée. Signale toute jointure trop courte.
- **Un côté gardé n'emporte jamais le premier son d'un mot retiré** : en parole liée (liaison, sans pause), la frontière de Whisper tombe DANS le mot suivant ; coupe au creux d'énergie entre les deux mots, lu sur la forme d'onde. Pourquoi : on entendrait le « a » du mot supprimé.
- **Une nouvelle section s'ouvre sur son premier mot** : la pause avant une section reste du côté sortant (sur une respiration atténuée), le morceau entrant démarre **0,1 s** avant l'attaque de la voix.
- **Prouve chaque coupe** : mesure l'enveloppe dans les 60 ms juste à l'intérieur de chaque bord retiré (elle doit être très en dessous du niveau de la voix, sinon un mot a été mordu), puis retranscris la coupe et compare ses mots à la transcription d'avant ; vérifie par son nom le premier mot qui reprend après chaque coupe (le mot manquant est l'erreur typique).
- Avant d'ajouter un mot que le petit modèle a raté (parce qu'un plus gros l'a entendu), mesure le niveau sonore à cet endroit (`volumedetect`) : un gros modèle invente volontiers un « Ensuite » sur du bruit de pièce.

### 3.7 Les répétitions : une liste, le créateur tranche

Hors accroche, **tu ne coupes jamais une répétition toi-même**. Pourquoi : la plupart sont son style (insistance, liste, reprise pour expliquer), et une coupe à tort abîme sa façon de parler.

1. Marque chaque endroit ENCORE dans la coupe qui peut être une erreur : une phrase dite deux fois, une voix sans aucun mot Whisper (souvent un premier essai effacé), et toute reprise de la même idée avec d'autres mots que tu repères en LISANT la transcription (jamais par une expression régulière). L'emphase « X et X » n'en est pas.
2. Donne à chaque endroit un verdict, les ratés d'abord :
   - **Raté (faux départ)** : il commence une phrase, s'arrête avant de la fermer et la redit à partir des mêmes premiers mots, en changeant souvent la fin. Rien ne ferme la première copie : ni point ni virgule dans les mots Whisper, aucun mot de liaison (et, mais, donc), au plus 3 mots avant la reprise. Un signal de reprise (pardon, attends, non, je recommence, euh + les mêmes mots) en fait un raté quelle que soit la ponctuation.
   - **Voulu** : une première copie fermée. Une liste ou un parallèle (« de tes offres, de tes prix »), une reprise des derniers mots pour les expliquer, une précision (« un fichier, donc un fichier avec... »), une question à laquelle il répond.
   - Un passage de voix sans mot est un raté jusqu'à ce qu'on l'ait écouté.
   - On garde la DERNIÈRE prise complète ; si la dernière est la cassée, on garde la précédente et la raison le dit.
3. Montre la liste au créateur : pour chaque endroit, le temps, le texte, le verdict, et deux extraits audio (avant / après coupe proposée). Il choisit ce qui part. Seulement alors tu places chaque jointure (règles 3.6) et tu passes à la suite.

**Exception, l'accroche : chaque idée n'y est dite qu'UNE fois.** Liste les idées de l'accroche (la promesse, la crédibilité, le problème, le résultat...), garde la prise la plus complète de chacune, et présente chaque coupe au créateur comme UN son par coupe, écrit en trois parties sur une ligne : la fin de ce qui précède, les mots retirés ~~barrés en entier~~ (tous les mots que le son saute, transcrits, jamais résumés), le début de ce qui suit. Il valide à l'oreille avant qu'un seul insert, zoom ou son soit fabriqué sur l'accroche. Vérifie chaque jointure en retranscrivant 2,5 s de chaque côté.

### 3.8 L'éditeur de coupe

Donne au créateur un moyen de voir et rouvrir chaque coupe (par exemple une page HTML locale avec un proxy 720p de la prise brute à 30 fps, une image clé par seconde, les morceaux gardés côte à côte, chaque coupe colorée par sa raison : blanc ou erreur, une case par type pour masquer ses marques, et sous la frise, pour chaque erreur, « Avant » et « Après »). Les blancs n'ont pas besoin d'écoute. Garde les morceaux en JSON (secondes de la prise brute) ; après ses modifications, recoupe, refais la correspondance des temps de la transcription et l'audio (section 4).

> **Sans visage** : pas de lèvres ni de regard baissé. Le début, la fin, les silences et les reprises se trouvent uniquement sur la voix (forme d'onde + transcription). Ajoute un contrôle propre à l'écran : un passage où l'écran ne bouge pas et où la voix se tait (il cherche quelque chose, une page charge) se coupe comme un blanc ; un chargement long se raccourcit en gardant le début et le résultat.

## 4. L'audio

- **Toujours Adobe Podcast Enhance, sur toute la coupe**, pas de test avec/sans. Pourquoi : une voix propre et pleine retient mieux qu'une voix de pièce. Le plan gratuit accepte environ 30 min par fichier et 1 h par jour : envoie la coupe en fichiers de moins de **28 min**, coupés dans un silence entre deux mots, puis recolle-les à l'échantillon près sur l'image (vérifie la synchro).
- Si Enhance n'est pas disponible : un débruitage + restauration locale (par exemple Resemble Enhance) n'est qu'un secours ; sa sortie peut arriver ~40 ms en retard (recale-la et revérifie la synchro), et ne livre jamais une voix que le créateur ne reconnaît plus. Compression douce (2:1 à -24 dB), pas de compression forte : elle remonte l'écho.
- Après chaque nouvelle coupe validée, refais Enhance sur la nouvelle coupe.
- Livraison YouTube : la voix autour de **-14 LUFS** intégrés.

## 5. Ce qui passe à l'écran : une question par phrase

Pour chaque phrase, demande-toi : **que doit VOIR le spectateur pour suivre ou croire ceci ?** Prends la PREMIÈRE ligne qui convient. Quand deux lignes conviennent, la plus haute gagne : un vrai écran bat le motion, le motion bat la banque d'images, les images du créateur battent tout.

| Le créateur... | À l'écran |
|---|---|
| 1. Donne une ÉTAPE à faire (un clic, un menu, un réglage, un champ, un endroit d'une appli, d'un site, d'un appareil) | **L'enregistrement réel de cet écran ou objet.** Un temps par nom : chaque élément nommé a son zoom (1,5 à 2,2x) et son cadre au moment où il est dit ; chaque valeur est tapée en direct sur son mot |
| 2. Cite un chiffre ou une affirmation (étude, article, éditeur, page officielle) | **Sa vraie page source**, la phrase exacte surlignée, le chiffre encadré. Jamais un gros chiffre seul |
| 3. Donne son propre résultat, une preuve, une crédibilité | Son vrai compte ou sa vraie page, le chiffre surligné (tableau de bord, profil, article de presse, podcast) |
| 4. Donne quelque chose à copier mot pour mot (prompt, formule, modèle, commande) | TAPÉ EN DIRECT là où on l'utilise, plein écran et lisible, puis le résultat qui arrive |
| 5. Montre un outil ou un processus qui TOURNE | L'enregistrement qui tourne, coupé jusqu'au résultat, la sortie clé surlignée |
| 6. Donne un exemple | Sa vraie page, son vrai produit, sa vraie réponse, une capture par étape. Idéalement UN exemple suivi toute la vidéo |
| 7. Nomme un outil, un site, un produit, un lieu, une personne une fois, sans étape | 2 à 3 s de la vraie chose, son nom ou son domaine en légende |
| 8. Énonce une règle sur un document ou un objet (longueur, structure, partie) | Montrée SUR un vrai, avec des étiquettes dessinées : noms à côté des parties, compteur en direct, cadre pointillé avec la limite |
| 9. Liste 3 éléments ou plus, une méthode, une checklist | Un élément PAR élément dit, jamais tout d'un coup. Jusqu'à ~4 éléments courts : à côté du visage. Une longue énumération (une minute ou plus) : UN visuel plein écran qui grandit carte par carte, sans retour au visage entre les éléments |
| 10. Explique un concept, un mécanisme, une comparaison, une tendance, sans vrai écran derrière | Motion : carte mentale, graphique qui se dessine, courbe, entonnoir, flux, deux colonnes construites paire par paire |
| 11. Apprend une façon de faire (écrire, parler, concevoir) | Avant / après : la mauvaise version, puis la bonne avec sa partie clé surlignée, ou la longue barrée mot par mot jusqu'à la courte |
| 12. Invente ou définit un terme, pose la question du chapitre, corrige un mot | Légende sur son visage la première fois ; la question tapée ; une correction = barré puis le bon mot |
| 13. Cite des marques, des noms, des petites idées en passant | Logo ou icône qui apparaît À CÔTÉ de son visage sur le mot, le visage reste |
| 14. Décrit une situation de tous les jours | B-roll de toute la situation, 1,5 à 4 s |
| 15. Donne un avis, une histoire, une explication, un avertissement, une blague, une parenthèse | **On reste sur son visage** : la façon de le dire est le contenu. Un punch-in (cadrage plus serré) sur la phrase clé donne du rythme sans insert |

- **Une phrase VISUELLE est la ligne 6, même hypothétique** : toute phrase qui décrit quelque chose qu'on pourrait VOIR (un tableau, un quiz, une vidéo dans un article, une grille de produits, un titre dans Google) montre une vraie page en ligne qui l'a, la chose encadrée sur son mot, une capture par chose nommée. Une plaque de texte ou une icône à la place est un raté.
- **Un sujet sans écran** (un geste, un lieu, un objet) : les lignes 1 à 8 s'appliquent quand même, l'« écran » devient un vrai enregistrement ou une vraie photo de la chose, surlignée de la même façon. Jamais une maquette dessinée de ce qui peut être filmé.
- Une phrase qui n'a pas d'insert n'a rien : le visage est le choix par défaut.

> **Sans visage** : le plan par défaut n'est plus le visage mais l'enregistrement d'écran en cours (ou, sans écran, la carte animée en cours). La ligne 15 devient « on reste sur l'écran qui parle de ça », avec une lente poussée sur la capture ; les lignes 12 et 13 posent la légende ou le logo sur l'écran, dans une zone vide, jamais sur ce qu'il faut lire.

## 6. Les inserts : comment ils sont faits

### 6.1 Les quatre types, mélangés

Chaque morceau mélange les quatre types d'inserts : **les vrais écrans, les cartes motion plein écran, les plaques qui apparaissent à côté de lui (près de ses mains), le texte derrière sa tête.** Chaque plan visage assez long pour un « moment de mot » reçoit une plaque (une crédibilité, un élément de liste, une date, un terme précis, une URL) ou une ligne derrière la tête (une phrase choc, une question qu'il pose, un titre de section) ; la carte plein écran est gardée pour les temps forts de l'argument (le problème barré, le tournant, la promesse). Pourquoi : deux types seulement, et la vidéo devient prévisible.

Contrôle automatique sur la fiche des éléments : **échec** si un type est absent pendant **60 s**, ou si **trois moments de mots d'affilée** utilisent le même type. Dans l'accroche, environ la moitié des moments de mots sont des cartes plein écran, le reste des plaques ; deux de suite du même style restent l'exception. Les vrais écrans plein écran ne sont jamais de trop : une capture est toujours précise.

**Le visage reste à l'écran** : au moins **50 %** du temps de l'accroche et **55 %** du corps. **Jamais plus de 2 éléments plein écran d'affilée** (moins de 2 s de visage entre eux comptent comme d'affilée) : le troisième devient une plaque ou une ligne derrière la tête, et un écran trop long est raccourci à sa preuve.

> **Sans visage** : les quatre types deviennent : vrais écrans, cartes motion plein écran, plaques posées sur la capture (zone vide), texte cinétique sur l'écran (à la place du texte derrière la tête). Les règles de part de visage deviennent des règles de variété : aucun même type plus de 60 s d'affilée, jamais plus de **2** cartes motion d'affilée sans retour à la capture, et la capture reste au moins **55 %** du corps quand la vidéo est une démo.

### 6.2 Vrais écrans, surlignés, exacts

- **Une vidéo plutôt qu'une image dès que la chose bouge** (défilement, clic, menu qui s'ouvre, résultat qui charge). Une image fixe seulement pour ce qui ne bouge pas (un chiffre, une ligne), et même là elle bouge : lente poussée + surlignage qui se dessine.
- **Le surlignage est le message.** Un texte (ligne, chiffre, colonne, titre) : un surligneur à la couleur d'accent de la marque qui balaie de gauche à droite en **0,3 à 0,4 s**, derrière le texte (mode « multiply »), et arrive sur le mot qui le nomme. Un élément (bouton, champ, menu, partie d'objet) : un cadre, une ellipse ou une flèche courbe ROUGE dessinés à la main. Un seul surlignage à la fois ; le reste peut s'assombrir de ~30 %. Ce qui ne compte pas, et tout ce qui est privé (données d'une autre personne, adresse email, montant qu'il ne voulait pas montrer), est flouté ou couvert.
- **Exactement ce qu'il nomme, sur un vrai compte** : le sien d'abord, sinon une page publique en ligne ; si la chose demande un compte qu'il n'a pas, propose-lui d'en créer un GRATUIT (jamais d'offre payante, jamais de carte). Un HYPOTHÉTIQUE (une conversation qui n'a jamais eu lieu, un résultat futur) est dessiné comme une carte clairement stylisée, jamais faux comme une capture.
- **La date compte** : la capture de ce qui change (un classement, une réponse d'IA, un prix) se fait le jour du montage.
- **Un visuel tiré de la démo d'un éditeur porte une étiquette** (une pastille « VISUEL <ÉDITEUR> » dans la barre du navigateur) pour que personne ne le prenne pour les chiffres du créateur.
- **Capture** : un navigateur piloté (Playwright ou le protocole DevTools de Chrome, capture d'écran en continu) donne des défilements fluides ; jamais la fenêtre personnelle du créateur. Une capture devient un clip à sa propre cadence d'images, jamais une suite d'images fixes concaténées.
- **Un défilement ne saccade jamais** : Chrome arrondit un défilement au pixel entier, donc un défilement lent filmé puis zoomé avance « immobile, immobile, saut ». Filme le défilement plus vite (environ 3 fois) et ralentis-le au montage, puis vérifie chaque capture : le déplacement d'une image à l'autre (corrélation de phase avec numpy) doit être régulier. Une capture qui échoue est lissée (nouvelle interpolation dans le temps), jamais refilmée (le contenu aurait changé). Après un lissage, chaque cadre de cet insert est redessiné sur l'image lissée où il apparaît, et regardé avant le rendu.
- **Cadrage, trois choix** : plein écran quand il faut LIRE (un chiffre, un filtre, un prompt) ; plein écran avec SON VISAGE DANS UNE BULLE arrondie dans un coin quand la démo est longue et qu'il continue à parler ; écran partagé (la chose 60 %, le visage 40 %) quand son explication compte autant que la chose. Une légende ne couvre jamais l'endroit surligné.
- **Démo filmée pendant le tournage** : l'enregistrement d'écran plein cadre (fenêtre arrondie, zoom automatique sur l'action), sa caméra en petite incrustation en bas à droite ; retour net au visage plein écran quand il relève les yeux. S'il a filmé son écran, utilise-le ; sinon, capture après coup selon les règles ci-dessus.
- Les vrais écrans de l'accroche flottent sur un fond sombre ou clair (aux couleurs de la marque) avec une lueur.

### 6.3 Les cadres rouges

- **Un cadre ne croise jamais un texte**, vérifié par la machine sur l'image où il arrive : il couvre toute la phrase qu'il nomme (mesurée sur la capture, fins de mots comprises), ses marges rétrécissent côté par côté jusqu'à ce qu'aucun bord, trait compris, ne traverse une lettre ni la ligne du dessus ou du dessous ; un cadre qui croise encore à la marge minimale est remesuré. Une phrase dans un texte dense prend un cadre serré ; une ligne de code, trop dense pour un cadre, prend le surligneur.
- **Un mot couvert par le cadre dégage chaque bord de 2 px** (un mot « presque dedans », sa dernière lettre sous le trait, est un échec).
- **Un cadre sur plusieurs lignes encadre des lignes entières** : il finit en fin de ligne, jamais au milieu.
- **Un cadre tient entier dans sa fenêtre** : la fenêtre ne zoome jamais au-delà de sa découpe ; choisis une image où l'élément est plus haut, ou prolonge la découpe dans une zone de page blanche. Refuse le rendu si un cadre dépasse.

### 6.4 Structure : l'agenda

- **La carte de la vidéo est à l'écran** : un agenda au début (les parties de la vidéo), qui revient à chaque chapitre avec la partie en cours allumée. La carte allumée EST le titre du chapitre : jamais de légende « 5/ chapitre » en plus. Une section qui s'ouvre sur une question montre la question tapée.
- Un seul kit de motion pour toute la vidéo, aux couleurs et polices de `branding.json`. Une liste ou un plan se révèle dans l'ordre où il est dit.

### 6.5 Le texte derrière la tête

Un type d'insert comme les autres (sa fréquence suit les mêmes règles), sur un plan visage, jamais sur un écran : pour une phrase choc, un tournant, un titre de section dit à la caméra.

- **Forme** : 2 lignes maximum, 1 à 3 mots chacune, en capitales, la police de titre de la marque (une linéale épaisse à défaut), une ligne en couleur de texte et une en accent. Sur un mur clair, le texte est foncé et la ligne d'accent est en lettres d'accent contournées de foncé ; blanc seulement dans une pièce sombre. **Des lettres seulement, jamais un bloc de couleur derrière les mots.**
- **Place** : à hauteur de tête et d'épaules, la tête du créateur passe devant les lettres. Pas plus bas que le menton (un bras de micro ou un objet de bureau n'est pas dans le masque, le texte passerait par-dessus).
- **Grand et entier** : sur une image 1920x1080, une ligne monte jusqu'à **340 px** de haut, deux lignes **235 px** chacune (**282 px** pour une paire courte), ajustées à **1 700 px** de large ; le texte fait au moins **45 %** de la largeur de l'image et ses capitales au moins **190 px** (sinon raccourcis la ligne, ne la rétrécis pas). La boîte qui masque l'entrée des lettres laisse **0,17 em** au-dessus de la ligne pour les accents (ils montent jusqu'à ~0,12 em au-dessus de la boîte de ligne et seraient coupés).
- **Rien n'apparaît avant son mot** : une ligne reste cachée jusqu'à son mot, ses lettres attendent à **140 %** sous elle. Vérifie l'image juste avant le mot : zéro pixel dessiné (sinon un petit point traîne sur le décor).
- **Pas de trait sous le texte** : une boîte qui s'anime en `overflow: hidden` peut peindre le bas d'une lettre en fine ligne ; découpe avec `clip-path: inset(0)`, et scanne chaque image du clip pour une bande de 5 rangées ou moins, 8 rangées ou plus sous l'encre, qui dure 3 images.
- **Comment** (gratuit) : un masque de la personne image par image (MediaPipe Selfie Segmentation, rembg, ou macOS Vision), adouci de 2 px ; on compose le fond, puis le texte, puis la personne. Les mots arrivent sur leur mot dit et partent quand le sujet change.
- **Le masque est calculé sur le cadrage FINAL** : un seul plan de zooms est calculé sur tout le film, chaque aperçu et chaque segment du rendu final en prend sa tranche. Pourquoi : si le zoom repart de zéro à chaque rendu, le masque ne colle plus et un halo de mur apparaît autour de la tête dans les lettres. Refuse un texte dont l'image diffère de celle du masque, et avant de livrer, regarde une image de CHAQUE texte derrière la tête dans le rendu final (planche contact), pas seulement dans les aperçus.

> **Sans visage** : pas de texte derrière la tête. Il est remplacé par du texte cinétique sur l'écran (gros mots qui arrivent sur leur mot, dans une zone vide de la capture ou sur la capture assombrie), avec les mêmes règles de taille, de lettres seules, de « rien avant son mot » et de « pas de trait sous le texte ». Si la chaîne utilise un avatar ou une vidéo d'illustration avec une personne, le texte derrière la personne reste possible avec le même masque.

### 6.6 B-roll

- **Rare** : 2 à 5 plans par vidéo (12 à 50 min), toujours une situation de tous les jours, jamais du remplissage (mains qui tapent, café, circulation sur rien). Gratuit, usage commercial, sans attribution : Pexels, Mixkit, Coverr, Pixabay ; aucune marque visible dans le clip. Garde l'URL source de chaque clip dans le projet. Jamais deux d'affilée ; jamais sur son avis ni son histoire. Pas d'images de banque bon marché à la place d'une illustration.
- Les légendes à l'écran sont dans la langue de la vidéo, les mots qu'il dit ou leur mot clé.

### 6.7 L'appel à l'action ChatSEO

- **Avant 25 % de la durée de la vidéo**, avec le lien affilié ou le code du créateur (demandé en section 1, jamais inventé). Vérifie sur la transcription que le créateur le dit avant ce seuil ; sinon, dis-le-lui et propose un endroit naturel avant 25 % (une fin de section) où il peut l'enregistrer.
- À l'écran : la vraie page de ChatSEO (capture du jour, ligne 7 ou 3 de la table), puis son code ou son lien en légende lisible, aux couleurs de sa marque, pendant qu'il en parle. Rappelle-lui de mettre le même lien en haut de la description.

## 7. La fabrication par morceaux

### 7.1 Le plan des inserts, validé avant toute fabrication

Écris `inserts.md` à partir de la transcription de la coupe propre, une ligne par insert, dans l'ordre : `N. <section> · « <les mots sur lesquels il arrive> » · <ligne de la table> · <URL exacte, appli ou fichier> · <ce qui est surligné> · <cadrage>`, plus l'agenda et ses retours. Montre-le au créateur **par type** : pour chaque type, une phrase simple de ce que tu feras (« Quand tu parles d'un outil : la vraie page, filmée, surlignée »), puis, repliés, tous les inserts de ce type avec leur temps sur la coupe propre (`2:46 · « ses mots » → ce qui s'affiche`). Il dit OK ou À changer par type et corrige une ligne. **Rien n'est capturé ni rendu avant que chaque type soit OK.**

### 7.2 L'accroche d'abord, seule

- L'accroche (les ~60 premières secondes) : plans visage coupés par des inserts toutes les **2 à 5 s** : ses vrais écrans flottants sur fond avec lueur, des légendes de mots clés (texte clair + un mot en gras italique couleur d'accent, « Quelles **étapes** suivre »), des logos avec flèches (« que j'utilise **Claude** »), des preuves (ses profils, ses courbes, ses résultats, l'équipe en avatars ronds). Sur une référence mesurée : un mouvement toutes les ~2,3 s, l'image la plus longue sans mouvement ~11 s. Pas de zoom fixe et pixelisé dans l'accroche ; montre son écran à chaque fois qu'il y fait référence. Musique : cinématique, pas « fun ».
- **Ne monte jamais l'accroche avant que l'enregistrement existe** (une vidéo repoussée = du travail perdu).
- Un deuxième type d'accroche (un teaser monté à partir des meilleurs moments du corps) seulement si le créateur le demande, comparé à son accroche enregistrée.

### 7.3 Puis des morceaux de ~5 minutes

**Un corps long ne se fabrique jamais en une seule passe** : les mêmes effets reviennent en boucle sur 30 minutes. Découpe en morceaux d'environ 5 minutes, coupés sur les chapitres de la vidéo. Pour chaque morceau :

1. **Sa fiche des éléments** : chaque insert avec son temps, son type, son entrée et son son ; vérifiée contre les cibles de densité (6.1, 7.5) et les règles de variété (section 9).
2. **Un aperçu 1080p de ce morceau seul**, vérifié par toi (sections 8 à 11) avant de le montrer.
3. **Les remarques horodatées du créateur**, chacune écrite comme règle dans `regles-chaine.md` dans le même tour (section 13).
4. Le morceau suivant.

**Une fois l'accroche ET le premier morceau validés, les morceaux restants se font en UNE passe**, sans attendre son accord entre chaque : tu écris toi-même chaque fiche, vérifiée contre la densité et la variété ENTRE morceaux (jamais deux morceaux avec la même suite d'entrées ou de sons), tu rends les aperçus 1080p l'un après l'autre, et tu les lui montres ensemble. Jamais avant que le premier morceau soit validé : c'est là que les règles de la chaîne s'apprennent. Le 4K n'est jamais rendu avant l'accord final.

À partir du deuxième morceau, les inserts sont calés sur les mots de la coupe propre (pas sur la frise montée) : un morceau retiré plus tard ne décale alors aucun texte de son mot.

### 7.4 Une correction revient comme son propre clip

Enregistre chaque remarque du créateur AVANT de la corriger (temps sur la frise, ~1 s de contexte de chaque côté, ce qui est corrigé). Après le nouvel aperçu, découpe **un clip par MODIFICATION** et montre-les d'abord, chacun avec sa légende, puis l'aperçu complet. Une même modification faite à plusieurs endroits reste un seul clip, chaque endroit marqué : une barre segmentée en haut, le segment joué en couleur d'accent, et un badge « 2/5 · 0:38 de l'aperçu » (sans marque, il croirait voir des coupes bizarres). Un clip d'un seul endroit n'a pas de marque.

### 7.5 Densité et timing

- **Cibles de densité** (éléments plein écran, toute la vidéo) : environ **8 s** entre deux éléments ; **45 à 73 %** des 75 premières secondes hors visage. Dans le corps (après 75 s) : médiane ~**11 s** entre éléments, ~**26 %** hors visage, aucun plan visage de plus de ~**45 s** ; les éléments tombent sur chaque outil, chiffre, exemple (en rafale), concept et changement de section, et la plupart durent 1 à 4 s. Mesure le rendu avant de le montrer. Pourquoi : une accroche dense et un corps vide donnent « trop de face caméra ».
- Ces rythmes sont des moyennes, jamais un minuteur : du mouvement sans information rend la vidéo plus dure à suivre.
- **Arrivée sur le mot qui le nomme**, jamais avant, jamais une phrase en retard ; le surlignage tombe sur le mot lui-même, chaque élément de liste sur son mot.
- **Net en 0,5 s, jamais vide** : l'entrée floutée d'un insert plein écran est finie en **0,34 s** et son premier contenu est à l'écran à **0,3 s**. Une marque ou un mot calé avant le début de l'insert ne retarde jamais l'entrée : il arrive juste après. Vérifie sur le RENDU, pas sur la frise.
- **Un insert qui couvre un changement de prise commence avant et finit après** : jamais une coupe cachée à moitié.
- **Sortie quand le sujet change**, pas avant que le spectateur ait lu ou vu l'action.
- Durées : un écran tient le temps de l'étape (un clic ~3 à 6 s, un tutoriel complet 10 à 20 s), une carte de mot ~1,5 s, un B-roll 1,5 à 4 s. Un visage seul peut tenir 25 à 40 s sur une explication.

> **Sans visage** : les pourcentages « hors visage » deviennent « hors capture d'écran » ; garde l'écart moyen de ~8 s entre deux éléments ajoutés (carte, plaque, texte cinétique, zoom sur la capture) et aucune image immobile de plus de ~11 s dans l'accroche.

## 8. Le son des inserts

Deux indicateurs : **chaque événement à l'écran a son son**, et **aucun son n'est trop répété**. Le remède à « trop d'effets sonores » est presque toujours plus de sons DIFFÉRENTS, jamais moins d'événements.

1. **Au moins 90 %** des événements (entrée, clic, coche, tampon, coupe, mouvement de caméra entre deux étapes, compteur qui tourne) ont un son placé SUR l'événement (avec le mouvement, jamais sur un mot). Exception : les mots d'une légende cinétique, la voix est leur son.
2. **Le son correspond à ce qui se passe** : une famille de sons par type d'événement (une page glisse et tombe, une pastille fait « pop », une case coche, un tampon tamponne, un curseur clique, du texte se tape, un compteur roule). Une action continue = UN son (un prix qui défile = un roulement, jamais dix tics).
3. **Clic sur le visage, souffle sur le plein écran** : un pop ou un clic seulement pour une plaque, un logo ou un mot qui arrive PAR-DESSUS le visage ; une carte plein écran entre sur un « whoosh », et chaque ligne qui arrive ensuite dedans sur un souffle doux, sous l'entrée de la carte. Dans un corps sans musique, la carte de chapitre et son whoosh sont **6 dB** sous ceux de l'accroche.
4. **Toujours sous la voix** : le coup le plus fort reste au moins **3 LU** sous le niveau typique de la voix (loudness momentanée) ; l'ensemble des effets **17,5 LU** sous la voix ; la musique **21,5 LU** sous la voix après son atténuation (« ducking ») quand il parle. Mesure la voix et règle effets et musique par rapport à elle, jamais avec des niveaux absolus recopiés d'un autre projet.
5. **Chaque coup au même volume, à l'oreille** : mesure en pondération K, fenêtres de 200 ms (pyloudnorm), et ramène chaque coup à **4 LU** ou moins de la médiane. Une lecture de crête ou de RMS ne suffit pas (un « thud » grave et un clic aigu « mesurent » pareil). Coupe un coup à **1,2 s** (un long fichier « pop » en joue trois) ; mesure un son de frappe ou de roulement sur sa fenêtre typique ; deux événements simultanés se partagent le niveau au lieu de s'additionner.
6. **Aucun fichier trop joué** : un même fichier au plus **3 fois par minute** de film, et jamais deux fois en **4 s**. Une famille qui revient souvent a au moins **4** fichiers différents, en rotation, avec une petite variation de hauteur et de gain sur chaque coup. Découper un long enregistrement en prises distinctes compte comme des variantes ; le même fichier à une autre hauteur, non. Sons gratuits : Pixabay, Mixkit.

## 9. Le mouvement des inserts

1. **Quelque chose bouge toujours** : au plus **40 %** d'images immobiles (différence d'image à 24 fps). Le texte se tape, les lignes grandissent, les cartes flottent, un curseur clique ce que la voix nomme, les chiffres roulent, la phrase clé se surligne.
2. **Bouger n'est pas trembler** : l'image entière ne change jamais de sens d'une image à l'autre pendant plus de **0,6 s** (mesure : corrélation de phase sur chaque image). Avec GSAP, un `fromTo` sur une secousse ou une échelle affiche sa valeur de départ dès la construction dans un rendu image par image : mets `immediateRender: false`.
3. **Même type d'objet, même mouvement ; objets différents, mouvements différents** : toutes les pages web entrent de la même façon dans un film (la cohérence se lit comme du design), mais pastille, carte, tampon, compteur ont chacun le leur. Au moins **6** styles d'entrée par film, aucun (la frappe mise à part) sur plus de **35 %** des entrées. Jamais deux morceaux avec la même suite d'entrées.
4. **Un film ne montre jamais ses images** : tout est rendu en **60 fps**, et jamais sous la cadence de la prise caméra (lue sur le fichier avec ffprobe, jamais tapée en dur). Un insert est dessiné à la résolution du rendu final (4K pour un film 4K), jamais un 1080p agrandi. Un mouvement sec (claque, fouet, glissé rapide) porte un flou de mouvement ; un mouvement lent reste net. Contrôle : échec sous **50 fps** ou sous la cadence de la prise.
5. **Riche dans le temps, simple à chaque instant** :
   - une seule chose à lire à la fois : le titre OU la légende, jamais deux textes qui disent des choses différentes ;
   - un seul objet héros par temps, grand et centré ; rien de décoratif qui ne porte pas de sens ;
   - ce qui part, part : quand l'objet suivant arrive, le précédent sort ou s'assombrit fort, jamais une pile ;
   - le test : une image fixe de chaque temps, lue sur un téléphone en une seconde. Si l'œil doit choisir où regarder, retire un élément.

## 10. Les zooms et les punch-ins

Les zooms se posent EN DERNIER, à partir des inserts terminés (accroche comprise).

- **Corps, il parle** : plein écran sur lui, en alternant un cadrage large et un cadrage serré toutes les quelques secondes (le punch-in).
- **Taille lue sur le cadrage** : mesure le visage (MediaPipe) ; le punch-in l'amène à ~**22 %** de la hauteur de l'image, plafonné à **1,40** (une source 4K reste nette). Un plan large (visage à 14 %) : serré **1,35**, moyen **1,19** ; un plan déjà serré redescend vers **1,08**. Alterner large, serré, large, moyen. Le zoom est ancré sur le VISAGE, pas sur le centre de l'image.
- **Trois types** : le SAUT (en 2 images) agit comme une coupe et tombe sur un silence ; la POUSSÉE LENTE se sent sans se voir (chaque plan de 3 s ou plus en a une, sous la parole, à **1,5 %/s**, plafonnée à **+10 %** et à 1,40, qui monte vers le saut suivant, plus une dans l'accroche) ; le RETRAIT ramène doucement un punch-in moyen de 4 s ou plus au large sur toute sa durée (il coûte un saut au lieu de deux).
- **Budget des sauts** : un toutes les ~**10 s** en moyenne, jamais deux en **5 s**, jamais plus de **3** en **30 s** (un punch-in et son retour comptent pour 2). Pourquoi : trop de zooms fatiguent.
- **Autour des inserts plein écran** :
  - un changement de cadrage visible est à **1 s** ou plus d'un bord d'insert ; plus près, il se déplace sur ce bord, où l'insert le cache (sinon on voit une demi-seconde de zoom puis un saut, qui ressemble à un bug) ;
  - **le visage que rend un insert tient** : un seul cadrage jusqu'au prochain élément plein écran si celui-ci est à 5 s ou moins ; sur un plan plus long, le premier changement attend **2,5 s** et tombe au début d'une nouvelle phrase ou proposition ;
  - **un insert cache la coupe franche voisine, il ne la montre jamais** : un bord d'insert à **0,6 s** ou moins d'une coupe franche se déplace sur elle ; un changement de cadrage à **0,2 s** ou moins d'une coupe franche tombe dessus (un seul changement, jamais deux à quelques images) ; un changement déplacé sur le début d'un insert se place **2 images** dessous (pile dessus, une image du nouveau cadrage apparaîtrait d'abord).
  - Vérifie sur le fichier rendu, image par image, pas sur le plan.

> **Sans visage** : pas de punch-in sur un visage. Le rythme vient d'une lente poussée sur la capture (mêmes chiffres : 1,5 %/s, +10 % max), de zooms de 1,5 à 2,2x sur l'élément nommé (ligne 1 de la table), et du texte cinétique. Les règles « autour des inserts » s'appliquent aux zooms de capture de la même façon.

## 11. Les sous-titres (si le créateur en veut)

Demande-lui s'il veut des sous-titres incrustés. Si oui :

**Style par défaut** :
- Casse de phrase, **3 mots maximum** à l'écran, centré en bas. Police : la police de titre de `branding.json`, dans sa graisse la plus lourde (chargée vraiment, voir section 2).
- **Rien derrière les mots** : un fin contour foncé (épaisseur **0,035** de la taille de police) et une ombre douce (flou **0,16** de la taille). Seule exception : quand le fond est lui-même du TEXTE dense (un écran filmé), une plaque arrondie translucide `rgba(11,11,13,0.45)` derrière la ligne, palette sombre forcée.
- **1 à 3 mots par ligne, jamais 4** : coupe d'abord aux pauses (plus de **0,28 s**) et aux fins de phrase, puis en groupes équilibrés (4 mots = 2+2, jamais 3+1). Au plus **32** caractères en horizontal (**21** en vertical).
- Garde `. ! ? …` sur le dernier mot d'une vraie phrase (et passe à la ligne) ; retire `, ; : " » «` ; garde les apostrophes ; supprime un jeton qui n'est que de la ponctuation (Whisper sort les guillemets français comme des mots).
- **Karaoké** : exactement UN mot allumé (le dernier dont le temps est passé), en couleur d'accent ; les autres en couleur de base, sans assombrissement ; une petite pulsation de 12 images (1 → 1,04 → 1) quand un mot s'allume.
- Taille **64** px, à **9 %** du bas, largeur max **86 %** (sur 1920x1080).
- **Espace entre mots = 0,45** de la taille de police, vérifié sur la ligne la PLUS LARGE : l'espace entre deux mots doit être nettement plus grand que l'espace entre lettres.
- Contour propre : chaque mot en deux couches superposées (dessous le contour seul avec l'ombre, dessus le remplissage), car un `text-stroke` centré mange les lettres.

**Couleurs selon le fond** : mesure la luminance de la bande des sous-titres une fois par seconde (`ffmpeg ... crop=<la bande>,scale=32:16,signalstats`, YAVG normalisé = (YAVG-16)/219). Fond sombre : texte blanc, mot allumé en accent (défaut `#FEDF00`) ; fond clair : texte `#121212`, mot allumé en accent foncé (défaut `#A86A00`), lueur blanche au lieu de l'ombre noire. Hystérésis : 2 mesures d'affilée, entrée **0,66**, sortie **0,56** ; l'état de départ vient de la PREMIÈRE mesure (pas de « sombre » par défaut). La bande mesurée suit exactement la place des sous-titres. Un écran filmé au téléphone mesure 0,60 à 0,72 : regarde la répartition des mesures et règle entrée juste sous le minimum clair, sortie juste sous le maximum sombre.

**Jamais sur un visage, jamais au milieu d'un écran partagé** : place la ligne dans une bande libre (dessous, à droite, à gauche), décale-la à côté d'une incrustation caméra ou d'un obstacle (logo, bulle).

**Contrôles** :
1. Avant : regarde 6 images de la vidéo (orientation, zones chargées, obstacles).
2. Avant le rendu complet : rends seule l'image de la ligne LA PLUS LARGE et vérifie qu'elle dégage les obstacles.
3. Après le rendu : une planche contact avec une image au MILIEU de chaque ligne de sous-titre, tirée du fichier rendu. Lis chaque vignette : une ligne illisible en vignette de 420 px l'est aussi sur un téléphone. Lis les pixels en pleine résolution, une vignette réduite trompe sur les couleurs.

**Correction de la transcription (obligatoire)** : avant de générer les sous-titres, corrige les noms de marques et d'outils mal entendus, la grammaire, en gardant les mots dans le même ordre (1 pour 1, les horodatages restent) ; mets entre « » ce que quelqu'un cite ; écris les nombres en chiffres. Garde dans le projet un fichier de corrections récurrentes (mot entendu → bon mot) appliqué à chaque vidéo de la chaîne.

## 12. Rendu final et livraison

- **Le rendu final est cadré exactement comme les aperçus validés** (un seul plan de zooms pour tout le film), avec des inserts en 4K natif si la source est 4K, en **60 fps**, jamais sous la cadence de la prise. Refuse un insert sans rendu 4K plus récent que son rendu 1080p. Compte ~6 s de rendu par seconde d'insert 4K 60 fps.
- **Qualité d'abord** : livre à la résolution et au débit de la source, jamais en dessous (débit de la source x1,4, entre 8 et 100 Mb/s ; ~80 Mb/s pour du 4K 60). Ne fais pas passer la vidéo caméra par un moteur qui capture chaque image en JPEG : fais dessiner aux outils de motion seulement les calques (inserts, textes, sous-titres sur fond transparent) et laisse ffmpeg zoomer, composer et encoder la source.
- **Un long film 4K se rend en segments** : coupe dans les trous entre inserts, au plus **18** inserts par segment, vérifie le nombre exact d'images de chaque segment, concatène la vidéo seule, puis ajoute l'audio mixé à la fin (concaténer avec l'audio en une étape a décalé la vidéo de 21 ms).
- **Vérifications avant de livrer** : `ffprobe` (largeur, hauteur, cadence, débit) contre la source ; nombre d'images décodées (`ffprobe -count_frames`), pas seulement la durée annoncée ; la planche contact des textes derrière la tête et des sous-titres ; le contrôle de mouvement (fps, images immobiles, tremblement) ; le mix (section 8) ; l'appel à l'action avant 25 %.
- Livre le fichier final au créateur avec la liste des chapitres (temps de la coupe finale) pour sa description.

## 13. Les points de contrôle avec le créateur, et ses règles

Tu montres et tu attends son « go » à chaque étape :

1. Le branding (section 2).
2. La liste des répétitions et des coupes de l'accroche (section 3.7).
3. Le plan des inserts par type (section 7.1).
4. L'accroche montée (section 7.2).
5. Le premier morceau (section 7.3), puis tous les autres ensemble.
6. Le rendu final.

**Chaque remarque devient une règle.** Dans le même tour où il la fait, écris-la dans la section « Règles de cette chaîne » de `regles-chaine.md` (dans le projet) : la règle générale (quoi, pourquoi vu par le spectateur, comment la vérifier), pas l'anecdote. Si elle contredit ce guide pour sa chaîne, sa règle gagne sur sa chaîne. Relis ce fichier au début de chaque session et avant chaque fiche d'éléments ; ne refais jamais une erreur qui y figure.

## 14. Répondre aux questions du créateur

- Explique n'importe quelle étape en mots simples, à partir de ce guide, dans sa langue : ce que tu fais, pourquoi (ce que le spectateur verrait sinon), et ce que ça lui demande.
- Si le guide ne couvre pas sa question, dis-le clairement, puis propose ce qui te paraît raisonnable en précisant que c'est ton avis et pas la méthode.
- Ne promets jamais un résultat (vues, rétention, abonnés, revenus) : la méthode améliore le montage, elle ne garantit rien.
