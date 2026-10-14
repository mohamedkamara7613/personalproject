TRANSLIT_MAP = {
    # ------------------------------
    # Déjà présents chez toi (je garde)
    "kh": "kh", "x": "kh",
    "ḥ": "h", "ḥ": "h",
    "q": "k", "k": "k", "g": "k",           # g → k très fréquent en maghrébin
    "j": "j", "dj": "j",
    "th": "t", "dh": "d",
    "sh": "ch", "š": "ch", "ch": "ch",
    "gh": "r",                               # choix maghrébin très courant
    "‘": "", "’": "", "'": "", "ʿ": "",
    "aa": "a", "â": "a", "ā": "a",
    "ee": "i", "ii": "i", "î": "i", "ī": "i",
    "oo": "u", "ou": "u", "uu": "u", "û": "u", "ū": "u",
    "é": "e", "è": "e", "ê": "e", "ë": "e",

    # ------------------------------

    # Variantes fréquentes de translittération (surtout maghrébine/française)
    "ç": "s",       # ç parfois utilisé pour ص ou س
    "ss": "s",      # très fréquent (Hassan → Hassane / Hassoun)
    "ll": "l",
    "nn": "n",
    "mm": "m",
    "rr": "r",
    "tt": "t",
    "dd": "d",
    "bb": "b",
    "ff": "f",
    "pp": "b",      # parfois p → b
    "kk": "k", "cc": "k",   # cc pour ق ou ك parfois

    # Autres digrammes / variantes classiques
    "ou": "u",      # déjà là mais on renforce
    "w": "ou",      # w → ou très fréquent (Wahid → Ouaïd)
    "y": "i",       # parfois y final → i (karim → karime)
    "ى": "a", "ي": "i",     # quand même caractère apparaît
    "ة": "a", "h": "a",     # ta marbuta souvent a ou h ou e

    # Sons "lourds" parfois simplifiés encore plus (surtout oral/France)
    "ṣ": "s", "ṣ": "s",
    "ḍ": "d", "ḍ": "d",
    "ṭ": "t", "ṭ": "t",
    "ẓ": "z", "ẓ": "z",
}