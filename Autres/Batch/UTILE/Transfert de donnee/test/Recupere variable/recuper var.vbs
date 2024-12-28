dim vari, launch, fso, fichier
' var : valeur inputbox'
' launch : permet de lancer le bat
' fso : permet d'ouvrir un fichier
' f : contient information sur le fichier (lecture,ecriture)
vari = inputbox("Valeur : ", "Mon_programme.vbs")
' Permet décrire la variable "var" dans un fichier (temp.txt)'
Const ForReading = 1, ForWriting = 2
Set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
Set fichier = fso.OpenTextFile("\temp.txt", ForWriting,true)
fichier.write("" &vari)
fichier.close()
set launch = CreateObject("WScript.Shell")
launch.run "test.bat"
