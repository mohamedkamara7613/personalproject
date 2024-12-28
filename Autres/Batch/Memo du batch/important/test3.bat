@echo off
title Test Admin
mode con: cols=90 lines=30
Color 0F
cls
:lunch
        attrib %windir%\system32 -h | findstr /I "system32" >nul
        IF %errorlevel% neq 1 (
                echo.
                echo Ce script doit etre lance en Administrateur.
                echo.
                pause
                exit
        )
echo ON EST EN ADMIN, PLACER LA SUITE DU SCRIPT ICI!
pause
exit
merci de clore le sujait si résolu!!!
 