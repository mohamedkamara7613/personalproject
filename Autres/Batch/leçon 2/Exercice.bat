@echo off
rem ______________________________________________________________________________________________________________________

:next
set /a amis=%random%%%1001
set /a x=%random%%%101

rem ______________________________________________________________________________________________________________________

:debut
cls
echo --------------------@JeanKevinDu%x% vous demande en amis--------------------
echo Nombres d'amis de JeanKevinDu%x% : %amis% amis
echo.
echo Bonjour veux-tu etre mon ami?
choice /c on 
if %errorlevel%==2 goto :non
if %errorlevel%==1 goto :oui

:non
cls
echo.
echo Domage alors!!
echo Nombres d'amis de JeanKevinDu%x% : %amis% amis
pause>nul
goto :debut

:oui
cls
echo Vous allez etre amis avec JeanKevinDu%x% dans quelques instant
timeout /t 5 /nobreak
set /a amis=%amis%+1
echo.
echo Oh chouette alors j'ai un ami en plus  !!!
echo Nombres d'amis de JeanKevinDu%x% : %amis% amis
pause>nul
goto :next

rem ______________________________________________________________________________________________________________________
pause>nul