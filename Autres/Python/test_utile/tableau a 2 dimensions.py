#coding:utf-8
#CREER UNE LISTE BIDIMENTIONNELLE


"""
-------------------------SA MARCHE ---------------------------
grille = []

for line in range(13):
	nvligne = []
	for col in range(13):
		nvligne.append((line, col))
	grille.append(nvligne)
grille[12][12] = "mario"
#print(grille)


i = 0
while i < 5:
	j = 0
	while j < 6:
		print("({} , {})".format(i, j))
		j += 1
	
	i += 1
"""


# -------------------------------SA AUSSI--------------------------------
line = 3
cols = 4
grille = [[0]* cols for i in range(line)]

grille[2][0] = "ndeyekebe"
print(grille)