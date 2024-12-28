::execute le script de maniere synchrone dans la mm fenetre
::Marche aussi mais pas a tous les coups
@echo off
::%WINDIR%\SysWOW64\cmd.exe
cscript test.vbs
echo Je fais un test
set /p nom=Vous pouvez me donner votre nom si vous voulez :
pause
