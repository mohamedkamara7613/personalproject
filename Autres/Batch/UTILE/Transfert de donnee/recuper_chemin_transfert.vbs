Option explicit
dim src,dst,WshShell,Monbatch

'set WshShell = Wscript.CreateObject("WScript.Shell")
src =inputbox("Entrer le chemin de la source des fichiers a transferer : ",,"Demande de la source")
dst =inputbox("Entrer le chemin de la destination du transfert",,"Demande de la destination")
Monbatch = "Transfert.bat " & src & dst
'WshShell.Run Monbatch
