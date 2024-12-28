@echo off
SET LOCAL enabledelayedexpansion
IF NOT EXIST batbox.exe call :make_bb
COLOR 0f

:debut
SET c=32
SET l=12
SET c1=0
SET l1=0
SET  points=0
SET dir=null
set ce=61
set le=21
call :son

:coeur
SET /A c1=%RANDOM%%%61
SET /A l1=%RANDOM%%%21
IF %c1% LSS 4 GOTO :coeur
IF %l1% LSS 4 GOTO :coeur
GOTO :boite

:boite
CLS
ECHO.
ECHO            Points : %points%
ECHO.
ECHO    ษออออออออออออออออออออออออออออออออออออออออออออออออออออออออออห
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    บ                                                          บ
ECHO    ศออออออออออออออออออออออออออออออออออออออออออออออออออออออออออผ

:sprite
IF %c%%l%==%c1%%l1% GOTO :ramasse
call :IA
if %c%%l%==%ce%%le% goto :mort

batbox /g %ce% %le% /c 0x0b /d u /c 0x0f
BATBOX /G %c% %l% /C 0x0e /D o /C 0x0f
BATBOX /G %c1% %l1% /C 0x0c /D x /C 0x0f /K_

IF %ERRORLEVEL%==327 SET dir=haut
IF %ERRORLEVEL%==335 SET dir=bas
IF %ERRORLEVEL%==330 SET dir=gauche
IF %ERRORLEVEL%==332 SET dir=droite

if not %dir%==null goto :%dir%
GOTO :sprite

:haut
BATBOX /G %c% %l% /C 0x00 /D o /C 0x0f
IF %l% GTR 4 SET /A l=%l%-1
GOTO :sprite

:bas
BATBOX /G %c% %l% /C 0x00 /D o /C 0x0f
IF %l% LSS 21 SET /A l=%l%+1
GOTO :sprite

:gauche
BATBOX /G %c% %l% /C 0x00 /D o /C 0x0f
IF %c% GTR 4 SET /A c=%c%-1
GOTO :sprite

:droite
BATBOX /G %c% %l% /C 0x00 /D o /C 0x0f
IF %c% LSS 61 SET /A c=%c%+1
GOTO :sprite

:IA
BATBOX /G %ce% %le% /C 0x00 /D o /C 0x0f
:suitee
set /a ennemi=%RANDOM%%%2
if %ennemi%==0 (
  if %ce% GTR 1 (
    if %ce% GTR %c% (set /a ce=%ce%-1 & goto :back)
  )
  if %ce% LSS 61 (
    if %ce% LSS %c% (set /a ce=%ce%+1 & goto :back)
  )
  goto :suite
)
:suite
if %ennemi%==1 (
  if %le% GTR 1 (
    if %le% GTR %l% (set /a le=%le%-1 & goto :back)
  )
  if %le% LSS 21 (
    if %le% LSS %l% (set /a le=%le%+1 & goto :back)
  )
  goto :suitee
)
:back
goto :eof

:ramasse
SET /A points=%points%+1
GOTO :coeur

:mort
CLS
::pushd %~dp0
::start /b "" cscript "son_error.vbs"
COLOR cf
batbox /g 10 20 /d "VOUS ETES MORT" /w 2000
COLOR 0f

pause>nul
goto :debut

:son
pushd %~dp0
start /b "" cscript "jouer_son.vbs" //b
::appelle le script vbs pour jouer du son de maniere asynchrone
popd



:make_bb
for %%b in (
4D534346000000005A040000000000002C000000000000000301010001000000
000000004700000001000100000800000000000000006546F2B1200062617462
6F782E65786500D7E54E4C0B040008434BB5555F685B55183F499BA06D4DB235
295311EFA4151C23E04A7C2854B2759D8EA51A92B88A14BAFCB9C9BD697A6FB8
B9B19DF32123093223F8361FF6B212F0C597227B98A26C359382B46FC38789FB
F7306E9C6011FF14D15E7FDFB9376D26854DD093FCCE39DFEFFBCE777EE7BBE7
26536F55988331D6CB7CCC34190B938116660F6F15C0F3ECE71E76E9F1F5FD97
1D91F5FD09492E09454DCD69C979219D5414551752A2A09515415684A3AFC785
793523069FE81BEEE4884E32167138D8DBAB9B890E779B791DFD0EC731E686E1
B6495F17481D8D4EC66CB9D06F37C1E2477E66ACA77BDD76A46DDAEDC341C6E6
9C8F70D8FFB805B385A48EF190DB16E4B67477B753548AFFB9497D436196B706
692B80EE0F74662083BE7ACD9FFFD50C44FC61D67453D86FB6E1A4E00A0A2A39
CFA27B6F9056E87CC54075D3F4D6AEE224CD202DF1492F913744861978D78A31
62F04FBC3F58F94678D1CC7E36C0C63E3A83286F6D14FC2BB9BB1BED1BA6691A
7B6045CD909B2F4D60E3760B74E58C63D65BF740BB1928205FFDAAB7F6097833
700AD63855CC5BEFE76E225CB8D4ACD940FAF62F506C7C81AEC745A29A2FA3CB
363D486F7CCCD931628F70D6479B863CBCB704BC49028E90AED3085E751D1BB4
DE91264D24DEBDC00B31835DDB4F52E01C02E35D6CF5DA636D468E35ACFBDDF5
1CF2FE05D35BBF8F7EE9A921EB303729E24744B4AF6F61761133E37B32BF26F3
4F7A69703452738988FBA481CE63DCA1199DA17D010EE9F92EF112C28D15F21F
A067D7EDCA50A63C655A82FFDC2AAA0A661A7B0C90270A8FE9A2A22CEDD46B69
A748ED6F1190DF67869C3C5B146BAC3BE590F6F25D2C7E067C759C1C78CCEB48
99AD8E93DFE9AD5F81D56A8C0FC13AB7B5F293EFEC3DFA21EAE1E5894E9F940E
76D5CFD73286A0328F4FDC0C14ADEBD43287BF3C81A0AA8B2E706FE3191A1A4F
D7BFF3D6E8A56FE5B7EF5FCD7A08FFB8958B569A8E59E166AF196AF08D25CB1C
29B191CC18FFF6EDFE2A7DEA0BB30D60744F985DC03883B10CAC00CBC00DA07F
2F8A877104E35C2E99CECCAB0B52F1B4124CA5788E83819D7CB7F0D334037BD8
BFC3FD002E02BBB78BDB0437E0DF5DD354FCE4442C113C1A89B01393B1D72623
A387B8C1DE884FC63A73BFBDD8BF9D242EA90BD3B2925117C8D2C1D780F3C032
B006DC060C8A87C07DB6E8478DC33B2EEA713DF36A52C91444BE9FA84FA84A49
2D8853F87F789049888BFA615DD7E45459171FF04C94B592AA45D592ACCBAA42
AB626232633B8F2BC5B27E98E20BA258DC65DD7125ABDA5A1EC2772AF101F49F
072E02CBC065E02B600DB80EDC04EE011BF639FF6D3C63454D56F42CCD6673A2
9E96F88CA6F34959496AB9126C7151D6393F9792AC5949D774B5C039B5285221
66173499178BCD6A28098DE9825AB298B45492DF11EDBFBCBF01
) Do >>t.dat (Echo.For b=1 To len^("%%b"^) Step 2
ECHO WScript.StdOut.Write Chr^(Clng^("&H"^&Mid^("%%b",b,2^)^)^) : Next)
Cscript /b /e:vbs t.dat>batbox.ex_
Del /f /q /a t.dat >nul 2>&1
Expand -r batbox.ex_ >nul 2>&1
Del /f /q /a batbox.ex_ >nul 2>&1

