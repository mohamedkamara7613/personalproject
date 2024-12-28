@echo off
title Numero mystere
mode con cols=70 lines=30
color 9f
:next
set  myster=%RANDOM%
if %myster% GTR 1000 goto :next
if %myster% LSS 1 goto :next

:debut
cls
color 9f
echo.
echo 	Bienvenu dans le jeu du nombre mystere
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 0 et 1000) : 

if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo

:inferieur
cls
color cf
echo.
echo 		Le nombre mystere est plus petit
echo.
echo     `////////////////////////////////////////.     
echo     //......................................:+     
echo     //......................................:o     
echo     //......................................:o     
echo     //...://////////:...://///////////......:o     
echo     //...oooooo+:+oos/::.           `.o:....:o     
echo     //...oooooo/.:ooo             `:::s/-...:o     
echo     //...oooooooooooo                 `o:...:o     
echo     //...oooooooooooo              .:::s/-..:o     
echo     //...oooooooooooo                 `:o-..:o     
echo     //...oooooooooooo               ---/o:..:o     
echo     //...oooooooooooo`              ```.o:..:o     
echo     //...+ooooooooooo++`               `o/-.:o     
echo     //.....----------.-o`   :o++++++++++:-..:o     
echo     //.................//   -o:.............:o     
echo     //.................-o   `s:.............:o     
echo     //..................o   -o:.............:o     
echo     //..................+/:++:-.............:o     
echo     //....................---...............:o     
echo     //......................................:+     
echo     `////////////////////////////////////////.     
echo.
echo 	Appuyez sur entrer pour retenter votre chance
pause>nul
goto :debut

:superieur
cls
color cf
echo.
echo 		Le nombre mystere est plus grand
echo.
echo     `////////////////////////////////////////.     
echo     //......................................:+     
echo     //......................................:o     
echo     //......................................:o     
echo     //...://////////:...://///////////......:o     
echo     //...oooooo+:+oos/::.           `.o:....:o     
echo     //...oooooo/.:ooo             `:::s/-...:o     
echo     //...oooooooooooo                 `o:...:o     
echo     //...oooooooooooo              .:::s/-..:o     
echo     //...oooooooooooo                 `:o-..:o     
echo     //...oooooooooooo               ---/o:..:o     
echo     //...oooooooooooo`              ```.o:..:o     
echo     //...+ooooooooooo++`               `o/-.:o     
echo     //.....----------.-o`   :o++++++++++:-..:o     
echo     //.................//   -o:.............:o     
echo     //.................-o   `s:.............:o     
echo     //..................o   -o:.............:o     
echo     //..................+/:++:-.............:o     
echo     //....................---...............:o     
echo     //......................................:+     
echo     `////////////////////////////////////////.     
echo.
echo 	Appuyez sur entrer pour retenter votre chance
pause>nul
goto :debut

:bingo
cls
color a1
echo.
echo Bravo !! Bravo !!Bravo !!Bravo !!Bravo !!Bravo !!Bravo
echo.
echo     .////////////////////////////////////////`      
echo     o:``````````````````````````````````````// 
echo     o-``````````````````````````````````````// 
echo     o-``````````````````////.```````````````// 
echo     o-`````````````````.o  `+/.`````````````// 
echo     o-`````````````````-+   .s-`````````````// 
echo     o-`````````````````/:   :o-`````````````// 
echo     o-````````````````.o`   ++:--------.````//
echo     o-```/++++++++++--+.    `..........:+.``//
echo     o-```yoooooooooso-                 `s:.`//
echo     o-```yooooooooos/              `:::o+-.`//
echo     o-```yooooooooos/                  /+-``//
echo     o-```yooooooooos/              -::/s:.``//
echo     o-```yooooooooos/                 `s:.``//
echo     o-```yooooo+:+os/             `::/o/-.``//
echo     o-```yooooo/-/os+--`             `s:.```//
echo     o-```+oooooooooo+:://////////////+/-.```//
echo     o-`````...........```..............`````//
echo     o-``````````````````````````````````````//
echo     o:``````````````````````````````````````//
echo     .////////////////////////////////////////`
echo.
echo 	Tapez : 1.Rejouer 2.Quitter
choice /c 12 /n
if %errorlevel% == 2 exit
if %errorlevel% == 1 goto :next 

pause>nul
