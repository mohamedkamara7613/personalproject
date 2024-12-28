@echo off
for /r C:\ %%X in (*.mp3) do (echo %%X >> C:\listeMP3.txt)
pause