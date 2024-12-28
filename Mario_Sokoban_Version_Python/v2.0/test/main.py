
import pickle

nivaux = {0:"111111111111131000000011100000020111100110110010111110110010114200000300110111110110110111110110110110100010114000011000111111111111111111111111"}

with open("level", 'wb') as file:
	record = pickle.Pickler(file)
	record.dump(nivaux)


with open("level", "rb") as file:
	get_record = pickle.Unpickler(file)
	niveaux = get_record.load()


print(niveaux)