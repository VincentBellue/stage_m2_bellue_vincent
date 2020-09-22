import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import argparse

usage = """<documentation>"""
parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input", type = str, help="Chemin vers le fichier en input(fichier tsv)")
parser.add_argument("output", type=str, help="Chemin vers le fichier output(image .png)")
args = parser.parse_args()
fic_input = args.input
fic_output = args.output

data = pd.read_csv(fic_input,sep='\t')

fichier_split="heatmap"+" "+fic_input.split("\\")[-1]
plt.title(fichier_split)

# ~ # récupérer les noms de colonnes + mettre Unnamed à la fin
cols = data.columns[1:]
cols = cols.append(data.columns[0:1])

# ~ # Réassigner les noms
data.columns = cols

# retirer la colonne Unnamed qui ne contient que des Nan
data = data.drop("Unnamed: 0", axis=1)

heat_map = sb.heatmap(data)#création de la heatmap

labels=data.columns #on utilise les colonnes du fichier pour avoir le nom des labels (Oui/soleil/plomb)

#boucle qui servira à ne garder que les labels qui sont des multiples de 10 -> 0, 10, 20,etc
nom_de_label=[]#liste vide qui contiendra les labels qui nous intéressent
cpt=0 #init du compteur


# ~ for i in range(0,len(labels)): #parcours des labels
	# ~ if i==cpt:#si le label est égal au compteur, on l'ajoute à la liste. Ne garde que les multiples de 10, donc 1 label tous les 10.
		# ~ nom_de_label.append(labels[i])
		# ~ cpt+=10

#image en output,écart de 10 entre les valeurs affichées
# ~ plt.xticks(np.arange(len(labels),step=10),labels=nom_de_label,fontsize=8)
# ~ plt.yticks(np.arange(len(labels),step=10),labels=nom_de_label,fontsize=8)

for i in range(0,len(labels)):
	nom_de_label.append(labels[i])

#image en output,écart de 1 entre les valeurs
plt.xticks(np.arange(len(labels),step=1),labels=nom_de_label,fontsize=1)
plt.yticks(np.arange(len(labels),step=1),labels=nom_de_label,fontsize=1)

plt.savefig(fic_output,bbox_inches='tight',dpi=700)

