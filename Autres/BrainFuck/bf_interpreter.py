
# NON FONCTIONNEL POUR L'INSTANT

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

file = sys.argv[1]
if not os.path.isfile(file):
    print(f"Erreur : Le fichier '{file}' n'existe pas.")
    sys.exit(1)

try:
    with open(file, 'r') as f:
        content = f.read()
except Exception as e:
    print(f"Erreur lors de la lecture du fichier : {e}")
    sys.exit(1)

input_data = input("Entrez les données nécessaires au programme Brainfuck (si requis) : ")

def brainfuck_interpreter(raw_code, input_data="", debug=False):
    # Filtrer le code pour ne conserver que les caractères valides
    valid_commands = "><+-.,[]"
    code = "".join(c for c in raw_code if c in valid_commands)

    tape = [0] * 30000  # Bande mémoire
    pointer = 0  # Pointeur
    input_pointer = 0
    code_pointer = 0
    output = ""
    brackets = []
    
    # Préparer les sauts pour les boucles []
    loop_map = {}
    for i, c in enumerate(code):
        if c == "[":
            brackets.append(i)
        elif c == "]":
            start = brackets.pop()
            loop_map[start] = i
            loop_map[i] = start
    
    while code_pointer < len(code):
        command = code[code_pointer]
        if command == ">":
            pointer += 1
        elif command == "<":
            pointer -= 1
        elif command == "+":
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == "-":
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == ".":
            output += chr(tape[pointer])
        elif command == ",":
            if input_pointer < len(input_data):
                tape[pointer] = ord(input_data[input_pointer])
                input_pointer += 1
            else:
                tape[pointer] = 0
        elif command == "[" and tape[pointer] == 0:
            code_pointer = loop_map[code_pointer]
        elif command == "]" and tape[pointer] != 0:
            code_pointer = loop_map[code_pointer]
        if debug:
            print(f"Tape: {tape[:10]}, Pointer: {pointer}, Command: {command}")
        code_pointer += 1
    return output

print(brainfuck_interpreter(content, input_data))
