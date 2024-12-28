#coding:utf-8

"""
	module où il est definit les fonctions dont je veux pas qu'ils apparaissent dans mon programme principale
"""

def initialiser_fenetre(app):
	#app.minsize(640, 480)
	# centrer la fenetre
	screen_x = app.winfo_screenwidth()
	screen_y = app.winfo_screenheight()
	window_x = 640
	window_y = 480

	pos_X = (screen_x // 2) - (window_x // 2)
	pos_Y = (screen_y // 2) - (window_y // 2)

	geo = "{}x{}+{}+{}".format(window_x, window_y, pos_X, pos_Y)

	app.geometry(geo)

