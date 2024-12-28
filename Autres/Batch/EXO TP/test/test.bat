@echo off

echo choisir
choice /c AB 
if %errorlevel%==B ECHO B
if %errorlevel%==A EXIT
pause>nul
