#Exemple de fichier à utiliser en input : FL_BON_OUTPUT.tsv

import sys
sys.path.append('../../../')
from fonctions import input_utilisateur, parcours_fichier, output_matrice, heatmap_output
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

#création d'une matrice de similarité cosinus avec des vecteurs contextuels de FlauBERT puis une Heatmap (groupes de 20 exemples)

#entree_utilisateur=le fichier tapé en input,output_utilisateur=le fichier output tapé en input,reponse=réponse à la question : True(oui)/False(non)
entree_utilisateur,output_utilisateur,reponse=input_utilisateur(True,True)#1er True=fichier tsv vers tsv. 2ème True= on veut que la question soit posée à l'utilisateur

#tant que l'utilisateur n'aura pas répondu correctement à la question elle sera reposée
while reponse == None:
	entree_utilisateur,output_utilisateur,reponse=input_utilisateur(True,True)

#nom_vecteur et liste_tensor=variables utilisées pour faire la matrice de similarité
nom_vecteur,liste_tensor = parcours_fichier(entree_utilisateur,reponse,True,False,False)#True=similarité(et pas dendrogramme); 1er False=vecteur contextuel; 2ème False=groupes de 20 exemples(variable onze_ex sur False)

#création de la matrice de similarité dans le 1er fichier output
output_matrice(output_utilisateur,nom_vecteur,liste_tensor)

#commenter la suite du script si l'on ne veut pas créer de heatmap.
#fichier_out_heatmap,labels_heatmap,nom_de_label_fic_split_heatmap= utilisés pour les paramètres de la figure
fichier_out_heatmap,labels_heatmap,nom_de_label,fic_split_heatmap=heatmap_output(output_utilisateur,False,False,False,False,reponse)#1er False=une valeur affichée tous les 10 (écart de 10),2eme False=Heatmap,3ème False=contextuel,4ème False=onze_ex sur False

#paramètres à modifier selon la taille du fichier (change la taille de la police)
plt.title(fic_split_heatmap,size=5)#titre de la figure
plt.xticks(np.arange(len(nom_de_label),step=10),labels=labels_heatmap,fontsize=4)
plt.yticks(np.arange(len(nom_de_label),step=10),labels=labels_heatmap,fontsize=4)
plt.savefig(fichier_out_heatmap,bbox_inches='tight',dpi=500)


#paramètres utilisés:

#FL_BON et FL_MAGN :
#xticks et ysticks fontsize = 4
#dpi=500

#FL_MAGN_BON_CLASSE :
#xticks et ysticks fontsize = 3
#dpi=500

#SILENCE_VS_SOLEIL_PLOMB, SOLEIL_PLOMB_VS_COLERE_SAINE et SOLEIL_PLOMB_VS_DEGOUT_PROFOND:
#xticks et ysticks fontsize = 5
#dpi=500
