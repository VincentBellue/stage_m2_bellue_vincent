#Exemple de fichier en input : FL_BON.tsv

import argparse

usage = """<documentation>"""
parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input", type = str, help="Chemin du fichier input (tsv)")
parser.add_argument("output", type=str, help="Chemin du fichier output (tsv)")
args = parser.parse_args()
fic_input = args.input #fichier input
fic_output = args.output#fichier output

tableau=open(fic_input,'r',encoding='utf8')
next(tableau) #ignore la 1ère ligne du tableau
output=open(fic_output,'w',encoding='utf8')
output.write("Ligne" + "\t" + "Compositionnel" + "\t" "Base" + "\t" + "Genre base" + "\t" + "Vecteur base" + "\t" + "Collocatif" + "\t" + "Vecteur collocatif" + "\t" + "Phrase" + "\n")#entête des colonnes du fichier en output


liste_info=[]#liste qui contiendra le contenu de chaque colonne pour chaque ligne (numéro de la ligne, base, collocatif, trait compositionnel, phrase entière)
set_vecteur=set()#set vide où l'on placera les bases et collocatifs en un seul exemplaire, afin d'obtenir le vecteur de chacun.
cpt=2
for ligne in tableau:
	numero_ligne_phrase=cpt #compteur de la ligne sur laquelle se trouve la phrase
	decoupage=ligne.split('\t')
	base = decoupage[0]
	genre_base = decoupage[1]
	nb_base = decoupage[2]
	collocatif = decoupage[3]
	genre_colloc= decoupage[4]
	nb_colloc= decoupage[5]
	lemme_colloc=decoupage[6]
	trait_compositionnel = decoupage[7]
	phrase = decoupage[8]
	
	if collocatif not in set_vecteur:#condition si le collocatif n'est pas dans le set, on l'ajoute
		set_vecteur.add(collocatif)
	if base not in set_vecteur:#condition si la base n'est pas dans le set, on l'ajoute
		set_vecteur.add(base)
	liste_info.append([numero_ligne_phrase,base,genre_base,collocatif,trait_compositionnel,phrase])#ajout du contenu des colonnes dans la liste vide liste_info
	cpt+=1

vectors = {}#dictionnaire qui contiendra clé=nom du vecteur, valeur=le vecteur entier
tokens = set_vecteur #on utilise le set rempli précédemment pour obtenir le nom de tous les vecteurs que l'on souhaite comparer dans le gros fichier de vecteurs
with open("cc.fr.300.vec", encoding="utf8") as f:#boucle qui compare les vecteurs du set à ceux du fichier de vecteurs
	for line in f:
		token, *vec = line.split()
		if token in tokens:
			vectors[token] = [float(x) for x in vec]

for ln in liste_info:#boucle qui parcourt la liste créée précédemment avec toutes les informations de chaque ligne
	num_phrase=ln[0]#numéro de la phrase
	tok_base=ln[1]#base
	base_genre=ln[2]
	tok_colloc=ln[3]#collocatif
	trait_compo=ln[4]#compositionnalité oui/non
	phrase_entiere=ln[5]#phrase entière
	vec_base=vectors[tok_base]#vecteur de la base
	vec_colloc=vectors[tok_colloc]#vecteur du collocatif
	
	
	#écriture dans le fichier de sortie sous la forme : numéro de la phrase, trait compositionnel, token de la base, vecteur de la base, token du collocatif, vecteur du collocatif, phrase entière. Séparés par des tabulations.
	output.write(str(num_phrase)+"\t"+trait_compo+"\t"+ tok_base+"\t"+ base_genre + "\t"+ " ".join(map(str, vec_base))+"\t"+tok_colloc+"\t"+ " ".join(map(str,vec_colloc))+"\t"+phrase_entiere+"\n")

