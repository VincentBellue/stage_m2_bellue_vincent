#Exemple de fichier en input : FL_BON.tsv

import torch
from transformers import FlaubertModel, FlaubertTokenizer
import argparse

#fonction utilisée lorsque le nombre d'occurrence de la base est supérieur à 1. On cherche quelle base est la plus proche du collocatif dans la phrase (ou inversement si collocatif supérieur à 1).
#une phrase peut posséder plusieurs occurrences du collocatif OU plusieurs occurrences de la base, mais pas les deux en même temps(du moins dans mes exemples).
def base_collocatif_plus_proche(tableau_indice,id_tok,id_tok_deux,choix_base): #renvoie toujours la base en 1er, grâce au booleen choix_base
	liste=[] #liste vide qui contiendra la place des différentes bases dans la phrase(ou place des collocatifs dans un cas avec plusieurs collocatifs).
	for token in tableau_indice.keys(): #parcours des clés(numéro du token dans la phrase)
		if tableau_indice[token] == id_tok: #si l'id Flaubert du token en plusieurs exemplaires est une base on l'ajoute à la liste (pareil pour collocatif dans la condition avec plusieurs collocatifs).
			liste.append(token)
		elif tableau_indice[token] == id_tok_deux: #si l'autre token est une base ou si l'autre token est un collocatif, on le garde dans une variable.
			indice_tok_deux = token
	meilleur_indice=20 #variable qui sera mise à jour, résultat de la soustraction soustraction base - collocatif/collocatif - base selon le cas.
	meilleur_indice_tok=liste[0] # variable contenant l'emplacement de la base la plus proche du collocatif. Par défaut la meilleure est la 1ère base, remplacée si une meilleure est trouvée(pareil dans l'autre condition).
	
	for id_liste in liste: #parcours de la liste d'id (place du token dans la phrase)
		resultat= id_liste - indice_tok_deux #soustraction place de la base - place du collocatif ou collocatif - base selon la boucle.
		if resultat < 0:#si résultat négatif
			resultat = -resultat #normalisation
		if resultat < meilleur_indice: #si le résultat de la soustraction est inférieur au meilleur indice(20 de base).
			meilleur_indice=resultat #on le remplace par la nouvelle valeur. En théorie la meilleure valeur sera proche de 0.
			meilleure_place_tok=id_liste #on récupère l'indice de la meilleure base ou meilleur collocatif dans la phrase.
			meilleur_indice_tok=tableau_indice[id_liste] #on récupère aussi son id flaubert.
	if choix_base: #si choix_base est sur True
		return(meilleur_indice_tok,id_tok_deux,meilleure_place_tok, indice_tok_deux)#si base = tok1 et colloc=tok2
	else: #si choix_base est False
		return(id_tok_deux,meilleur_indice_tok,indice_tok_deux,meilleure_place_tok)#si colloc=tok1 et base=tok2

def main():
	usage = """<documentation>"""
	parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("input", type = str, help="Path to input tsv file")
	parser.add_argument("output", type=str, help="Path to output")
	args = parser.parse_args()
	fic_input = args.input #fichier input
	fic_output = args.output#fichier output
	
	tableau=open(fic_input,'r',encoding='utf8')
	next(tableau) #ignore la 1ère ligne du tableau
	output=open(fic_output,'w',encoding='utf8')
	output.write("Ligne" + "\t" + "Compositionnel" + "\t" "Base" + "\t" + "Genre base" + "\t" + "Vecteur base" + "\t" + "Collocatif" + "\t" + "Vecteur collocatif" + "\t" + "Phrase" + "\n")#entête des colonnes du fichier en output

	#chargement de flaubert
	model_id = "flaubert-base-cased"
	tokenizer = FlaubertTokenizer.from_pretrained(model_id, do_lower_case=False)
	flaubert = FlaubertModel.from_pretrained(model_id)
	flaubert.eval()
	
	#parcours du fichier
	cpt=2 #compteur pour savoir de quelle phrase il s'agit dans le fichier. 1ère phrase = ligne 2 dans le fichier en input.
	for ligne in tableau:
		numero_ligne_phrase=cpt #compteur de la ligne sur laquelle se trouve la phrase
		decoupage=ligne.split('\t') #découpage des colonnes à la tabulation
		base = decoupage[0]
		genre_base = decoupage[1]
		nb_base = decoupage[2]
		collocatif = decoupage[3]
		genre_colloc= decoupage[4]
		nb_colloc= decoupage[5]
		lemme_colloc=decoupage[6]
		trait_compositionnel = decoupage[7]
		phrase = decoupage[8]
		
		#tokenisation avec Flaubert
		id_base = tokenizer.encode(base)[1] #id de la base (id du milieu car entouré par "1" et "1")
		id_collocatif = tokenizer.encode(collocatif)[1]#id du collocatif (id du milieu car entouré par "1" et "1")
		id_phrase = tokenizer.encode(phrase) #id dans le vocabulaire de flaubert des tokens de la phrase
		
		tableau_indice={}#dictionnaire avec les indices des tokens pour CHAQUE phrase. clé = numéro du token dans la phrase, valeur = id dans le vocabulaire de flaubert
		nb_occurrences={} #dictionnaire avec les occurrences pour CHAQUE phrase. clé = id dans le vocabulaire de flaubert, valeur = nombre d'occurrence
		
		#utilisation de pytorch et flaubert sur chaque phrase
		token_ids = torch.tensor([id_phrase]) #création d'une matrice pour chaque phrase
		contextual_vectors = flaubert(token_ids)[0] #calcule des vecteurs contextuels
		contextual_vectors = contextual_vectors.squeeze(0) #On enlève la première dimension
		recovered_tokens = tokenizer.convert_ids_to_tokens(id_phrase)#tokens reconstitués(parfois des bouts de tokens, parfois des tokens entiers
		
		#parcours token par token dans les phrases pour compter le nombre d'occurrence
		for i in range(0,len(id_phrase)-1):
			id_token=id_phrase[i]
			tableau_indice[i] = id_token
			if id_token in nb_occurrences: 
				nb_occurrences[id_token] += 1
			else:
				nb_occurrences[id_token] = 1
		
		#cas où il n'y a qu'une occurrence de la base et du collocatif
		if nb_occurrences[id_base] ==1 and nb_occurrences[id_collocatif] ==1:
			resultat_colloc = id_collocatif
			resultat_base = id_base
			for tok in tableau_indice.keys():
				if tableau_indice[tok] == id_base:
					place_tok_un = tok
				elif tableau_indice[tok] == id_collocatif:
					place_tok_deux = tok
		
		#cas où une base apparait plusieurs fois dans une phrase
		elif nb_occurrences[id_base] >1: #si la base apparait plus d'une fois par phrase
			resultat_base,resultat_colloc,place_tok_un,place_tok_deux = base_collocatif_plus_proche(tableau_indice,id_base,id_collocatif,True)#resultat_base contiendra id_base, et resultat_colloc contiendra id_collocatif
		#cas où un collocatif apparait plusieurs fois
		elif nb_occurrences[id_collocatif] >1: #si le collocatif apparait plus d'une fois par phrase
			resultat_base,resultat_colloc,place_tok_un,place_tok_deux = base_collocatif_plus_proche(tableau_indice,id_collocatif,id_base,False) #resultat_base contiendra id_collocatif, et resultat_colloc contiendra id_base
		for i in range(0,len(recovered_tokens)-1):
			if i == place_tok_un: #si le token lu est égal à la base/collocatif de la phrase
				# ~ tok_un = recovered_tokens[i] #token 1 avec découpage de Flaubert
				vecteur_tok_un=contextual_vectors[i] #on récupère le vecteur du token lu
				tok_lu_un = base
			if i == place_tok_deux: #si le token lu est égal à la base/collocatif de la phrase
				# ~ tok_deux = recovered_tokens[i] #token 2 avec découpage Flaubert
				vecteur_tok_deux=contextual_vectors[i] #on récupère le vecteur du token lu
				tok_lu_deux = collocatif
		#écriture du numéro de la ligne, token1, vecteur token1, token2, vecteur token2 et phrase entière
		output.write(str(numero_ligne_phrase) + "\t" + trait_compositionnel + "\t" + tok_lu_un + "\t" +genre_base +"\t" + " ".join(map(str, vecteur_tok_un.numpy()))+ "\t" + tok_lu_deux + "\t" + " ".join(map(str, vecteur_tok_deux.numpy())) + "\t" + phrase + "\n")
		cpt+=1
	
	output.close()

if __name__ == "__main__":
	with torch.no_grad(): # dire à pytorch que l'on n'a pas besoin de calculer le gradient pour ces calculs
		main()
