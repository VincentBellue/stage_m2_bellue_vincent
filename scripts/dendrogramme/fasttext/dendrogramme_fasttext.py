#Exemple de fichier à utiliser en input : FL_BON_OUTPUT_VEC_STATIQUE.tsv
.tsv
import sys
sys.path.append('../../')
from fonctions import input_utilisateur, parcours_fichier, output_matrice, plot_dendrogram, dendrogramme_output
import matplotlib.pyplot as plt

#dendrogramme avec des vecteurs statiques de FastText

#entree_utilisateur=le fichier tapé en input,output_utilisateur=le fichier output tapé en input,reponse=réponse à la question : True(oui)/False(non)
entree_utilisateur,output_utilisateur,reponse=input_utilisateur(False,False)#1er False=fichier tsv vers png. 2ème False= on ne veut pas que la question soit posée car il s'agira forcément du calcul de la base-collocatif(car statique)

#liste_nom_vecteur et liste_de_liste_vecteur= les deux variables à utiliser pour faire le dendrogramme
liste_nom_vecteur,liste_de_liste_vecteur = parcours_fichier(entree_utilisateur,reponse,False,True,False)#1er False=dendrogramme(et pas similarité), True=vecteur statique, 2ème False=groupes de 20 exemples(variable onze_ex sur False car statique donc pas besoin de groupes de 20 ou 11)

#par défaut pour un vecteur statique on laisse onze_ex sur False car ça ne sert à rien de faire des groupes étant donné que chaque couple base-colloc n'est ajouté qu'une fois.
#nom_fichier_out,labels_dendro,modele= utilisés pour les paramètres de la figure
nom_fichier_out,labels_dendro,modele=dendrogramme_output(liste_de_liste_vecteur,liste_nom_vecteur,reponse,True,False,entree_utilisateur,True)#1er True=vecteurs statiques, False=groupes de 20 ex, 2ème True=on crée un dendrogramme

#paramètres de la figure./!\ valeurs de "linewidth", "leaf_font_size", "font_size" et "dpi" à modifier si problème avec la taille des différents éléments /!\.
plt.title(nom_fichier_out,fontsize=5)#titre de la figure + taille du titre
plt.rcParams['lines.linewidth'] = 1 # réduit la taille des traits du dendrogramme./!\ A modifier selon la taille du fichier en input/!\
plot_dendrogram(modele,truncate_mode=None,labels=labels_dendro,orientation='right',leaf_font_size=4)#orientation du dendrogramme(right=sur la droite), labels=le nom du vecteur(ex: Oui/soleil/plomb),leaf=1 : réduit la taille de la police pour la légende(1=minimum possible)
plt.savefig(output_utilisateur,dpi=300)#sauvegarde le dendrogramme dans le fichier_output, dpi=600 : meilleure qualité quand on zoom mais fichier plus gros.


#paramètres utilisés:

#FL_BON et FL_MAGN :
#linewidth=0.5
#leaf_font_size=2
#dpi=500

#FL_MAGN_BON_CLASSE :
#linewidth=0.2
#leaf_font_size=1
#dpi=600

#SILENCE_VS_SOLEIL_PLOMB, SOLEIL_PLOMB_VS_COLERE_SAINE et SOLEIL_PLOMB_VS_DEGOUT_PROFOND:
#linewidth=1
#leaf_font_size=4
#dpi=300

