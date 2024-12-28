::execute le script vbs de maniere asynchrone dans la mm fenetre
@echo off
pushd %~dp0
start /b "" cscript test.vbs
echo.
echo je fais un test
pause
