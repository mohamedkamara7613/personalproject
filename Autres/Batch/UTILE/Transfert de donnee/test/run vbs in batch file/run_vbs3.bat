::exucute un script vbs de maniere synchrone dans une nouvelle fenetre
@echo off
pushd %~dp0
start /wait "" cmd /c cscript test.vbs
echo je fais un test
pause
