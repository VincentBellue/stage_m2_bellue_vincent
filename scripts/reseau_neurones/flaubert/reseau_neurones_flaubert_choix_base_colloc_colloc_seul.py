#Exemple de fichier en input : FL_BON_OUTPUT.tsv

import torch
import numpy as np
import torch.nn as nn
from torch.nn import functional as F
import torch.optim as optim
import argparse
import os

def input_utilisateur(calcul_colloc_seul):
	usage = """<documentation>"""
	parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("input", type = str, help="Chemin vers le fichier en input(fichier tsv)")
	parser.add_argument("output", type=str, help="Chemin vers le fichier output(fichier tsv)")
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

#sépare le corpus en groupes de 20 exemples (dans une liste de liste), sous la forme [[liste1_elem1,liste1_elem2],[liste2_elem1,liste2_elem2],[...]]
def compteur(input_user):
	liste=[]#liste temporaire
	grosse_liste=[]#liste qui contient les listes de 20 éléments
	cpt=1
	for i in range(0,len(input_user)):
		liste.append(input_user[i])#ajout de l'élément dans la liste
		if cpt==20:#lorsqu'elle atteint 20 éléments
			grosse_liste.append(liste)#on les ajoute à la liste de liste
			liste=[]#et on recommence
			cpt=0
		cpt+=1
	return(grosse_liste)#renvoie la liste de listes

#parcours de la liste de listes(il peut s'agir de la liste de liste de tenseurs,de traits compositionnels, de nom de collocation ou de genre de la base)
def corpus(input_utilisateur):
	entrainement = []
	test = []
	for i, j in enumerate(input_utilisateur):
		entrainement.append(input_utilisateur[:i] + input_utilisateur[i+1:])#on ajoute dans entrainement tous les éléments sauf 20
		test.append(j)#on ajoute à test les 20 éléments restants, qui serviront à tester le modèle.
	return(entrainement,test)#renvoie deux listes: entrainement(tout sauf 20) et test(20 éléments)

def parcours(fichier_input,reponse):
	fic_split =  os.path.basename(fichier_input)
	tableau=open(fichier_input,'r',encoding='utf8')
	next(tableau)
	liste_vecteur=[]#liste vide de vecteurs
	compo_oui_non=[]#liste vide de trait compositionnel oui/non
	nom_collocation=[]#liste vide nom de collocation (base + collocatif)
	liste_genre_base=[]#liste vide du genre de la base (féminin/masculin)
	
	for ligne in tableau:
		ligne_split = ligne.split("\t")
		col_compositionnel=ligne_split[1]#trait compositionnel : Oui/Non
		nom_base=ligne_split[2]#nom de la base
		genre_base=ligne_split[3]#genre de la base
		col_v_base=ligne_split[4].split()#colonne vecteur de la base(split à l'espace car on veut une liste et pas une chaine de caractères)
		nom_colloc=ligne_split[5]#nom du collocatif
		col_v_colloc=ligne_split[6].split()#vecteur collocatif
		
		liste=[]#liste vide où l'on ajoutera le résultat base - collocatif de chaque coefficient(768 par ligne pour flaubert, 600 pour fasttext)
		for i in range(0,len(col_v_base)):#parcours des 768/600 coefficients de chaque vecteur
			vecteur_base=col_v_base[i]#coefficient de la base
			vecteur_colloc=col_v_colloc[i]#coefficient du collocatif
			if reponse:#si l'on a tapé au préalable "oui" à la question posée: calcul base-collocatif
				resultat = float(vecteur_base) - float(vecteur_colloc) #soustraction base - collocatif. En float car à la base il s'agit de string.
			elif reponse==False:#si l'on a tapé "non" au préalable en reponse à la question: calcul collocatif seul
				resultat = float(vecteur_colloc) #vecteur du collocatif
			liste.append(resultat)#ajout du resultat base - collocatif dans la liste pour chaque coefficient
		if col_compositionnel=="Oui":#transforme oui en en int(1)
			col_compositionnel=1
		elif col_compositionnel=="Non":#transforme non en int(0)
			col_compositionnel=0
		#ajout dans les listes vides
		compo_oui_non.append(col_compositionnel)
		liste_genre_base.append(genre_base)
		liste_vecteur.append(torch.tensor(liste))
		nom_collocation.append(nom_base+" "+nom_colloc)
	return(liste_vecteur,compo_oui_non,nom_collocation,liste_genre_base,fic_split)

#fonction permettant de comparer la valeur de deux clés. Booleen sur True par défaut:la valeur de la 2ème clé est plus grande que la 1ère. Si la 1ère est plus grande que la deuxième, renvoie False à la place, sinon si les deux sont égales, renvoie None.
def occurrences(dictionnaire,arg_un,arg_deux):#prend en argument : un dictionnaire avec clé->tuple genre+compositionnel, valeur->occurrences. on compare la valeur du 1er argument au 2ème.
	booleen=True#valeur par défaut (2ème argument plus grand que le 1er)
	if dictionnaire[(arg_un)]>dictionnaire[(arg_deux)]:#si la valeur du 1er argument est plus grande, passe sur False
		booleen=False
	elif dictionnaire[(arg_un)]==dictionnaire[(arg_deux)]:#cas où nombre d'occurrences est égal
		booleen=None
	return(booleen)#renvoie True si la 2ème valeur est plus grande, False si 1ère, et None si aucune (égalité)

def entrainement(input_vec,input_compo):#en arguments la liste de tenseurs et la liste trait compositionnel(0/1). On utilise cette fonction pour chaque groupe de 180 (ou 380 si 400 exemples).
	input_vectors = input_vec#liste de tenseurs(180 tenseurs au total)
	dim_input=len(input_vectors[0])#nombre de dimensions (768 coeffs pour flaubert, 600 pour fasttext)
	dim_hidden = 100
	
	# output sous la forme d'une liste de booleen
	output_bool = [x for x in input_compo]#parcours de la liste de booléens(180 au total)
	
	
	# output sous la forme de tensors à 1 élément (il faut des float)
	output_tensor = [torch.tensor([b], dtype=torch.float) for b in output_bool]
	
	# Modèle: réseau de neurones à une couche cachée:
	# On spécifie les opérations effectuées successivement
	model = nn.Sequential(
				nn.Linear(dim_input, dim_hidden),   #   output = M * input   (matrice de taille dim_hidden x dim_input )
				nn.Tanh(),                          #   output = tanh(input)   (fonction appliquée individuellement pour chaque coefficient)
				nn.Linear(dim_hidden, 1),           #   output = M' * input  (matrice de taille 1 x dim_hidden)
				nn.Sigmoid())                       #   output = Sigmoid(input)  (fonction appliquée individuellement pour chaque coefficient)
	loss_function = nn.BCELoss() #Creates a criterion that measures the Binary Cross Entropy between the target and the output
	
	optimizer = optim.Adam(model.parameters())
	
	for epoch in range(20): # itération sur les données d'entraînement
		loss_epoch = 0
		cpt_juste=0
		for input_vector, target in zip(input_vectors, output_tensor): # Pour chaque exemple d'entraînement
		
			optimizer.zero_grad()
			
			# calcul de l'output du modèle
			output = model(input_vector)
			
			# l'output est entre 0 et 1 et s'interprète comme P(compositionnel | exemple)
			# Pour extraire une prédiction, on considère que la réponse du modèle est 1 si output > 0.5 et 0 sinon
			prediction = output > 0.5   # -> permet de calculer l'exactitude du modèle sur les données de test
			# ~ if int(prediction) != int(target):#si la prédiction n'est pas la même que la cible
				# ~ print(prediction, int(target))
			if int(prediction) == int(target):
				cpt_juste+=1
			
			loss = loss_function(output, target)
			loss_epoch += loss.detach().numpy()
			
			loss.backward()
			optimizer.step()
		accuracy=100*cpt_juste/len(output_tensor)
		# ~ print(f"Epoch {epoch} loss = {loss_epoch}"+" entrainement")
		# ~ print(accuracy,": précision sur l'epoch")
	return(model)

def evaluation(model,input_data,labels,noms_collocations,genre_bases,syst_baseline_masc,syst_baseline_fem):#input_data=20 tenseurs, labels=20 labels
	model.eval()#passe en mode évaluation
	
	input_vectors = input_data#liste de tenseurs(20 tenseurs au total)
	
	# output sous la forme d'une liste de booleen
	output_bool = [x for x in labels]#parcours de la liste de booléens(20 au total)
	
	# output sous la forme de tensors à 1 élément (il faut des float)
	output_tensor = [torch.tensor([b], dtype=torch.float) for b in output_bool]
	
	name_collocation = [y for y in noms_collocations]#parcours des noms de collocations
	
	genre_base_finale = [z for z in genre_bases]#parcours du genre des bases
	
	cpt_juste_baseline=0
	cpt_juste=0
	for input_vector,target,collocation,base in zip(input_vectors, output_tensor,name_collocation,genre_base_finale):
		# calcul de l'output du modèle
		output = model(input_vector)
		
		prediction = output > 0.5   # -> permet de calculer l'exactitude du modèle sur les données de test
		if int(prediction) == int(target):
			cpt_juste+=1
		
		if base=="féminin":
			print("résultat attendu : "+str(int(target))+"\t"+"résultat obtenu : "+str(int(prediction))+"\t"+ "résultat baseline : "+str(int(syst_baseline_fem))+"\t"+"base + collocatif : "+collocation)
			if (int(syst_baseline_fem))==int(target):
				cpt_juste_baseline+=1
		elif base=="masculin":
			if (int(syst_baseline_masc))==int(target):
				cpt_juste_baseline+=1
			print("résultat attendu : "+str(int(target))+"\t"+"résultat obtenu : "+str(int(prediction))+"\t"+ "résultat baseline : "+str(int(syst_baseline_masc))+"\t"+"base + collocatif : "+collocation)
	accuracy=100*cpt_juste/len(output_tensor)
	accuracy_baseline=100*cpt_juste_baseline/len(output_tensor)
	print("accuracy modèle :",accuracy,"%","\t","accuracy système baseline :",accuracy_baseline,"%","\n")
	return(accuracy,accuracy_baseline)


#appel de la fonction input_utilisateur
fichier_en_entree,fichier_en_sortie,choix_utilisateur=input_utilisateur(True)#fichier en entrée tapé par l'utilisateur + fichier en sortie et choix de l'utilisateur à la question. True=on pose la question

#tant que l'utilisateur ne répond pas correctement on repose la question
while choix_utilisateur == None:
	fichier_en_entree,fichier_en_sortie,choix_utilisateur=input_utilisateur(True)

#appel de la fonction parcours
liste_vecteurs,compo_oui_non,nom_collocation,liste_genre_de_la_base,nom_du_fichier=parcours(fichier_en_entree,choix_utilisateur)#entrainement sur le corpus FL_BON + récupération du nom des collocations et le genre de la base et si elle est compositionnelle ou non et le nom du fichier (si chemin avec plusieurs dossiers, ne prend que le nom du fichier)

#appel de la fonction compteur, pour séparer les données en listes de 20 éléments
liste_de_vec=compteur(liste_vecteurs)#liste de liste de tenseurs(10 listes de 20 tenseurs)
liste_compo=compteur(compo_oui_non)#liste de trait compositionnel(10 listes de 20 oui(1)/non(0))
nom_collocation=compteur(nom_collocation)#liste de liste des collocations (10 liste de 20 nom base+" "+nom collocatif)
genre_base_liste_de_liste=compteur(liste_genre_de_la_base)#liste de liste du genre de la base (10 listes de 20)

#appel de la fonction corpus, pour séparer le corpus en corpus d'entrainement et corpus de test.(180 pour entrainement, et 20 pour test). Puis pour les 180, on fait une liste de liste.
#exemple liste vecteurs de test : [['vec1','...','vec20'],[...],['vec181','...','vec200']]
#exemple liste de vecteurs entrainement : [[['vec21', '...','vec40'],[...],['vec181','...', 'vec200']],[['vec1',"...",'vec20'],[...], ['vec160','...','vec180']]]
entrainement_vecteurs,test_vecteurs=corpus(liste_de_vec)#création des groupes de 180(180 séparés en listes de 20) et groupes de 20 pour les tenseurs
entrainement_compo,test_compo=corpus(liste_compo)#création des groupes de 180 compositionnel oui/non(180 séparés en listes de 20) et groupe de 20 oui(1)/non(0)
entrainement_genre_base,test_genre_base=corpus(genre_base_liste_de_liste)#création des groupes de 180 genre de la base masculin/feminin(180 séparés en listes de 20) et groupe de 20 masculin/feminin

#compteurs pour l'accuracy du modèle entrainé et baseline
accuracy_baseline=0
accuracy_modele=0

output=open(fichier_en_sortie,"w",encoding="utf8")
output.write(nom_du_fichier+"\n")
output.write("Groupe"+"\t"+"accuracy modèle"+"\t"+"accuracy système baseline"+"\n")

#on récupère à chaque passage de la boucle : tenseurs entrainement(180),tenseurs tests(20), compositionnel entrainement(180), compositionnel test(20), genre base entrainement(180), genre base test(20).
for i in range(0,len(entrainement_vecteurs)):
	print("Corpus numéro :",i+1)
	
	hash_genre_base_compo={}#dictionnaire vide, qui contiendra le nombre d'occurrence de chaque tuple
	
	#données entrainement
	liste_vide_compo=[]#liste vide pour rassembler en une seule liste de 180 éléments les 180 éléments qui étaient séparés en listes de 20.
	trn_compo=entrainement_compo[i]#compositionnel pour l'entrainement
	for compo in trn_compo:#parcours des listes et concatenation pour ne faire plus qu'une liste de 180 éléments
		liste_vide_compo+=compo
	
	liste_vide_vecteur=[]
	trn_vecteur=entrainement_vecteurs[i]#tenseurs pour l'entrainement
	for vect in trn_vecteur:#parcours des listes et concatenation pour ne faire plus qu'une liste de 180 éléments
		liste_vide_vecteur+=vect
	
	liste_vide_genre=[]
	trn_genre=entrainement_genre_base[i]
	for genre in trn_genre:
		liste_vide_genre+=genre
	
	#remplissage du dictionnaire pour avoir le nombre d'occurrences de masculin-féminin/compositionnel-non_compositionnel
	for j in range(0,len(liste_vide_genre)):#180 éléments
		genre_compo=(liste_vide_genre[j],liste_vide_compo[j])#tuple genre et compositionnel
		if genre_compo in hash_genre_base_compo:
			hash_genre_base_compo[genre_compo]+=1
		else:
			hash_genre_base_compo[genre_compo]=1
	
	#appel de la fonction du calcul d'occurrence
	booleen_masculin=occurrences(hash_genre_base_compo,('masculin', 0),('masculin', 1))#calcul pour masculin
	booleen_feminin=occurrences(hash_genre_base_compo,('féminin', 0),('féminin', 1))#calcul pour féminin
	
	#données test
	tst_vec=test_vecteurs[i]#tenseurs pour le test
	tst_compo=test_compo[i]#compositionnel pour le test
	nom_collocation_test=nom_collocation[i]#nom des collocations (base + colloc) de chaque groupe de 20 (qui correspondent aux vecteurs de test)
	genre_bases_tests=test_genre_base[i]
	
	#appel de la fonction d'entrainement sur les données d'entrainement (liste de tenseurs et liste de compositionnel) x 10 et nombre d'epoch.
	modele=entrainement(liste_vide_vecteur,liste_vide_compo)

	#utilisation du modele entrainé comme modèle pour le test
	# ~ print(nom_collocation_test)#print des 20 collocations des données de test
	exactitude_modele,exactitude_baseline=evaluation(modele,tst_vec,tst_compo,nom_collocation_test,genre_bases_tests,booleen_masculin,booleen_feminin)#appel de la fonction d'entrainement sur les données d'entrainement (liste de tenseurs et liste de compositionnel) x 10
	accuracy_modele+=exactitude_modele
	accuracy_baseline+=exactitude_baseline
	
	output.write(str(i+1)+"\t"+str(exactitude_modele)+"\t"+str(exactitude_baseline)+"\n")

accuracy_totale_modele=accuracy_modele/len(entrainement_vecteurs)
accuracy_totale_baseline=accuracy_baseline/len(entrainement_vecteurs)

print("accuracy totale du modèle :",accuracy_totale_modele,"%")
print("accuracy totale du système baseline :",accuracy_totale_baseline,"%")

output.write("total"+"\t"+str(accuracy_totale_modele)+"\t"+str(accuracy_totale_baseline))




