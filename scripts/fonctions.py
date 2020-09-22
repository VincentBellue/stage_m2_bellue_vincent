#fonctions appelées par les scripts dendrogramme_fasttext.py, dendrogramme_flaubert_onze_ex.py, dendrogramme_flaubert_vingt_ex.py, matrice_et_heatmap_fasttext.py, matrice_et_heatmap_flaubert_onze_ex.py, matrice_et_heatmap_flaubert_vingt_ex.py

import argparse
import torch
import random
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import os

#fonction demandant le chemin d'accès au fichier input et où sera créé le fichier output + question pour calcul de collocatif ou base-collocatif. L'utilisateur peut taper "python nom_du_script.py -h" pour obtenir de l'aide sur les types de fichiers input et outputs nécessaires.
def input_utilisateur(type_fic_output,calcul_colloc_seul):
	usage = """<documentation>"""
	parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("input", type = str, help="Chemin vers le fichier en input(fichier tsv)")
	if type_fic_output:#cas d'un script nécessitant un output de type tsv
		parser.add_argument("output", type=str, help="Chemin vers le fichier output(fichier tsv)")
	else:#cas d'un script nécessitant un output de type png
		parser.add_argument("output", type=str, help="Chemin vers le fichier output(fichier png)")#cas d'une image (dendrogramme, pour le cas d'une heatmap le traitement est fait en même temps que le fichier tsv, donc le fichier output choisi sera en .tsv)
	args = parser.parse_args()
	fic_input = args.input
	fic_output = args.output
	oui_ou_non=True #Booleen sur True par défaut. Reponse à la question posée à la ligne d'après. oui=calcul base-collocatif, non=calcul collocatif seul.
	if calcul_colloc_seul:#cas où l'on veut voir apparaitre le message demandant le calcul du collocatif seul ou base-collocatif.
		input_utilisateur=input("Voulez vous calculer la base et le collocatif ? oui/non ").lower()
		if input_utilisateur =='oui':
			oui_ou_non=True#si lutilisateur tape "oui" alors oui_non reste sur True(donc calcul de base-collocatif)
		elif input_utilisateur=='non':
			oui_ou_non=False #si l'utilisateur tape "non" alors oui_non passe à False(donc calcul collocatif seul)
		else:
			oui_ou_non=None#si l'utilisateur tape autre chose oui_ou_non passe sur None
			print("Veuillez taper oui ou non")#message d'erreur
	return(fic_input,fic_output,oui_ou_non)#return le fichier input+output tapés par l'utilisateur et la réponse à la question(oui=True, non=False, autre chose=None)

#fonction de découpage du fichier.traitements différents selon le choix : 
#similarite:True(matrice de similarité)/False(dendrogramme);reponse:True(soustraction base-collocatif)/False(collocatif seul),statique:True(vecteur statique)/False(vecteur contextuel)
def decoupage(liste,reponse,similarite,statique,liste_base_colloc):#liste et liste_base_colloc récupérés dans la fonction parcours_fichier
	liste_de_listes=[]#liste de tenseurs pytorch si similarite=True / liste de liste de vecteurs si similarite=False(chaque liste dans la liste contient un vecteur)
	nom_vecteur=""#chaine vide qui contiendra le nom du vecteur sous la forme compositionnel(Oui/Non)/base/collocatif. (ex : Non/colère/saine)
	col_ligne=liste[0]#numéro de la ligne
	col_compositionnel=liste[1]#trait compositionnel : Oui/Non
	col_base=liste[2]#colonne de la base, chaine de caractères
	col_v_base=liste[4].split()#colonne vecteur de la base(split à l'espace car on veut une liste et pas une chaine de caractères)
	col_colloc=liste[5]#colonne collocatif
	col_v_colloc=liste[6].split()#colonne vecteur collocatif
	if statique:#uniquement pour calcul de vecteurs statiques
		if (col_base,col_colloc) not in liste_base_colloc:#si le couple base/collocatif n'est pas encore dans la liste "liste_base_colloc"
			liste_base_colloc.append((col_base,col_colloc)) #on l'ajoute, afin d'effectuer le calcul du vecteur base-collocatif une seule fois (étant donné qu'il y a plusieurs fois le même couple base/collocatif dans le fichier)
			liste=[]#liste vide où l'on ajoutera le résultat base - collocatif de chaque coefficient(300 par ligne pour fasttext)
			for i in range(0,len(col_v_base)):#parcours des 300 coefficients du vecteur
				vec_base=col_v_base[i]#coefficient de la base
				vec_colloc=col_v_colloc[i]#coefficient du collocatif
				resultat = float(vec_base) - float(vec_colloc) #soustraction base - collocatif. En float car il s'agissait de str.
				liste.append(resultat)#ajout du resultat base - collocatif dans la liste pour chaque coefficient
			nom_vecteur=col_compositionnel+"/"+col_base+"/"+col_colloc #ajout de compositionnel/base/collocatif de chaque vecteur (ex : Non/colère/saine, Oui/maison/belle)
			if similarite:#si l'on veut faire une matrice de similarité et par la suite une heatmap
				liste_de_listes.append(torch.tensor(liste))#on transforme la liste de resultats en tenseur pytorch
			elif similarite==False:#si l'on veut faire une liste de liste(avec un vecteur par liste) pour ensuite faire un dendrogramme
				liste_de_listes.append(liste)#on ajoute chaque liste(donc le vecteur) à la liste finale
		return(liste_de_listes,nom_vecteur,liste_base_colloc)
	elif statique==False:#cas où l'on veut des vecteurs contextuels (FlauBERT)
		liste=[]#liste vide où l'on ajoutera le résultat base - collocatif de chaque coefficient(768 par ligne pour FlauBERT)
		for i in range(0,len(col_v_base)):#parcours des 768 coefficients du vecteur
			vecteur_base=col_v_base[i]#coefficient de la base
			vecteur_colloc=col_v_colloc[i]#coefficient du collocatif
			if reponse:#si l'on a tapé au préalable "oui" à la question posée: calcul base-collocatif
				resultat = float(vecteur_base) - float(vecteur_colloc) #soustraction base - collocatif. En float car à la base il s'agit de string.
			elif reponse==False:#si l'on a tapé "non" au préalable en reponse à la question: calcul collocatif seul
				resultat = float(vecteur_colloc) #vecteur du collocatif
			liste.append(resultat)#ajout du resultat base - collocatif/collocatif seul dans la liste pour chaque coefficient
		nom_vecteur=col_compositionnel+"/"+col_base+"/"+col_colloc #ajout de trait compositionnel(oui/non)/la base/collocatif de chaque vecteur (ex : Non/colère/saine, Oui/maison/belle, ...)
		if similarite:#si l'on veut faire une matrice de similarité et par la suite une heatmap
			liste_de_listes.append(torch.tensor(liste))#on transforme la liste de résultats en tenseur de pytorch
		elif similarite==False:#si l'on veut faire une liste de liste(de vecteur) pour ensuite faire un dendrogramme
			liste_de_listes.append(liste)
		return(liste_de_listes,nom_vecteur)

#fic_input=return de la fonction input_utilisateur; reponse=return de la fonction input_utilisateur-> reponse à la question(oui=True, non=False,autre=None)
#similarite=True->matrice de similarité(pour heatmap)/False-> liste de listes(pour dendrogramme); statique=True(vecteurs statiques)/False(vecteurs contextuels)
def parcours_fichier(fic_input,reponse,similarite,statique,onze_ex):
	fichier_lu=open(fic_input,'r',encoding='utf8')
	next(fichier_lu) #ignore la 1ère ligne du fichier input (nom des colonnes)
	liste_de_liste=[]#si similarite=True->liste de tensors pytorch; si similarite=False->liste de listes(chaque liste contient un vecteur)
	liste_nom_vecteur=[] #liste vide qui indiquera trait compositionnel(oui/non)/la base/collocatif du vecteur (string)
	if onze_ex:#si onze exemples par groupe
		liste_phrase=[]#liste intermédiaire
		grosse_liste=[]#liste de liste qui contiendra les groupes de 20phrases dont on a besoin(2listes de 20 phrases si input de 40 phrases)
		#boucle permettant de faire des groupes de 20(pour pouvoir la split en deux groupes de 10 après)
		cpt=1
		for ligne in fichier_lu:
			liste_phrase.append(ligne)
			if cpt==20:
				grosse_liste.append(liste_phrase)
				liste_phrase=[]
				cpt=0
			cpt+=1
		for line in grosse_liste:#parcours des listes de 20 phrases
			liste1=line[0:10] #liste des 10 premiers éléments(FL)
			liste2=line[10:20] #liste des 10 derniers éléments (compositionnels)
			phrase_random=random.choice(liste1) #choix au hasard d'une phrase parmi les 10 de la FL
			liste2.append(phrase_random)
			for elem in liste2:#parcours des lignes dans chaque liste de 10 (séparées par des \t)
				ligne_split = elem.split("\t")
				#appel de la fonction decoupage sur ligne_split. False car on est dans une condition onze_ex=True et onze_ex ne fonctionne que pour un vecteur contextuel, donc impossible que ça soit un vecteur statique et [] car dans le cas d'un vecteur contextuel on ne rempli par la liste_base_colloc
				listes,vecteur=decoupage(ligne_split,reponse,similarite,False,[])
				liste_de_liste+=listes
				liste_nom_vecteur.append(vecteur)
	else :#si onze_ex=False
		if statique==True:
			liste_base_colloc=[]#liste vide créée uniquement dans le cas où l'on calcule des vecteurs statiques
		for ligne in fichier_lu:
			ligne_split=ligne.split("\t")
			if statique:#si calcul de vecteur statique
				listes,vecteur,liste_bases_collocs=decoupage(ligne_split,reponse,similarite,True,liste_base_colloc)#appel de la fonction decoupage. True car vecteur statique, et liste_base_colloc est utilisée.
			else:#si vecteur contextuel
				listes,vecteur=decoupage(ligne_split,reponse,similarite,False,[])#appel de la fonction decoupage. False car statique=False donc vecteur contextuel 20 exemples, [] car pas besoin de faire une liste de base_colloc
			liste_de_liste+=listes
			if vecteur!="":#on ajoute le vecteur a la liste seulement si la chaine de caractères ne reste pas vide.
				liste_nom_vecteur.append(vecteur)
	return(liste_nom_vecteur,liste_de_liste)#return les deux listes: liste_nom_vecteur=trait compositionnel(oui/non)/base/collocatif de chaque vecteur;liste_de_liste=soit liste pytorch, soit liste de liste(chaque liste contient un vecteur)


#fonction pour créer la matrice de similarité
def output_matrice(fichier_output,liste_nom_vecteur,liste_de_liste):#prend en input le fichier output de la fonction input_utilisateur, la liste des noms de vecteurs et la liste de vecteurs.
	output=open(fichier_output,'w',encoding='utf8')#ouverture de l'output
	for nom in liste_nom_vecteur:
		output.write("\t"+nom)#écriture de la 1ère ligne. 1ère cellule vide, puis Oui-Non/base/collocatif
	for i in range(0,len(liste_de_liste)): #boucle1 i sur la liste de tenseurs
		output.write("\n"+liste_nom_vecteur[i]+"\t")#dans la 1ère colonne sur chaque ligne écrire le couple oui-non/base/collocatif qui correspond au vecteur(Non/colère/saine, Oui/maison/belle, ...)
		resultat_ligne="" #initialisation d'une chaine de caractères vide
		for j in range(0,len(liste_de_liste)):#boucle2 j sur la liste de tenseur
			resultat_cosinus_tensor=torch.nn.functional.cosine_similarity(liste_de_liste[i],liste_de_liste[j],dim=0)#comparaison liste[i] et liste[j] pour obtenir la similarité cosinus
			resultat_cosinus=str(resultat_cosinus_tensor.item())#on récupère ce qui nous intéresse sur le tenseur (la similarité cosinus)
			resultat_ligne+=resultat_cosinus+"\t" #on l'ajoute à la chaine de caractère, en séparant par des \t.
		output.write(resultat_ligne)#on écrit dans le fichier le contenu de la variable resultat_ligne (ligne par ligne)

#fonction pour le dendrogramme(trouvée sur https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html)
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

#fonction permettant de créer un dendrogramme
#reponse,statique,onze_ex,input_user,dendro utilisés seulement pour nommer le fichier output correctement lors de l'appel de la fonction nom_de_fichier_output
def dendrogramme_output(liste_de_liste_vecs,liste_nom_vecteur,reponse,statique,onze_ex,input_user,dendro):
	model = AgglomerativeClustering(distance_threshold=0, n_clusters=None,affinity='cosine',linkage='complete', compute_full_tree=True)#calcul du cosinus, arbre entier
	model = model.fit(liste_de_liste_vecs)#on utilise comme input la liste "liste_de_liste_vecteur" qui contient les vecteurs.
	#Boucle pour donner à chaque vecteur le label qui lui correspond
	liste_de_label=[]
	for i in range(0,len(liste_nom_vecteur)):
		liste_de_label.append(liste_nom_vecteur[i])
	#appel de la fonction pour avoir des infos sur le fichier et le nommer correctement
	nom_du_fichier_split=nom_de_fichier_output(input_user,dendro,statique,onze_ex,reponse)
	return(nom_du_fichier_split,liste_de_label,model)

#fonction permettant de créer une heatmap
#dendro,statique,onze_ex,reponse utilisés seulement pour nommer correctement le fichier output lors de l'appel de la fonction nom_de_fichier_output. toutes_les_vals= booléen pour l'écart entre chaque valeur affichée.
def heatmap_output(fic_entree,toutes_les_vals,dendro,statique,onze_ex,reponse):
	data = pd.read_csv(fic_entree,sep='\t')
	#appel de la fonction pour nommer la figure correctement
	nom_du_fichier_split=nom_de_fichier_output(fic_entree,dendro,statique,onze_ex,reponse)
	# récupérer les noms de colonnes + mettre Unnamed à la fin
	cols = data.columns[1:]
	cols = cols.append(data.columns[0:1])
	# Réassigner les noms
	data.columns = cols
	# retirer la colonne Unnamed qui ne contient que des Nan
	data = data.drop("Unnamed: 0", axis=1)
	heat_map = sb.heatmap(data)#création de la heatmap
	labels=data.columns #on utilise les colonnes du fichier pour avoir le nom des labels (Oui/soleil/plomb)
	nom_de_label=[]
	if toutes_les_vals:#si l'on veut une heatmap avec toutes les valeurs, avec un écart de 1
		for i in range(0,len(labels)):
			nom_de_label.append(labels[i])
	else:#heatmap avec un écart de 10 entre les valeurs affichées
		cpt=0
		for i in range(0,len(labels)): #parcours des labels
			if i==cpt:#si le label est égal au compteur, on l'ajoute à la liste. Ne garde que les multiples de 10, donc 1 label tous les 10.
				nom_de_label.append(labels[i])
				cpt+=10
	input_split = os.path.splitext(fic_entree)#on reprend le nom du fichier sans l'extension et ajoute _HEATMAP.png
	fic_out=input_split[0]+"_HEATMAP"+".png"
	return(fic_out,nom_de_label,labels,nom_du_fichier_split)

#fonction pour nommer la figure(heatmap/dendrogramme) correctement. Utilise uniquement des booléens et le nom du fichier en input
def nom_de_fichier_output(input_util,dendro,statique,onze_ex,reponse):
	if dendro:
		nom_fich="Dendrogramme "
	else:
		nom_fich="Heatmap "
	if statique:
		vec="vecteurs statiques "
	else:
		vec="vecteurs contextuels "
	if onze_ex:
		exemples="(groupes de 11, "
	else:
		if statique:
			exemples="("
		else:
			exemples="(groupes de 20, "
	if reponse:
		rep="Base-Collocatif) "
	else:
		rep="Collocatif seul) "
	nom_fich_input=os.path.basename(input_util)
	fichier_split=nom_fich+vec+exemples+rep+nom_fich_input
	return(fichier_split)
