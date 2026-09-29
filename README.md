# Le miel et les abeilles

Résolution du problème du voyageur de commerce par algorithme génétique.
Une colonie de 100 abeilles cherche le trajet le plus court reliant la ruche
à 50 fleurs, puis revenant à la ruche.

Projet Bachelor 2 Data & IA — La Plateforme_

## Lancer

```bash
uv sync
uv run python main.py
```

Le programme affiche la progression toutes les 10 générations et écrit trois
figures dans `figures/`.

## Structure

| Fichier | Rôle |
|---|---|
| `config.py` | Tous les paramètres, au même endroit |
| `bee.py` | La classe `Bee` : un ordre de visite, sa longueur, ses parents |
| `beehive.py` | Le champ, la matrice de distances, la colonie et les opérateurs |
| `plots.py` | Les trois figures |
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
dans les deux cas. D'où l'intérêt de mesurer plutôt que de raisonner.

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

Les fleurs à l'intérieur du segment inversé gardent les mêmes voisines, elles
sont simplement parcourues à l'envers ; la matrice étant symétrique, ces
distances-là ne changent pas.

### Une sélection par tournoi de 3

Marier systématiquement les meilleures ferait converger toute la population
vers deux ancêtres en quelques générations. Le tournoi tire trois abeilles au
hasard et garde la meilleure : il favorise les bonnes sans exclure les
autres.

### De l'élitisme

Les 10 meilleures passent à la génération suivante sans modification, ce qui
garantit que la meilleure distance ne remonte jamais d'une génération à
l'autre.

## Résultats

Avec `seed=0`, 100 abeilles, 100 générations :

| | Génération 0 | Génération 100 |
|---|---|---|
| Moyenne de la colonie | 25 049 | 8 570 |
| Meilleure abeille | 21 637 | 8 160 |

Une réduction de 66 % de la distance moyenne, en moins d'une seconde.

![Convergence](figures/convergence.png)

![Meilleur trajet](figures/tour.png)

## Comparaisons

### Opérateur de mutation

| Mutation | Moyenne gén. 100 | Meilleure |
|---|---|---|
| Inversion de segment (2-opt) | **8 570** | **8 160** |
| Échange de deux fleurs | 10 288 | 9 839 |

16,7 % de mieux sur la moyenne, 17,1 % sur la meilleure. La forme des courbes
diffère aussi : avec l'échange, la convergence s'aplatit dès la 60ᵉ
génération ; avec l'inversion, elle progresse encore à la 100ᵉ.

### Remplacement générationnel ou steady-state

Une erreur d'indentation a produit accidentellement une variante où la
population est remplacée à chaque naissance, les nouveau-nées devenant
immédiatement parents potentiels. Elle converge **mieux** : 6 745 contre
8 160 pour la version générationnelle demandée par le sujet. Piste à creuser
plutôt qu'anomalie à corriger.

## Limites

Le meilleur trajet trouvé se croise lui-même en plusieurs endroits, visible
sur la figure ci-dessus. Or deux segments qui se croisent peuvent toujours
être remplacés par deux segments plus courts. 8 160 n'est donc pas l'optimum,
et la preuve est géométrique, pas statistique.

## À faire

- Étude des paramètres : taille du tournoi, taux de mutation, nombre d'élites
- Passage à l'échelle sur 250 et 1 000 fleurs
- Veille sur d'autres approches heuristiques