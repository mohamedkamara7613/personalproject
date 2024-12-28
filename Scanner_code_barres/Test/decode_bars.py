

# Table de correspondance EAN-13 : exemple simplifié pour les parités normales et inversées
EAN13_L_CODES = {
    (3, 2, 1, 1): '0', (2, 2, 2, 1): '1', (2, 1, 2, 2): '2', (1, 4, 1, 1): '3',
    (1, 1, 3, 2): '4', (1, 2, 3, 1): '5', (1, 1, 1, 4): '6', (1, 3, 1, 2): '7',
    (1, 2, 1, 3): '8', (3, 1, 1, 2): '9'
}

EAN13_R_CODES = {  # Codes en miroir pour la partie droite
    (1, 1, 2, 3): '0', (1, 2, 2, 2): '1', (2, 2, 1, 2): '2', (1, 1, 4, 1): '3',
    (2, 3, 1, 1): '4', (1, 3, 2, 1): '5', (4, 1, 1, 1): '6', (2, 1, 3, 1): '7',
    (3, 1, 2, 1): '8', (2, 1, 1, 3): '9'
}



def detect_ean13_guards(widths):
    # Localiser la première séquence 1-1-1 (début)
    start_index = None
    for i in range(len(widths) - 2):
        if widths[i:i + 3] == [1, 1, 1]:
            start_index = i
            break

    # Localiser la dernière séquence 1-1-1 (fin)
    end_index = None
    for i in range(len(widths) - 3, 1, -1):
        if widths[i:i + 3] == [1, 1, 1]:
            end_index = i + 3
            break

    # Vérifier que les indices ont été trouvés et la validité de la zone middle_guard
    if start_index is None or end_index is None:
        print("Séquences de garde de début ou de fin non trouvées.")
        return None, None

    # Extraire la zone sans les gardes de début et de fin
    code_zone = widths[start_index:end_index]

    # Vérifier la présence de la séquence de garde centrale
    middle_guard_index = None
    for i in range(20, len(code_zone) - 20):  # Ajustement pour éviter les bords
        if code_zone[i:i + 5] == [1, 1, 1, 1, 1]:
            middle_guard_index = i
            break

    if middle_guard_index is None:
        print("Séquence de garde centrale non trouvée.")
        return None, None

    # Renvoyer les segments gauche et droit
    left_part = code_zone[3:middle_guard_index]
    right_part = code_zone[middle_guard_index + 5:]
    return left_part, right_part



def decode_ean13_barcode(widths):
    # Séparer les parties gauche et droite en validant les gardes
    left_part, right_part = detect_ean13_guards(widths)
    if left_part is None or right_part is None:
        return "Erreur : séquences de garde non valides"

    # Processus de décodage avec les tables de référence EAN-13
    def decode_section(part, codes_table):
        digits = []
        for i in range(0, len(part), 4):  # Extrait les groupes de 4 valeurs
            segment = tuple(part[i:i + 4])
            digit = codes_table.get(segment)
            if digit is not None:
                digits.append(digit)
            else:
                print(f"Motif inconnu : {segment}")
                return None
        return digits

    left_digits = decode_section(left_part, EAN13_L_CODES)
    right_digits = decode_section(right_part, EAN13_R_CODES)

    if left_digits and right_digits:
        return ''.join(left_digits + right_digits)
    else:
        return "Erreur de décodage"

# Exemple
bar_widths = [29, 1, 1, 1, 3, 2, 1, 1, 3, 2, 1, 1, 1, 1, 2, 3, 1, 1, 2, 3, 1, 1, 2, 3, 4, 2, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 3, 2, 1, 1, 3, 2, 1, 1, 4, 2, 1, 1, 3, 2, 1, 1, 1, 3, 1, 2, 1, 1, 1, 13, 7]
decoded_value = decode_ean13_barcode(bar_widths)
print("Code-barres décodé :", decoded_value)
