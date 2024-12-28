@echo off

title Facebook
color f9
mode con cols=120 lines=30

:next
set /a amis=%random%%%1001
set /a x=%random%%%101

:debut
cls
echo.
echo -----------------@JeanKevinDu%x% vous demande en amis--------------------- Nombre d'amis : %amis% amis---------------------
echo.
echo @JeanKevinDu%x% : "Veux-tu etre mon ami"
choice /c on 
if %errorlevel%==2 goto :non
if %errorlevel%==1 goto :oui

:non
cls
echo.
echo -----------------Message de @JeanKevinDu%x%------------------------------- Nombre d'amis : %amis% amis---------------------
echo.
echo  @JeanKevinDu%x% : "Oh domage"	"Allez stp !!"
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
pause>nul
goto :debut 

:oui
set /a amis=%amis%+1
cls
echo.
echo -----------------Message de @JeanKevinDu%x%------------------------------- Nombre d'amis : %amis% amis---------------------
echo.
echo  @JeanKevinDu%x% : "Ah chouette alors"
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
pause>nul
goto :next

pause>nul
