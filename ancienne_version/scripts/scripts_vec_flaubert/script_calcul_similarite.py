import argparse
import torch
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram

usage = """<documentation>"""
parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input", type = str, help="Chemin vers le fichier en input(fichier tsv)")
parser.add_argument("output", type=str, help="Chemin vers le fichier output(fichier tsv)")
args = parser.parse_args()
fic_input = args.input
fic_output = args.output
input_utilisateur=input("Voulez vous calculer la base et le collocatif ? oui/non ").lower()

if input_utilisateur in ['oui','non']:
	tableau_de_vecteur=open(fic_input,'r',encoding='utf8')#fichier input
	next(tableau_de_vecteur) #ignore la 1ère ligne du fichier input (nom des colonnes)

	tensor_liste=[]#liste qui contiendra les tenseurs des 768 coefficients de chaque ligne
	liste_nom_vecteur=[] #liste vide qui indiquera la base/collocatif du vecteur (string)

	for ligne in tableau_de_vecteur:#parcours du fichier en input (col1=ligne de la phrase, col2=token de la base, col3=vecteur de la base, col4=token du collocatif, col5=vecteur du collocatif)
		ligne_split = ligne.split("\t")
		col_ligne=ligne_split[0]#colonne numéro de la ligne
		
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
			
			liste.append(resultat)#ajout du resultat base - collocatif dans la liste pour chaque coefficient
		liste_nom_vecteur.append(col_compositionnel+"/"+col_base+"/"+col_colloc) #ajout de la base/collocatif de chaque vecteur (ex : colère/saine, maison/belle, ...)
		tensor_liste.append(torch.tensor(liste))#on transforme la liste de resultats en tenseur de pytorch

	output=open(fic_output,'w',encoding='utf8')#ouverture de l'output : matrice 200x200

	for nom in liste_nom_vecteur:#parcours de la liste qui contient pour chaque vecteur le nom de la base/collocatif qui correspond.
		output.write("\t"+nom)#écriture de la 1ère ligne. 1ère cellule vide, puis nom de la base/collocatif

	for i in range(0,len(tensor_liste)): #boucle1 i sur la liste de tenseurs
		output.write("\n"+liste_nom_vecteur[i]+"\t")#dans la 1ère colonne sur chaque ligne écrire le couple base/collocatif qui correspond au vecteur(colère/saine, maison/belle, ...)
		resultat_ligne="" #initialisation d'une chaine de caractères vide
		for j in range(0,len(tensor_liste)):#boucle2 j sur la liste de tenseur
			resultat_cosinus_tensor=torch.nn.functional.cosine_similarity(tensor_liste[i],tensor_liste[j],dim=0)#comparaison liste[i] et liste[j] pour obtenir la similarité cosinus
			resultat_cosinus=str(resultat_cosinus_tensor.item())#on récupère ce qui nous intéresse sur le tenseur (la similarité cosinus)
			resultat_ligne+=resultat_cosinus+"\t" #on l'ajoute à la chaine de caractère, en séparant par des \t.
		output.write(resultat_ligne)#on écrit dans le fichier le contenu de la variable resultat_ligne (ligne par ligne)

	#demi-matrice (pour ne pas avoir de résultats en double), à supprimer plus tard.
	# ~ for i in range(0,len(tensor_liste)-1): #boucle1 i sur la liste de tenseurs -1
		# ~ output.write("\n"+liste_nom_vecteur[i]+"\t")
		# ~ resultat_ligne=""
		# ~ for j in range(i+1,len(tensor_liste)):#boucle2 j sur la liste de tenseur
			# ~ resultat_cosinus_tensor=torch.nn.functional.cosine_similarity(tensor_liste[i],tensor_liste[j],dim=0)#comparaison liste[i] et liste[j] pour obtenir la similarité cosinus
			# ~ resultat_cosinus=str(resultat_cosinus_tensor.item())
			# ~ resultat_ligne+=resultat_cosinus+"\t"
		
		# ~ for cpt in range(0,i+1):
			# ~ output.write("\t")
		# ~ output.write(resultat_ligne)
	# ~ output.write("\n"+liste_nom_vecteur[len(liste_nom_vecteur)-1])

else:
	print("Veuillez taper oui ou non")
