@echo off
mode con cols=40 lines=21
title Score Save
color 07
echo.
echo.
echo      浜様様様様様様様様様様様様様融
echo      �                            �
echo      �                            �
echo      �                            �
echo      �                            �
echo      �                            �
echo      �                            �
echo      �                            �
echo      �    敖陳陳陳陳陳陳陳陳朕    �
echo      �    �                  �    �
echo      �    青陳陳陳陳陳陳陳陳潰    �
echo      �                            �
echo      �                            �
echo      �                            �
echo      �                            �
echo      �                            �
echo      藩様様様様様様様様様様様様様夕
batbox /g 9 5 /c 0x07 /d "Enregistrer votre score" /g 9 7 /c 0x07 /d "    au " /c 0x03 /d "pseudo" /c 0x07 /d " de ..    " /g 9 15 /c 0x0E /d "    Score :" /c 0x07 /d " 0" /g 12 11 /c 0x03
set /p "lettre="
echo 0/%lettre%>>Score.txt
exit
