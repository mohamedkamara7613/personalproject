@echo off
set local EnableDelayedExpansion
title Calculateur
mode con cols=55 lines=10
color f0

:variables
set resultat=0
set reussis=0
set levl=11
set records=0
set rec=0

:menu
cls
color f0
echo.
echo 	[1] Choix de niveau 		[2]  Quitter 
choice /c 12 /n
if %errorlevel%==2 exit
if %errorlevel%==1 goto :levlselect
goto :calcul

:levlselect 
cls
echo.
echo 		Choississez un niveau
echo.
echo 		  [1]  Entre 1 et 10 
echo.
echo 		  [2]  Entre 1 et 30 
echo.
echo 		  [3]  Entre 1 et 50 
choice /c 123 /n
if %errorlevel%==3 set levl=51
if %errorlevel%==2 set levl=31
if %errorlevel%==1 set levl=11

:calcul
::Choix des nombres de calcule et de l'operateur de maniere aléatoires
cls
set /a nbre1=%RANDOM%%%levl%
set /a nbre2=%RANDOM%%%levl%
set /a op=%RANDOM%%%3

if %op%==0 set op=+
if %op%==1 set op=-
if %op%==2 set op=*
goto :nxt
:nxt
echo.
echo.
echo.
echo.
echo 			%nbre1%%op%%nbre2%
set /a resultat=%nbre1%%op%%nbre2%
echo 					Reussis=%reussis%
set /p reponse=Entrez le resultat : 
if %reponse%==%resultat% (goto :suivant) else (goto :perdu)
goto :menu

:suivant
cls
set /a reussis=%reussis%+1
goto :calcul

:perdu
cls
color cf
if %reussis% GTR %records% (set records=%reussis% & echo %reussis%,>records.save & set /a rec=records)
echo.
echo.
echo.
echo 	Oups !! vous avez perdu, le resultat etait %resultat%
echo.
for /f "tokens=1 delims=," %%a in (records.save) do (echo Reussis : %reussis% 		Record actuel : %%a) 
set reussis=0
pause>nul
goto :menu
