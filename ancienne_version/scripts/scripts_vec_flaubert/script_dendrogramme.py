import argparse
import torch
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram

#fonction pour le dendrogramme
def plot_dendrogram(model, **kwargs):
	# Create linkage matrix and then plot the dendrogram
	# create the counts of samples under each node
	counts = np.zeros(model.children_.shape[0])
	n_samples = len(model.labels_)
	for i, merge in enumerate(model.children_):
		current_count = 0
		for child_idx in merge:
			if child_idx < n_samples:
				current_count += 1  # leaf node
			else:
				current_count += counts[child_idx - n_samples]
		counts[i] = current_count
	linkage_matrix = np.column_stack([model.children_, model.distances_,counts]).astype(float)
	# Plot the corresponding dendrogram
	dendrogram(linkage_matrix, **kwargs)

usage = """<documentation>"""
parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input", type = str, help="Chemin vers le fichier en input(fichier tsv)")
parser.add_argument("output", type=str, help="Chemin vers le fichier output(dendrogramme au format png)")
args = parser.parse_args()
fic_input = args.input
fic_output = args.output
input_utilisateur=input("Voulez vous calculer la base et le collocatif ? oui/non ").lower()

if input_utilisateur in ['oui','non']:
	tableau_de_vecteur=open(fic_input,'r',encoding='utf8')#fichier input
	next(tableau_de_vecteur) #ignore la 1ère ligne du fichier input (nom des colonnes)

	liste_nom_vecteur=[] #liste vide qui indiquera la base/collocatif du vecteur (string)
	liste_de_liste_vecteur=[]#liste qui contiendra chaque vecteur avec ses 768 coefficients. exemple [[vecteur1=1.26,1.50,...],[vecteur2=0.30,1.59,...]]

	for ligne in tableau_de_vecteur:#parcours du fichier en input (col1=ligne de la phrase, col2=token de la base, col3=vecteur de la base, col4=token du collocatif, col5=vecteur du collocatif)
		ligne_split = ligne.split("\t")
		
		col_compositionnel=ligne_split[1]#trait compositionnel : Oui/Non
		col_base=ligne_split[2]#colonne de la base, chaine de caractères
		col_v_base=ligne_split[3].split()#colonne vecteur de la base(split à l'espace car on veut une liste et pas une chaine de caractères)
		
		col_colloc=ligne_split[4]#colonne collocatif
		col_v_colloc=ligne_split[5].split()#colonne vecteur collocatif
		
		liste=[]#liste vide où l'on ajoutera le résultat base - collocatif de chaque coefficient(768 par ligne)
		for i in range(0,len(col_v_base)):#parcours des 768 coefficients de chaque vecteur
			vecteur_base=col_v_base[i]#coefficient de la base
			vecteur_colloc=col_v_colloc[i]#coefficient du collocatif
			if input_utilisateur=="oui":
				resultat = float(vecteur_base) - float(vecteur_colloc) #soustraction base - collocatif. En float car à la base il s'agit de string.
			if input_utilisateur=="non":
				resultat = float(vecteur_colloc) #collocatif. En float car à la base il s'agit de string.
			liste.append(resultat)
		liste_nom_vecteur.append(col_compositionnel+"/"+col_base+"/"+col_colloc) #ajout de la base/collocatif de chaque vecteur (ex : colère/saine, maison/belle, ...)
		liste_de_liste_vecteur.append(liste)#on ajoute à la liste le vecteur de la ligne

	#setting distance_threshold=0 ensures we compute the full tree.
	model = AgglomerativeClustering(distance_threshold=0, n_clusters=None,affinity='cosine',linkage='complete', compute_full_tree=True)#calcul du cosinus, arbre entier
	model = model.fit(liste_de_liste_vecteur)#on utilise comme input la liste "liste_de_liste_vecteur" qui contient les vecteurs.

	#Boucle pour donner à chaque vecteur le label qui lui correspond
	liste_de_label=[]
	for i in range(0,len(liste_nom_vecteur)):
		liste_de_label.append(liste_nom_vecteur[i])
	
	if input_utilisateur=='oui':
		fichier_split="dendrogramme"+" "+fic_input.split("\\")[-1]+" "+"BASE + COLLOCATIF"
	if input_utilisateur=='non':
		fichier_split="dendrogramme"+" "+fic_input.split("\\")[-1]+" "+"COLLOCATIF SEUL"
	plt.title(fichier_split)
	
	plt.rcParams['lines.linewidth'] = 0.2 # réduit la taille des traits du dendrogramme
	plot_dendrogram(model,truncate_mode=None,labels=liste_de_label,orientation='right',leaf_font_size=1)#orientation du dendrogramme(right=sur la droite), labels=le nom du vecteur(ex: Oui/soleil/plomb),leaf=0.1 : réduit la taille de la police pour la légende
	# ~ plt.savefig(fic_output,dpi=600,format="pdf")
	plt.savefig(fic_output,dpi=600)
	
	# ~ plot_dendrogram(model,truncate_mode=None,labels=liste_de_label,orientation='right')#orientation du dendrogramme(right=sur la droite), labels=le nom du vecteur(ex: Oui/soleil/plomb),leaf=0.1 : réduit la taille de la police pour la légende
	# ~ plt.show()
else:
	print("Veuillez taper oui ou non")
