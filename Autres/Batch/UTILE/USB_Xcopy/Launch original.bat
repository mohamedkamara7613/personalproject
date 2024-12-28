@ECHO OFF
REM  QBFC Project Options Begin
REM  HasVersionInfo: No
REM  Companyname: Waked xy
REM  Productname: USB COPY 
REM  Filedescription:Permet de copier toutes les  données d'un ordinateur sur un peripherique de stockage externe 
REM  Copyrights: 
REM  Trademarks: 
REM  Originalname: 
REM  Comments: 
REM  Productversion: 1.0
REM  Fileversion:  0. 0. 0. 0
REM  Internalname: 
REM  Appicon: 
REM  AdministratorManifest: No
REM  QBFC Project Options End
@ECHO ON
﻿@ECHO OFF 
color a 
echo assign letter=x noerr >> %temp%\driveletter.txt
::Necessite l'autorisation administrative
diskpart /s %temp%\driveletter.txt
del /s %temp%\driveletter.txt
xcopy C:"Users\%username%\nom de fichier a copier" \BD /e/y
pause
exit