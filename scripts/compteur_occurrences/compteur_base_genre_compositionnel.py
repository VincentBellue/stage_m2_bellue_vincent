#Exemple de fichier à utiliser en input "FL_MAGN_BON_CLASSE.tsv"

import argparse
usage = """<documentation>"""
parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input", type = str, help="Chemin vers le fichier en input(fichier tsv). exemple : FL_MAGN_BON_CLASSE.tsv")
parser.add_argument("output", type=str, help="Chemin vers le fichier output(fichier tsv)")
args = parser.parse_args()
fic_input = args.input
fic_output = args.output

tableau_de_vecteur=open(fic_input,'r',encoding='utf8')#fichier input
next(tableau_de_vecteur)
output=open(fic_output,'w',encoding='utf8')
output.write("Lemme du collocatif"+"\t"+"Compositionnel"+"\t"+"Genre de la base"+"\t"+"Occurrences de la base"+"\n")#1ère ligne du fichier

#Ce script permet de créer un compteur pour chaque lemme et un compteur global en prenant en compte le lemme, le genre et le trait compositionnel


#1ère partie du script qui permet de compter le nombre d'occurrences sous la forme :('lemme du collocatif', 'Trait compositionnel', 'genre'): nombre_d'occurrences -> ('sain', 'Non', 'féminin'): 10,('sain', 'Oui', 'féminin'): 10
frequence={}#dictionnaire où seront stockés les tuples
for ligne in tableau_de_vecteur:
	split=ligne.split("\t")
	base=split[0]#nom de la base
	genre_base=split[1]#genre de la base
	lemme=split[6]#lemme du collocatif
	compo=split[7]#trait compositionnel
	lemme_compo_genre=(lemme,compo,genre_base)#tuple avec les 3 éléments
	if lemme_compo_genre in frequence:#si le tuple est présent dans {frequence} 
		frequence[lemme_compo_genre]+=1#on ajoute +1 à sa frequence
	else: 
		frequence[lemme_compo_genre]=1#sinon on le crée et sa fréquence=1

occ_globale={}#dictionnaire qui contiendra le nombre d'occurrences globales. ex: {('féminin', 'Non'): 67, ('féminin', 'Oui'): 103}
liste_nom=[]#liste qui contiendra le nom de tous les lemmes. ex: ['sain', 'fin', 'brillant']. Sert

#2ème partie du script qui permet de compter pour CHAQUE lemme de collocatif (sain, fin, profond, etc) le nombre d'occurrences de féminin-trait_compo_non, féminin-trait_compo_oui, masculin-trait_compo_non, masculin-trait_compo_non de la BASE.
#les occurrences sont donc séparées par nom de lemme de collocatif. Si un lemme de collocatif apparait 40 fois (au lieu de 20 généralement) le compte sera sur 40 au lieu de 20.
for elem in frequence:
	colloc=elem[0]#on récupère le lemme de collocatif dans le dictionnaire. ex: sain
	compositionnel=elem[1]#trait compositionnel(Oui/Non)
	genre=elem[2]#genre de la base
	compte=frequence[elem]#nombre d'occurrence
	genre_et_compo=(genre,compositionnel)#tuple genre de la base et trait compositionnel. ex : ('féminin', 'Non') ou ('féminin', 'Oui') ou autre à chaque passage de la boucle.
	#on commence à écrire lemme par lemme
	if colloc not in liste_nom:#si le lemme n'est pas encore dans la liste
		output.write("\n"+colloc+"\t"+compositionnel+"\t"+genre+"\t"+str(compte)+"\n")#on crée une nouvelle ligne
		liste_nom.append(colloc)# et on ajoute le lemme à la liste
	elif colloc in liste_nom:#sinon si le lemme est déja dans la liste
		output.write(colloc+"\t"+compositionnel+"\t"+genre+"\t"+str(compte)+"\n")#on écrit dans l'output : lemme	trait compo	genre	nombre d'occurrences	retour à la ligne
	#on ajoute ensuite chaque occurrences de chaque lemme dans le dictionnaire des occurrences globales qui seront écrits dans la prochaine partie du script
	if genre_et_compo not in occ_globale:#si genre_et_compo n'est pas encore dans le dictionnaire d'occurrences globales
		occ_globale[genre_et_compo]=compte#on le crée et le compte du 1er collocatif sera sa valeur.
	elif genre_et_compo in occ_globale:#s'il est déja présent
		occ_globale[genre_et_compo]+=compte#on additionne

#cette partie permet de parcourir {occ_globale} qui contient le nombre d'occurrences globales et d'écrire dans le fichier output (voir plus haut pour connaitre sous quelle forme sont écrits les clés et valeurs)
output.write("\n"+"Décompte Total"+"\t"+"Compositionnel"+"\t"+"Genre de la base"+"\t"+"Occurrences de la base"+"\n")#1ère ligne pour l'écriture du compteur global
for occurrence in sorted(occ_globale):#parcours du dictionnaire
	genre_base=occurrence[0]#on récupère le genre de la base(féminin/masculin)
	trait_compo_base=occurrence[1]#le trait compositionnel (Oui/Non)
	occurrence_globale=occ_globale[occurrence]#le nombre d'occurrences
	output.write("\t"+trait_compo_base+"\t"+genre_base+"\t"+str(occurrence_globale)+"\n")#écriture dans l'output
