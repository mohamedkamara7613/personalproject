Dim WshShell, Monfichier
Set WshShell = WScript.CreateObject("WScript.Shell" )
variable = InputBox("Entrer une valeur !")
Monfichier = "variable_vbs.bat " & variable
WshShell.Run Monfichier
