@echo off
pushd %~dp0
echo %~dp0
cscript "C:\Users\USER\Desktop\Programmation\Langage batch\AUTRE\Transfert de donnee\test\vbs\test.vbs"
popd
cls
set /p nom= Quelle est votre nom ?
color fc
pause>nul
