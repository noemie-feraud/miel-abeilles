# Le miel et les abeilles

Résolution du problème du voyageur de commerce par algorithme génétique.
Une colonie de 100 abeilles cherche le trajet le plus court reliant la ruche
à 50 fleurs, puis revenant à la ruche.

Projet Bachelor 2 Data & IA — La Plateforme_

## Lancer

```bash
uv sync
uv run python main.py     # une simulation + les trois figures
uv run python study.py    # l'étude des paramètres (environ 1 min 30)
```

## Structure

| Fichier | Rôle |
|---|---|
| `config.py` | Tous les paramètres, au même endroit |
| `bee.py` | La classe `Bee` : un ordre de visite, sa longueur, ses parents |
| `beehive.py` | Le champ, la matrice de distances, la colonie et les opérateurs |
| `plots.py` | Les trois figures |
| `study.py` | L'étude des paramètres |
| `main.py` | Point d'entrée |

## Le champ

![Le champ de fleurs](figures/field.png)

## Choix d'implémentation

### Des indices, pas des coordonnées

J'ai choisi de manipuler des indices plutôt que des coordonnées parce qu'un
indice permet de lire directement dans une matrice de distances calculée une
seule fois au départ. Je ne recalcule donc jamais une distance : je la lis.

La matrice fait 51 × 51 (la ruche plus les 50 fleurs) et coûte 2 601 racines
carrées, une fois pour toutes. L'approche par coordonnées en refait 51 par
abeille et par évaluation.

Mesuré sur 9 000 évaluations, résultats identiques des deux côtés :

| Méthode | Temps |
|---|---|
| Coordonnées, une racine par segment | 0,462 s |
| Matrice pré-calculée | 0,086 s |

Soit **5,4 fois plus rapide**. L'écart est plus faible que le rapport du
nombre de racines carrées le laisserait croire, parce que le coût ne vient
pas uniquement des racines : la boucle Python et les accès mémoire pèsent
dans les deux cas.

### Un croisement qui préserve la permutation

Le croisement naïf — début de la mère, fin du père — produisait des trajets
qui visitaient deux fois la même fleur et en oubliaient d'autres : 36 fleurs
distinctes sur 50. Le danger n'est pas le plantage, c'est l'absence de
plantage — `path_length` calculait une distance parfaitement crédible pour un
trajet impossible, et rien à l'écran ne l'aurait signalé.

La version retenue garde le début de la mère, puis complète avec les fleurs
manquantes dans l'ordre où le père les visite. Vérifiée sur 2 040 croisements
couvrant toutes les positions de coupe : le résultat est toujours une
permutation valide des 50 fleurs.

### Une mutation par inversion de segment (2-opt)

Inverser un segment ne modifie que deux liaisons du trajet, là où échanger
deux fleurs en modifie quatre. La mutation conserve donc davantage de ce que
l'abeille avait déjà de bon, et a plus de chances de l'améliorer légèrement
plutôt que de le détruire.

### Sélection par tournoi et élitisme

Le tournoi tire plusieurs abeilles au hasard et garde la meilleure : il
favorise les bonnes sans exclure les autres. Les 10 meilleures passent à la
génération suivante sans modification, ce qui garantit que la meilleure
distance ne remonte jamais.

## Étude des paramètres

Chaque réglage est testé sur 5 graines aléatoires différentes. On compare la
moyenne des résultats, mais aussi leur **écart-type** : si deux réglages
diffèrent moins que la dispersion de leurs propres mesures, on ne peut pas
conclure qu'ils diffèrent.

### Un paramètre à la fois

Les autres paramètres restent à leur valeur initiale (tournoi 3, mutation 0,3,
10 élites).

**Taille du tournoi**

| Taille | Meilleure (moyenne) | Écart-type |
|---|---|---|
| 2 | 9 409 | 383 |
| 3 | 8 330 | 284 |
| 5 | 7 466 | 281 |
| 10 | 7 259 | 146 |
| 20 | 7 428 | 432 |

Un tournoi de 2 ne trie presque pas. L'optimum est vers 10.

**Taux de mutation**

| Taux | Meilleure (moyenne) | Écart-type |
|---|---|---|
| 0,0 | 16 724 | 541 |
| 0,1 | 9 218 | 199 |
| 0,3 | 8 330 | 284 |
| 0,5 | 8 204 | 446 |
| 0,8 | 8 834 | 437 |
| 1,0 | 9 464 | 335 |

Sans mutation, le résultat est deux fois pire : les enfants ne font que
recombiner ce qui existe déjà, la population se fige. À l'inverse, muter tout
le monde détruit à chaque génération ce que la sélection vient de trouver.

**Nombre d'élites**

| Élites | Meilleure (moyenne) | Écart-type |
|---|---|---|
| 0 | 8 350 | 143 |
| 1 | 8 423 | 536 |
| 5 | 8 257 | 370 |
| 10 | 8 330 | 284 |
| 25 | 8 394 | 369 |
| 50 | 9 424 | 820 |

Entre 0 et 25, les écarts sont plus petits que les écarts-types : **aucun effet
mesurable**. Seul 50 dégrade nettement — la moitié de la population ne change
plus, il reste moitié moins de place pour les enfants.

### Combinaisons

Tester un paramètre à la fois ne suffit pas : deux paramètres peuvent
interagir. Mesuré sur 12 graines :

| Tournoi | Mutation | Meilleure (moyenne) | Écart-type |
|---|---|---|---|
| 3 | 0,3 | 8 092 | 423 |
| 10 | 0,5 | 7 081 | 155 |
| **20** | **0,7** | **6 750** | 276 |
| 50 | 0,9 | 6 543 | 173 |
| 100 | 0,9 | 6 462 | 141 |

Mesuré seul, un tournoi de 20 était moins bon qu'un tournoi de 10. Combiné à
une mutation plus forte, il devient meilleur : une sélection plus dure paie
quand la mutation fournit assez de diversité pour la nourrir.

### Pourquoi ne pas prendre le meilleur chiffre

Avec un tournoi de 100 sur une population de 100, le tournoi retient toujours
la même abeille : la meilleure. La mère et le père sont donc identiques, et
croiser une abeille avec elle-même la redonne exactement (vérifié sur 200
permutations × 51 positions de coupe). **Le croisement ne fait plus rien** :
chaque enfant est un clone muté de la meilleure abeille.

Ce n'est plus un algorithme génétique mais une recherche locale. Qu'elle soit
la plus performante montre que sur ce problème, à cette taille, **l'essentiel
du travail est fait par la mutation 2-opt, pas par le croisement**.

### Réglage retenu

**Tournoi 20, mutation 0,7, 10 élites.** C'est le meilleur réglage qui reste un
vrai algorithme génétique — les parents sont distincts, le croisement opère.

## Résultats

Avec le réglage retenu, `seed=0`, 100 abeilles, 100 générations :

| | Génération 0 | Génération 100 |
|---|---|---|
| Moyenne de la colonie | 25 049 | 7 210 |
| Meilleure abeille | 21 637 | 6 788 |

Une réduction de 71 % de la distance moyenne, en moins d'une seconde. Le
réglage initial (tournoi 3, mutation 0,3) donnait 8 160.

![Convergence](figures/convergence.png)

![Meilleur trajet](figures/tour.png)

## Autres comparaisons

Mesurées avec le réglage initial (tournoi 3, mutation 0,3).

### Opérateur de mutation

| Mutation | Moyenne gén. 100 | Meilleure |
|---|---|---|
| Inversion de segment (2-opt) | **8 570** | **8 160** |
| Échange de deux fleurs | 10 288 | 9 839 |

16,7 % de mieux sur la moyenne, 17,1 % sur la meilleure.

### Remplacement générationnel ou steady-state

Une erreur d'indentation a produit accidentellement une variante où la
population est remplacée à chaque naissance, les nouveau-nées devenant
immédiatement parents potentiels. Elle converge mieux : 6 745 contre 8 160
pour la version générationnelle demandée par le sujet.

## Limites

Le meilleur trajet trouvé se croise encore **une fois** (compté par calcul
sur les 51 segments). Or deux segments qui se croisent peuvent toujours être
remplacés par deux segments plus courts : ce seul croisement prouve que
6 788 n'est pas l'optimum. Le réglage initial, à 8 160, en laissait plusieurs.

## À faire

- Passage à l'échelle sur 250 et 1 000 fleurs
- Veille sur d'autres approches heuristiques