@echo off
::Afficher le tableau contenant des information sur un processus
tasklist /FI "IMAGENAME eq explorer.exe"
::avoir le PID d'un processus
for /f "tokens=2 delims= " %%i in ('tasklist ^| findstr /i /c:"explorer"') do echo %%i
pause>nul
::Creer une tache planfier
schtasks /create /ru user /rp Password /sc hourly -mo 1 /ST 23:00:00 /TR "C:\chemin\du\batch.bat" /TN NomDeLaTache
::Pour arrêter le système via la ligne de commande ou dans un fichier batch, on utilise la commande shutdown. Voici la syntaxe de cette commande :
::Shutdown -s -t xx -c "Message"
::xx : nombre de seconde à attendre avant l'arrêt de l'ordinateur (0 : pour un arrêt immédiat)
::Message : un message qui accompagne l'opération
::Pour redémarrer remplacer -s par -r.
::Pour fermer la session remplacer -s par -l.
::Et pour annuler une des opérations précédentes, utilisez shutdown -a (avant l'expiration du délai défini par -t).
::Mettre en veille prologé
::rundll32.exe powrprof.dll,SetSuspendState
