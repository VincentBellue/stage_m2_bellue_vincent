# Fichiers .tsv

|Vecteurs  |Script                                                                                                                               |Dossier input                                    |Dossier output                                                       |
|----------| ------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|---------------------------------------------------------------------|
|FlauBERT  |[Vecteur base et collocatif](scripts/vecteur_base_collocatif/flaubert/script_vecteur_base_collocatif.py)                             |[input](inputs)                                  |[output](outputs/vecteurs_base_collocatif/flaubert)                   |
|          |[Matrice de similarité et heatmap (groupes de 20)](scripts/matrice_heatmap/flaubert/vingt_ex/matrice_et_heatmap_flaubert_vingt_ex.py)|[input](outputs/vecteurs_base_collocatif/flaubert)|[output](outputs/matrice_similarite/flaubert/vingt_exemples)|
|          |[Matrice de similarité et heatmap (groupes de 11)](scripts/matrice_heatmap/flaubert/onze_ex/matrice_et_heatmap_flaubert_onze_ex.py)  |[input](outputs/vecteurs_base_collocatif/flaubert)|[output](outputs/matrice_similarite/flaubert/onze_exemples) |
|FastText  |[Vecteur base et collocatif](scripts/vecteur_base_collocatif/fasttext/script_base_colloc_vec_statique.py)                            |[input](inputs)                                  |[output](outputs/vecteurs_base_collocatif/fasttext)                  |
|          |[Matrice de similarité](scripts/matrice_heatmap/fasttext/matrice_et_heatmap_fasttext.py)                                             |[input](outputs/vecteurs_base_collocatif/fasttext)|[output](outputs/vecteurs_base_collocatif/fasttext)|                       |
|**Divers**|                                                                                                                                     |                                                 |                                                                     |
|Compteur  |[Compteur d'occurrences FL BON+MAGN](scripts/compteur_occurrences/compteur_base_genre_compositionnel.py)                             |[input](inputs)                                  |[output](outputs/compteur_occurrences)|

# Entrainement et test d'un réseau de neurones à une couche cachée :new:
* FL Bon
  * FlauBERT
    * Base et collocatif
      * Résultats détaillés
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/details/FL_BON_OUTPUT_BASE_COLLOC_CONSOLE.tsv)
      * Résultats synthétiques
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_BON_OUTPUT_BASE_COLLOC_ACCURACY.tsv)
    * Collocatif seul
      * Résultats détaillés
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/details/FL_BON_OUTPUT_COLLOC_SEUL_CONSOLE.txt)
      * Résultats synthétiques
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_BON_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)
  * FlauBERT et FastText (concaténation base et collocatif)
    * Résultats synthétique
      * [Comparaison du modèle FlauBERT à FastText](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_BON_OUTPUT_COMPARAISON_CONCAT.tsv) 

* FL Magn
  * FlauBERT
    * Base et collocatif
      * Résultats détaillés
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/details/FL_MAGN_OUTPUT_BASE_COLLOC_CONSOLE.tsv)
      * Résultats synthétiques
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_MAGN_OUTPUT_BASE_COLLOC_ACCURACY.tsv)
    * Collocatif seul
      * Résultats détaillés
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/details/FL_MAGN_OUTPUT_COLLOC_SEUL_CONSOLE.txt)
      * Résultats synthétiques
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_MAGN_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)
  * FlauBERT et FastText (concaténation base et collocatif)
    * Résultats synthétique
      * [Comparaison du modèle FlauBERT à FastText](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_MAGN_OUTPUT_COMPARAISON_CONCAT.tsv) 

* FL Magn et Bon
  * FlauBERT
    * Base et collocatif
      * Résultats détaillés
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/details/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_CONSOLE.tsv)
      * Résultats synthétiques
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_ACCURACY.tsv)
    * Collocatif seul
      * Résultats détaillés
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/details/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_CONSOLE.txt)
      * Résultats synthétiques
        * [Comparaison modèle entrainé sur FlauBERT à un modèle baseline](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)
  * FlauBERT et FastText (concaténation base et collocatif)
    * Résultats synthétique
      * [Comparaison du modèle FlauBERT à FastText](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_MAGN_BON_CLASSE_OUTPUT_COMPARAISON_CONCAT.tsv)
---
# Résultats accuracy du réseau de neurones
### Comparaison accuracy FlauBERT et baseline basée sur le genre de la base
| Base-collocatif    |                                                                                                                                 |                                                                                                                               |                                                                                                                                           |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
|                    |                                                          Bon                                                                    |                                           Magn                                                                                |                                                Bon+Magn                                                                                   |
|FlauBERT            |   [62.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_BON_OUTPUT_BASE_COLLOC_ACCURACY.tsv)|[78.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_MAGN_OUTPUT_BASE_COLLOC_ACCURACY.tsv)| [72.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_ACCURACY.tsv)|
|Baseline            |   [56.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_BON_OUTPUT_BASE_COLLOC_ACCURACY.tsv)|[62.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_MAGN_OUTPUT_BASE_COLLOC_ACCURACY.tsv)| [59.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/base_collocatif/synthese/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_ACCURACY.tsv)|
|**Collocatif seul** |                                                                                                                                 |           |           |
|FlauBERT            |   [66.5%](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_BON_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)|[85.5%](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_MAGN_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)| [83.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)|
|Baseline            |   [56.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_BON_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)|[62.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_MAGN_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)| [59.0%](outputs/reseau_neurones/comparaison_flaubert_baseline/collocatif_seul/synthese/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_ACCURACY.tsv)|

### Comparaison accuracy FlauBERT et FastText (concaténation du vecteur de la base à celui du collocatif)
| Concaténation|                                                                                                                        |                                                                                                                       |                                                                                                                                  |
|------------- |------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
|              | Bon                                                                                                                    |                                                      Magn                                                             |                                                        Bon+Magn                                                                  |
|FlauBERT      |   [61.5%](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_BON_OUTPUT_COMPARAISON_CONCAT.tsv)|[86.0%](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_MAGN_OUTPUT_COMPARAISON_CONCAT.tsv) |[82.75%](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_MAGN_BON_CLASSE_OUTPUT_COMPARAISON_CONCAT.tsv)|
|FastText      |   [58.5%](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_BON_OUTPUT_COMPARAISON_CONCAT.tsv)|[82.5%](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_MAGN_OUTPUT_COMPARAISON_CONCAT.tsv) |[72.5%](outputs/reseau_neurones/comparaison_flaubert_fasttext/vecteur_concatene/FL_MAGN_BON_CLASSE_OUTPUT_COMPARAISON_CONCAT.tsv) |
---

# Résultats heatmap et dendrogramme (figures)
* Comparaison Bon
  * FlauBERT
    * Heatmap
      * Base et collocatif
        * [Matrice 200x200](figures/FL_BON/flaubert/heatmap/base_collocatif/vingt_exemples/FL_BON_OUTPUT_BASE_COLLOC_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 110x110](figures/FL_BON/flaubert/heatmap/base_collocatif/onze_exemples/FL_BON_OUTPUT_BASE_COLLOC_ONZE_EX_COS_HEATMAP.png)
      * Collocatif seulement
        * [Matrice 200x200](figures/FL_BON/flaubert/heatmap/collocatif_seul/vingt_exemples/FL_BON_OUTPUT_COLLOC_SEUL_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 110x110](figures/FL_BON/flaubert/heatmap/collocatif_seul/onze_exemples/FL_BON_OUTPUT_COLLOC_SEUL_ONZE_EX_COS_HEATMAP.png)
    * Dendrogramme
      * Base et collocatif
        * [Classification ascendante hiérarchique (200 exemples)](figures/FL_BON/flaubert/dendrogramme/base_collocatif/vingt_exemples/FL_BON_OUTPUT_BASE_COLLOC_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (110 exemples)](figures/FL_BON/flaubert/dendrogramme/base_collocatif/onze_exemples/FL_BON_OUTPUT_BASE_COLLOC_ONZE_EX_DENDROGRAMME.png)
      * Collocatif seulement
        * [Classification ascendante hiérarchique (200 exemples)](figures/FL_BON/flaubert/dendrogramme/collocatif_seul/vingt_exemples/FL_BON_OUTPUT_COLLOC_SEUL_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (110 exemples)](figures/FL_BON/flaubert/dendrogramme/collocatif_seul/onze_exemples/FL_BON_OUTPUT_COLLOC_SEUL_ONZE_EX_DENDROGRAMME.png)
  * FastText
    * Heatmap
      * [Matrice 115x115](figures/FL_BON/fasttext/heatmap/FL_BON_OUTPUT_VEC_STATIQUE_COS_HEATMAP.png)
    * Dendrogramme
      * [Classification ascendante hiérarchique (115 exemples)](figures/FL_BON/fasttext/dendrogramme/FL_BON_OUTPUT_VEC_STATIQUE_DENDROGRAMME.png)
---
* Comparaison Magn
  * FlauBERT
    * Heatmap
      * Base et collocatif
        * [Matrice 200x200](figures/FL_MAGN/flaubert/heatmap/base_collocatif/vingt_exemples/FL_MAGN_OUTPUT_BASE_COLLOC_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 110x110](figures/FL_MAGN/flaubert/heatmap/base_collocatif/onze_exemples/FL_MAGN_OUTPUT_BASE_COLLOC_ONZE_EX_COS_HEATMAP.png)
      * Collocatif seulement
        * [Matrice 200x200](figures/FL_MAGN/flaubert/heatmap/collocatif_seul/vingt_exemples/FL_MAGN_OUTPUT_COLLOC_SEUL_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 110x110](figures/FL_MAGN/flaubert/heatmap/collocatif_seul/onze_exemples/FL_MAGN_OUTPUT_COLLOC_SEUL_ONZE_EX_COS_HEATMAP.png)
    * Dendrogramme
      * Base et collocatif
        * [Classification ascendante hiérarchique (200 exemples)](figures/FL_MAGN/flaubert/dendrogramme/base_collocatif/vingt_exemples/FL_MAGN_OUTPUT_BASE_COLLOC_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (110 exemples)](figures/FL_MAGN/flaubert/dendrogramme/base_collocatif/onze_exemples/FL_MAGN_OUTPUT_BASE_COLLOC_ONZE_EX_DENDROGRAMME.png)
      * Collocatif seulement
        * [Classification ascendante hiérarchique (200 exemples)](figures/FL_MAGN/flaubert/dendrogramme/collocatif_seul/vingt_exemples/FL_MAGN_OUTPUT_COLLOC_SEUL_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (110 exemples)](figures/FL_MAGN/flaubert/dendrogramme/collocatif_seul/onze_exemples/FL_MAGN_OUTPUT_COLLOC_SEUL_ONZE_EX_DENDROGRAMME.png)
  * FastText
    * Heatmap
      * [Matrice 116x116](figures/FL_MAGN/fasttext/heatmap/FL_MAGN_OUTPUT_VEC_STATIQUE_COS_HEATMAP.png)
    * Dendrogramme
      * [Classification ascendante hiérarchique (116 exemples)](figures/FL_MAGN/fasttext/dendrogramme/FL_MAGN_OUTPUT_VEC_STATIQUE_DENDROGRAMME.png)
---
* Comparaison Magn et Bon
  * FlauBERT
    * Heatmap
      * Base et collocatif
        * [Matrice 400x400](figures/FL_MAGN_BON_CLASSE/flaubert/heatmap/base_collocatif/vingt_exemples/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 220x220](figures/FL_MAGN_BON_CLASSE/flaubert/heatmap/base_collocatif/onze_exemples/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_ONZE_EX_COS_HEATMAP.png)
      * Collocatif seulement
        * [Matrice 400x400](figures/FL_MAGN_BON_CLASSE/flaubert/heatmap/collocatif_seul/vingt_exemples/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 220x220](figures/FL_MAGN_BON_CLASSE/flaubert/heatmap/collocatif_seul/onze_exemples/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_ONZE_EX_COS_HEATMAP.png)
    * Dendrogramme
      * Base et collocatif
        * [Classification ascendante hiérarchique (400 exemples)](figures/FL_MAGN_BON_CLASSE/flaubert/dendrogramme/base_collocatif/vingt_exemples/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_VINGT_EX_DENDROGRAMME.pdf)
        * [Classification ascendante hiérarchique (220 exemples)](figures/FL_MAGN_BON_CLASSE/flaubert/dendrogramme/base_collocatif/onze_exemples/FL_MAGN_BON_CLASSE_OUTPUT_BASE_COLLOC_ONZE_EX_DENDROGRAMME.pdf)
      * Collocatif seulement
        * [Classification ascendante hiérarchique (400 exemples)](figures/FL_MAGN_BON_CLASSE/flaubert/dendrogramme/collocatif_seul/vingt_exemples/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_VINGT_EX_DENDROGRAMME.pdf)
        * [Classification ascendante hiérarchique (220 exemples)](figures/FL_MAGN_BON_CLASSE/flaubert/dendrogramme/collocatif_seul/onze_exemples/FL_MAGN_BON_CLASSE_OUTPUT_COLLOC_SEUL_ONZE_EX_DENDROGRAMME.pdf)
  * FastText
    * Heatmap
      * [Matrice 231x231](figures/FL_MAGN_BON_CLASSE/fasttext/heatmap/FL_MAGN_BON_CLASSE_OUTPUT_VEC_STATIQUE_COS_HEATMAP.png)
    * Dendrogramme
      * [Classification ascendante hiérarchique (231 exemples)](figures/FL_MAGN_BON_CLASSE/fasttext/dendrogramme/FL_MAGN_BON_CLASSE_OUTPUT_VEC_STATIQUE_DENDROGRAMME.pdf)
---
* Comparaison Silence de plomb et Soleil de plomb (Magn et Magn avec le même collocatif)
  * FlauBERT
    * Heatmap
      * Base et collocatif
        * [Matrice 40x40](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/heatmap/base_collocatif/vingt_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_BASE_COLLOC_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 22x22](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/heatmap/base_collocatif/onze_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_BASE_COLLOC_ONZE_EX_COS_HEATMAP.png)
      * Collocatif seulement
        * [Matrice 40x40](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/heatmap/collocatif_seul/vingt_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_COLLOC_SEUL_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 22x22](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/heatmap/collocatif_seul/onze_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_COLLOC_SEUL_ONZE_EX_COS_HEATMAP.png)
    * Dendrogramme
      * Base et collocatif
        * [Classification ascendante hiérarchique (40 exemples)](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/dendrogramme/base_collocatif/vingt_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_BASE_COLLOC_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (22 exemples)](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/dendrogramme/base_collocatif/onze_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_BASE_COLLOC_ONZE_EX_DENDROGRAMME.png)
      * Collocatif seulement
        * [Classification ascendante hiérarchique (40 exemples)](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/dendrogramme/collocatif_seul/vingt_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_COLLOC_SEUL_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (22 exemples)](figures/SILENCE_VS_SOLEIL_PLOMB/flaubert/dendrogramme/collocatif_seul/onze_exemples/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_COLLOC_SEUL_ONZE_EX_DENDROGRAMME.png)
  * FastText
    * Heatmap
      * [Matrice 22x22](figures/SILENCE_VS_SOLEIL_PLOMB/fasttext/heatmap/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_VEC_STATIQUE_COS_HEATMAP.png)
    * Dendrogramme
      * [Classification ascendante hiérarchique (22 exemples)](figures/SILENCE_VS_SOLEIL_PLOMB/fasttext/dendrogramme/SILENCE_VS_SOLEIL_PLOMB_OUTPUT_VEC_STATIQUE_DENDROGRAMME.png)
---
* Comparaison Soleil de plomb et Colère saine (Magn et Bon)
  * FlauBERT
    * Heatmap
      * Base et collocatif
        * [Matrice 40x40](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/heatmap/base_collocatif/vingt_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_BASE_COLLOC_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 22x22](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/heatmap/base_collocatif/onze_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_BASE_COLLOC_ONZE_EX_COS_HEATMAP.png)
      * Collocatif seulement
        * [Matrice 40x40](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/heatmap/collocatif_seul/vingt_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_COLLOC_SEUL_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 22x22](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/heatmap/collocatif_seul/onze_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_COLLOC_SEUL_ONZE_EX_COS_HEATMAP.png)
    * Dendrogramme
      * Base et collocatif
        * [Classification ascendante hiérarchique (40 exemples)](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/dendrogramme/base_collocatif/vingt_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_BASE_COLLOC_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (22 exemples)](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/dendrogramme/base_collocatif/onze_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_BASE_COLLOC_ONZE_EX_DENDROGRAMME.png)
      * Collocatif seulement
        * [Classification ascendante hiérarchique (40 exemples)](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/dendrogramme/collocatif_seul/vingt_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_COLLOC_SEUL_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (22 exemples)](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/flaubert/dendrogramme/collocatif_seul/onze_exemples/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_COLLOC_SEUL_ONZE_EX_DENDROGRAMME.png)
  * FastText
    * Heatmap
      * [Matrice 23x23](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/fasttext/heatmap/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_VEC_STATIQUE_COS_HEATMAP.png)
    * Dendrogramme
      * [Classification ascendante hiérarchique (23 exemples)](figures/SOLEIL_PLOMB_VS_COLERE_SAINE/fasttext/dendrogramme/SOLEIL_PLOMB_VS_COLERE_SAINE_OUTPUT_VEC_STATIQUE_DENDROGRAMME.png)
---
* Comparaison Soleil de plomb et Dégoût profond (Magn et Magn avec base et collocatif différents)
  * FlauBERT
    * Heatmap
      * Base et collocatif
        * [Matrice 40x40](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/heatmap/base_collocatif/vingt_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_BASE_COLLOC_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 22x22](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/heatmap/base_collocatif/onze_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_BASE_COLLOC_ONZE_EX_COS_HEATMAP.png)
      * Collocatif seulement
        * [Matrice 40x40](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/heatmap/collocatif_seul/vingt_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_COLLOC_SEUL_VINGT_EX_COS_HEATMAP.png)
        * [Matrice 22x22](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/heatmap/collocatif_seul/onze_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_COLLOC_SEUL_ONZE_EX_COS_HEATMAP.png)
    * Dendrogramme
      * Base et collocatif
        * [Classification ascendante hiérarchique (40 exemples)](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/dendrogramme/base_collocatif/vingt_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_BASE_COLLOC_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (22 exemples)](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/dendrogramme/base_collocatif/onze_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_BASE_COLLOC_ONZE_EX_DENDROGRAMME.png)
      * Collocatif seulement
        * [Classification ascendante hiérarchique (40 exemples)](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/dendrogramme/collocatif_seul/vingt_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_COLLOC_SEUL_VINGT_EX_DENDROGRAMME.png)
        * [Classification ascendante hiérarchique (22 exemples)](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/flaubert/dendrogramme/collocatif_seul/onze_exemples/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_COLLOC_SEUL_ONZE_EX_DENDROGRAMME.png)
  * FastText
    * Heatmap
      * [Matrice 22x22](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/fasttext/heatmap/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_VEC_STATIQUE_COS_HEATMAP.png)
    * Dendrogramme
      * [Classification ascendante hiérarchique (22 exemples)](figures/SOLEIL_PLOMB_VS_DEGOUT_PROFOND/fasttext/dendrogramme/SOLEIL_PLOMB_VS_DEGOUT_PROFOND_OUTPUT_VEC_STATIQUE_DENDROGRAMME.png)
