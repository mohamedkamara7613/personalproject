@echo off
cls
color 0a
set letter_disk = D
set /p letter_disk = "Entrez la lettre de votre disque : "
cd %letter_disk%:\
md Report
echo ..........................Voici les noms de wifi..............................
netsh wlan show profile
set /p wifiname = "Entrez le nom de votre wifi : "
cls
echo  Appyez sur une touche pour valider
pause>nul
echo ..........................Travail en cours..............................

netsh wlan show profile>Report\nomwifiall.txt
ipconfig>Report\IPconfig.txt
echo -IP : OK
ipconfig /all>Report\IPconfigAll.txt
echo -all IP : OK
hostname>Report\hostname.txt
echo -hostname : OK
netsh wlan show profile %wifiname% key=clear>Report\WifiPassword.txt
echo -wifi password : OK
net accounts>Report\netaccounts.txt
echo -windows accounts : OK
ver>Report\versionWindows.txt
echo -version de windows : OK
systeminfo>Report\systeminfo.txt
echo -information de system : OK
tree>Report\Tree.txt
echo arbre d'organisation system : Ok
net view>Report\netview.txt
echo ..........................FIN DE TRAVAIL..............................
pause>nul


