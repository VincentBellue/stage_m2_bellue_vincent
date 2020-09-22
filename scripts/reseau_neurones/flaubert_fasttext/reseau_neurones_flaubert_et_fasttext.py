#Exemples de fichiers en input : Pour FlauBERT (1er argument en input) -> FL_BON_OUTPUT.tsv, pour FastText (2ème argument en input) -> FL_BON_OUTPUT_VEC_STATIQUE.tsv

import torch
import numpy as np
import torch.nn as nn
from torch.nn import functional as F
import torch.optim as optim
import argparse
import os

def input_utilisateur():
	usage = """<documentation>"""
	parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("input_flaubert", type = str, help="Chemin vers le fichier en input FlauBERT (fichier tsv)")
	parser.add_argument("input_fasttext", type=str, help="Chemin vers le fichier en input FastText (fichier tsv)")
	parser.add_argument("output", type=str, help="Chemin vers le fichier output(fichier tsv)")
	args = parser.parse_args()
	fic_input_un = args.input_flaubert
	fic_input_deux = args.input_fasttext
	fic_output = args.output
	return(fic_input_un,fic_input_deux,fic_output)#return le fichier input+output tapés par l'utilisateur et la réponse à la question(oui=True, non=False, autre chose=None)

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

def parcours(fichier_input):
	fic_split =  os.path.basename(fichier_input)
	tableau=open(fichier_input,'r',encoding='utf8')
	next(tableau)
	liste_vecteur=[]#liste vide de vecteurs
	compo_oui_non=[]#liste vide de trait compositionnel oui/non
	nom_collocation=[]#liste vide nom de collocation (base + collocatif)
	
	for ligne in tableau:
		ligne_split = ligne.split("\t")
		col_compositionnel=ligne_split[1]#trait compositionnel : Oui/Non
		nom_base=ligne_split[2]#nom de la base
		genre_base=ligne_split[3]#genre de la base
		col_v_base=ligne_split[4].split()#colonne vecteur de la base(split à l'espace car on veut une liste et pas une chaine de caractères)
		nom_colloc=ligne_split[5]#nom du collocatif
		col_v_colloc=ligne_split[6].split()#vecteur collocatif
		
		#concaténation du nouveau vecteur + convertion en float
		nouveau_vec=col_v_base+col_v_colloc#concaténation de la base et du collocatif (768x2)
		liste_de_float = [float(x) for x in nouveau_vec]#convertion du nouveau vecteur en float car il s'agit de string actuellement
		
		#ajout dans les listes vides
		if col_compositionnel=="Oui":#transforme oui en en int(1)
			col_compositionnel=1
		elif col_compositionnel=="Non":#transforme non en int(0)
			col_compositionnel=0
		compo_oui_non.append(col_compositionnel)
		liste_vecteur.append(torch.tensor(liste_de_float))#convertion du vecteur en tenseur pytorch
		nom_collocation.append(nom_base+" "+nom_colloc)
	return(liste_vecteur,compo_oui_non,nom_collocation,fic_split)#fic_split= nom du fichier.tsv


def entrainement(input_vec,input_compo):#en arguments la liste de tenseurs et la liste trait compositionnel(0/1). On utilise cette fonction pour chaque groupe de 180 (ou 380 si 400 exemples).
	input_vectors = input_vec#liste de tenseurs(180 tenseurs au total)
	dim_input=len(input_vectors[0])#nombre de dimensions (768 coeffs pour flaubert, 600 pour fasttext)
	dim_hidden = 100
	
	# output sous la forme d'une liste de booleen
	output_bool = [x for x in input_compo]#parcours de la liste de booléens(180 au total)
	
	# output sous la forme de tensors à 1 élément (il faut des float)
	output_tensor = [torch.tensor([b], dtype=torch.float) for b in output_bool]
	
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
			
			prediction = output > 0.5   # -> permet de calculer l'exactitude du modèle sur les données de test
			if int(prediction) == int(target):
				cpt_juste+=1
			
			loss = loss_function(output, target)
			loss_epoch += loss.detach().numpy()
			
			loss.backward()
			optimizer.step()
		accuracy=100*cpt_juste/len(output_tensor)#accuracy par époque
		# ~ print(f"Epoch {epoch} loss = {loss_epoch}"+" entrainement")
		# ~ print(accuracy,": précision sur l'epoch")
	return(model)#renvoie le modèle entrainé

def evaluation(model,vec_input,labels,noms_collocations):#input_data=20 tenseurs, labels=20 labels
	model.eval()#passe en mode évaluation
	
	input_vectors = vec_input#liste de tenseurs(20 tenseurs au total)
	
	# output sous la forme d'une liste de booleen
	output_bool = [x for x in labels]#parcours de la liste de booléens(20 au total)
	
	# output sous la forme de tensors à 1 élément (il faut des float)
	output_tensor = [torch.tensor([b], dtype=torch.float) for b in output_bool]
	
	name_collocation = [y for y in noms_collocations]#parcours des noms de collocations
	
	liste_attendu=[]
	liste_obtenu=[]
	liste_nom_collocation=[]
	
	
	
	cpt_juste=0
	for input_vector,target,collocation in zip(input_vectors, output_tensor,name_collocation):
		# calcul de l'output du modèle
		output = model(input_vector)
		
		prediction = output > 0.5   # -> permet de calculer l'exactitude du modèle sur les données de test
		if int(prediction) == int(target):
			cpt_juste+=1
		
		# ~ print("résultat attendu : "+str(int(target))+"\t"+"résultat obtenu : "+str(int(prediction)) +"\t"+"base + collocatif : "+collocation)
		liste_attendu.append(int(target))
		liste_obtenu.append(int(prediction))
		liste_nom_collocation.append(collocation)
	accuracy=100*cpt_juste/len(output_tensor)
	# ~ print("accuracy modèle :",accuracy,"%","\n")
	# ~ print("attendu",liste_attendu, "obtenu", liste_obtenu, "collocation", collocation)
	return(accuracy,liste_attendu,liste_obtenu,liste_nom_collocation)


#appel de la fonction input_utilisateur
fichier_flaubert,fichier_fasttext,fichier_en_sortie=input_utilisateur()#fichier en entrée tapé par l'utilisateur (flaubert et fasttext) + fichier en sortie

# ~ #appel de la fonction parcours sur l'input flaubert et l'input fasttext
# ~ #flaubert
liste_vecteurs_flaubert,compo_flaubert,nom_collocation_flaubert,nom_fic_flaubert=parcours(fichier_flaubert)

# ~ #fasttext
liste_vecteurs_fasttext,compo_fasttext,nom_collocation_fasttext,nom_fic_fasttext=parcours(fichier_fasttext)


#appel de la fonction compteur, pour séparer les données en listes de 20 éléments
#flaubert
liste_vec_flaubert=compteur(liste_vecteurs_flaubert)#liste de liste de tenseurs(10 listes de 20 tenseurs)
liste_compo_flaubert=compteur(compo_flaubert)#liste de trait compositionnel(10 listes de 20 oui(1)/non(0))
nom_collocation_flaubert=compteur(nom_collocation_flaubert)#liste de liste des collocations (10 liste de 20 nom base+" "+nom collocatif)

#fasttext
liste_vec_fasttext=compteur(liste_vecteurs_fasttext)#liste de liste de tenseurs(10 listes de 20 tenseurs)
liste_compo_fasttext=compteur(compo_fasttext)#liste de trait compositionnel(10 listes de 20 oui(1)/non(0))
nom_collocation_fasttext=compteur(nom_collocation_fasttext)#liste de liste des collocations (10 liste de 20 nom base+" "+nom collocatif)

#appel de la fonction corpus, pour séparer le corpus en corpus d'entrainement et corpus de test.
#flaubert
entrainement_vecteurs_flaubert,test_vecteurs_flaubert=corpus(liste_vec_flaubert)#création des groupes de 180(180 séparés en listes de 20) et groupes de 20 pour les tenseurs
entrainement_compo_flaubert,test_compo_flaubert=corpus(liste_compo_flaubert)#création des groupes de 180 compositionnel oui/non(180 séparés en listes de 20) et groupe de 20 oui(1)/non(0)

#fasttext
entrainement_vecteurs_fasttext,test_vecteurs_fasttext=corpus(liste_vec_fasttext)#création des groupes de 180(180 séparés en listes de 20) et groupes de 20 pour les tenseurs
entrainement_compo_fasttext,test_compo_fasttext=corpus(liste_compo_fasttext)#création des groupes de 180 compositionnel oui/non(180 séparés en listes de 20) et groupe de 20 oui(1)/non(0)


accuracy_flaubert=0
accuracy_fasttext=0

output=open(fichier_en_sortie,"w",encoding="utf8")
output.write("\t"+nom_fic_flaubert+"\t"+nom_fic_fasttext+"\n")
output.write("Groupe"+"\t"+"Accuracy vecteurs FlauBERT"+"\t"+"Accuracy vecteurs FastText"+"\n")

for i in range(0,len(entrainement_vecteurs_flaubert)):
	print("Corpus numéro :",i+1)
	#flaubert
	#données entrainement
	liste_vec_flaubert=[]#liste vide pour rassembler en une seule liste de 180 éléments les 180 éléments qui étaient séparés en listes de 20.
	trn_vec_flaubert=entrainement_vecteurs_flaubert[i]#compositionnel pour l'entrainement
	for vec_flaubert in trn_vec_flaubert:#parcours des listes et concatenation pour ne faire plus qu'une liste de 180 éléments
		liste_vec_flaubert+=vec_flaubert
		
	liste_compo_flaubert=[]#liste vide pour rassembler en une seule liste de 180 éléments les 180 éléments qui étaient séparés en listes de 20.
	trn_compo_flaubert=entrainement_compo_flaubert[i]#compositionnel pour l'entrainement
	for compo_flaubert in trn_compo_flaubert:#parcours des listes et concatenation pour ne faire plus qu'une liste de 180 éléments
		liste_compo_flaubert+=compo_flaubert
	
	#données test
	tst_vec_flaubert=test_vecteurs_flaubert[i]#tenseurs pour le test
	tst_compo_flaubert=test_compo_flaubert[i]#compositionnel pour le test
	nom_collocation_test_flaubert=nom_collocation_flaubert[i]#nom des collocations (base + colloc) de chaque groupe de 20 (qui correspondent aux vecteurs de test)
	
	
	#fasttext
	#données entrainement
	liste_vec_fasttext=[]#liste vide pour rassembler en une seule liste de 180 éléments les 180 éléments qui étaient séparés en listes de 20.
	trn_vec_fasttext=entrainement_vecteurs_fasttext[i]#compositionnel pour l'entrainement
	for vec_fasttext in trn_vec_fasttext:#parcours des listes et concatenation pour ne faire plus qu'une liste de 180 éléments
		liste_vec_fasttext+=vec_fasttext
		
	liste_compo_fasttext=[]#liste vide pour rassembler en une seule liste de 180 éléments les 180 éléments qui étaient séparés en listes de 20.
	trn_compo_fasttext=entrainement_compo_fasttext[i]#compositionnel pour l'entrainement
	for compo_fasttext in trn_compo_fasttext:#parcours des listes et concatenation pour ne faire plus qu'une liste de 180 éléments
		liste_compo_fasttext+=compo_fasttext
	
	#données test
	tst_vec_fasttext=test_vecteurs_fasttext[i]#tenseurs pour le test
	tst_compo_fasttext=test_compo_fasttext[i]#compositionnel pour le test
	nom_collocation_test_fasttext=nom_collocation_fasttext[i]#nom des collocations (base + colloc) de chaque groupe de 20 (qui correspondent aux vecteurs de test)


	#appel de la fonction d'entrainement sur les données d'entrainement (liste de tenseurs et liste de compositionnel)
	modele_flaubert=entrainement(liste_vec_flaubert,liste_compo_flaubert)
	modele_fasttext=entrainement(liste_vec_fasttext,liste_compo_fasttext)
	
	
	#utilisation du modele entrainé comme modèle pour le test
	#flaubert
	exactitude_modele_flaubert,attendu_flaubert,obtenu_flaubert,nom_colloc_flaubert=evaluation(modele_flaubert,tst_vec_flaubert,tst_compo_flaubert,nom_collocation_test_flaubert)#appel de la fonction d'entrainement sur les données d'entrainement (liste de tenseurs et liste de compositionnel) x 10
	exactitude_modele_fasttext,attendu_fasttext,obtenu_fasttext,nom_colloc_fasttext=evaluation(modele_fasttext,tst_vec_fasttext,tst_compo_fasttext,nom_collocation_test_fasttext)#appel de la fonction d'entrainement sur les données d'entrainement (liste de tenseurs et liste de compositionnel) x 10
	
	for j in range(0,len(attendu_flaubert)):
		flaubert_target=attendu_flaubert[j]
		flaubert_predit=obtenu_flaubert[j]
		nom_colloc=nom_colloc_flaubert[j]
		fasttext_predit=obtenu_fasttext[j]
	
		print("Résultat attendu :",flaubert_target,"\t","Résultat vecteur FlauBERT :",flaubert_predit,"\t","Résultat vecteur FastText :",fasttext_predit,"\t","Collocation :",nom_colloc)
	print("Accuracy FlauBERT",exactitude_modele_flaubert,"\t","Accuracy FastText",exactitude_modele_fasttext,"\n")
	accuracy_flaubert+=exactitude_modele_flaubert
	accuracy_fasttext+=exactitude_modele_fasttext

	
	output.write(str(i+1)+"\t"+str(exactitude_modele_flaubert)+"\t"+str(exactitude_modele_fasttext)+"\n")

accuracy_totale_flaubert=accuracy_flaubert/len(entrainement_vecteurs_flaubert)
accuracy_totale_fasttext=accuracy_fasttext/len(entrainement_vecteurs_fasttext)




print("Accuracy totale FlauBERT :",accuracy_totale_flaubert,"%","\t","Accuracy totale FastText :",accuracy_totale_fasttext,"%")


output.write("Total"+"\t"+str(accuracy_totale_flaubert)+"\t"+str(accuracy_totale_fasttext))

