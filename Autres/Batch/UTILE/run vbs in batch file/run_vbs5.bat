::execute le script vbs de maniere asynchrone dans une nouvelle fenetre
@echo off
pushd %~dp0
start "" cmd /c cscript test.vbs
echo.
echo je fais un test
pause
