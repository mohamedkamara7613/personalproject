@echo off

echo Entrez un nombre
set /p nomb1=
echo Entrez un autre nombre
set /p nomb2=
set /a result= %nomb1% + %nomb2%
echo La somme de ces deux nombres est egale a  %result%
echo ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
echo Entrez votre age 
set /p age=
if %age% geq 18 echo Vous vous etes mageur 
if %age% lss 18 echo Vous vous etes mineur 

pause>nul
