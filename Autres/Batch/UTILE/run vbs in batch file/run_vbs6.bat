::Execute le script vbs de maniere synchrone dans la meme fenetre
::C'est la methode la plus recommandé car elle se fait sur une seule ligne
@call cscript "%~dp0test.vbs"
echo je fais un test
pause
::Si ça ne marche pas esseyer ->
::@%WINDIR%\SysWOW64\cmd.exe/c all cscript "%~dp0test.vbs"
::Si vous avez besoin de la fenêtre de rester, vous pouvez remplacer/c avec/k
