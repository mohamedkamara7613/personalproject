#conding:utf-8


class TableauNoir():
	"""
		Classe définissant un tableau sur lequel on peut écrire et effacer par jeux de methodes.
		L'attribut modifié est surface
	"""

	def __init__(self):
		self.surface = ""

	def ecrire(self, message_a_ecrire):
		if self.surface != "":
			self.surface += "\n"
		self.surface += "{}".format(message_a_ecrire) 

	def afficher_tab(self):
		print(self.surface)


tab = TableauNoir()
tab.ecrire("Je fait un test d'écriture")
tab.ecrire("Normalement la le test a resssssssssbuggggggggggggggggggg")
tab.afficher_tab()
