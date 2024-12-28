@echo off
mode con cols=60 lines=20
:menu
cls
color f0
echo.
echo                     ÚÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿
echo                     ³               ³
echo                     ³    Boite 1    ³
echo                     ³               ³
echo                     ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ
echo.
echo                     ÚÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿
echo                     ³               ³
echo                     ³    Boite 2    ³
echo                     ³               ³
echo                     ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ
echo.
echo                     ÚÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿
echo                     ³               ³
echo                     ³    Boite 3    ³
echo                     ³               ³
echo                     ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ

:loop
for /f "tokens=1,2,3 delims=:" %%a in ('batbox /m') do (
	set x=%%a
	set y=%%b
	set c=%%c
)

::echo %x% %y% %c%
if %c% == 1 if %x% GTR 20 if %x% LSS 36 if %y% LSS 5 if %y% GTR 1 goto :boite1
if %c% == 2 if %x% GTR 20 if %x% LSS 36 if %y% LSS 11 if %y% GTR 7 goto :boite2
if %c% == 3 if %x% GTR 20 if %x% LSS 36 if %y% LSS 17 if %y% GTR 13 goto :boite3

goto :loop
:boite1
cls
color a0
echo.
echo Arriver a destination dans la boite 1 avec un clic simple
pause>nul
goto :menu
:boite2
cls
color cf
echo.
echo Arriver a destination dans la boite 2 avec un clic droite
pause>nul
goto :menu
:boite3
cls
echo.
color 3f
echo Arriver a destination dans la boite 3 avec un double clic
pause>nul
goto :menu

20 36
4 9 14