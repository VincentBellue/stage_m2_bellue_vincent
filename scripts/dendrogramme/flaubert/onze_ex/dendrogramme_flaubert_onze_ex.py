#Exemple de fichier à utiliser en input : FL_BON_OUTPUT.tsv
import sys
sys.path.append('../../../')
from fonctions import input_utilisateur, parcours_fichier, output_matrice, plot_dendrogram, dendrogramme_output
import matplotlib.pyplot as plt

#dendrogramme avec des vecteurs contextuels de FlauBERT

#entree_utilisateur=le fichier tapé en input,output_utilisateur=le fichier output tapé en input,reponse=réponse à la question : True(oui)/False(non)
entree_utilisateur,output_utilisateur,reponse=input_utilisateur(False,True)#False=fichier tsv vers png.True = on veut que la question soit posée afin de savoir si l'on veut base-colloc ou colloc seul

#tant que l'utilisateur ne répond pas correctement on repose la question
while reponse == None:
	entree_utilisateur,output_utilisateur,reponse=input_utilisateur(False,True)

#liste_nom_vecteur et liste_de_liste_vecteur=les deux variables à utiliser pour faire le dendrogramme
liste_nom_vecteur,liste_de_liste_vecteur = parcours_fichier(entree_utilisateur,reponse,False,False,True)#1er False=dendrogramme(et pas similarité);2ème False=vecteur contextuel;True=groupes de 11 exemples(variable onze_ex sur True)

#nom_fichier_out,labels_dendro,modele= utilisés pour les paramètres de la figure
nom_fichier_out,labels_dendro,modele=dendrogramme_output(liste_de_liste_vecteur,liste_nom_vecteur,reponse,False,True,entree_utilisateur,True)#False=vecteurs contextuels, 1er True=groupes de 11 exemples, 2ème True=on crée un dendrogramme

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
