Dim WshShell Set WshShell = WScript.CreateObject("WScript.Shell" ) variable = InputBox("Entrer une valeur !") Monfichier = "C:\Users\myaccount\Desktop\test.bat " & variable WshShell.Run Monfichier
