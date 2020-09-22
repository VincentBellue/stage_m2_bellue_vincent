#Exemple de fichier à utiliser en input : FL_BON_OUTPUT_VEC_STATIQUE.tsv

import sys
sys.path.append('../../')
from fonctions import input_utilisateur, parcours_fichier, output_matrice, heatmap_output
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

#création d'une matrice de similarité cosinus avec des vecteurs statiques de FastText puis une heatmap avec Seaborn

#entree_utilisateur=le fichier tapé en input,output_utilisateur=le fichier output tapé en input,reponse=réponse à la question : True(oui)/False(non)
entree_utilisateur,output_utilisateur,reponse=input_utilisateur(True,False)#1er True=fichier tsv vers tsv. False= on ne veut pas que la question soit posée car il s'agira forcément du calcul de la base-collocatif

#nom_vecteur et liste_tensor=variables utilisées pour faire la matrice de similarité
nom_vecteur,liste_tensor = parcours_fichier(entree_utilisateur,reponse,True,True,False)#True=similarité(et pas dendrogramme);2ème True=vecteur statique; False=groupes de 11 sur False

#par défaut pour un vecteur statique on laisse onze_ex sur False car ça ne sert à rien de faire des groupes étant donné que chaque couple base-colloc n'est ajouté qu'une fois
#création de la matrice de similarité dans le 1er fichier output
output_matrice(output_utilisateur,nom_vecteur,liste_tensor)

#commenter la suite du script si l'on ne veut pas créer de heatmap.
#fichier_out_heatmap,labels_heatmap,nom_de_label_fic_split_heatmap= utilisés pour les paramètres de la figure
fichier_out_heatmap,labels_heatmap,nom_de_label,fic_split_heatmap=heatmap_output(output_utilisateur,True,False,True,False,reponse)#1er True=toutes les valeurs affichées (écart de 1),1er False=Heatmap,2ème True=statique,2ème False=onze_ex sur False

#paramètres à modifier selon la taille du fichier (change la taille de la police).
plt.title(fic_split_heatmap,size=5)#titre de la figure
plt.xticks(np.arange(len(nom_de_label),step=1),labels=labels_heatmap,fontsize=4)
plt.yticks(np.arange(len(nom_de_label),step=1),labels=labels_heatmap,fontsize=4)
plt.savefig(fichier_out_heatmap,bbox_inches='tight',dpi=500)

#paramètres utilisés:

#FL_BON et FL_MAGN :
#xticks et ysticks fontsize = 2.2
#dpi=500

#FL_MAGN_BON_CLASSE :
#xticks et ysticks fontsize = 1.2
#dpi=600

#SILENCE_VS_SOLEIL_PLOMB, SOLEIL_PLOMB_VS_COLERE_SAINE et SOLEIL_PLOMB_VS_DEGOUT_PROFOND:
#xticks et ysticks fontsize = 4
#dpi=500
