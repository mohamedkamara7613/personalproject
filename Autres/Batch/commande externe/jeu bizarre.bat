@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION ENABLEEXTENSIONS

CHCP 65001>NUL

TITLE THE GALACTIC GAME ^|^| By DarkBatcher - Experimental Work

CLS

CALL :Init

MODE CON: cols=80 lines=45

BATBOX /h 0
:: Some setup (ie. Declaring the variable)

SET LaunchedMissiles=0
SET MissileSide=0
SET MissileIndex=0

SET InputDelay=10

:MainLoop

SET IncrementX=0
SET IncrementY=0


BATBOX /w %InputDelay% /k_

IF %ERRORLEVEL%==335 SET IncrementY=1
IF %ERRORLEVEL%==332 SET IncrementX=1
IF %ERRORLEVEL%==327 SET IncrementY=-1
IF %ERRORLEVEL%==330 SET IncrementX=-1
IF %ERRORLEVEL%==32 (

   IF NOT DEFINED m_%MissileIndex%.x (
      CALL :InitMissile m_%MissileIndex%
   ) ELSE (
      GOTO :InputNext
   )

   SET m_%MissileIndex%.x=%SpaceShip.x%
   SET m_%MissileIndex%.y=%SpaceShip.y%

   IF %MissileSide%==1 (
      SET /A m_%MissileIndex%.x+=7
      SET MissileSide=0
   ) else (
      SET MissileSide=1
   )

   SET /A MissileIndex=^(%MissileIndex%+1^)%%3
   SET InputDelay=0
)

:InputNext

CALL :MoveMissiles

CALL :MoveObject SpaceShip %IncrementX% %IncrementY%

::IF %BB_API_RETURN%==1 GOTO :EndOfGame

GOTO :MainLoop

:MoveMissiles

IF NOT DEFINED _FirstMissile (
   SET InputDelay=10
   GOTO:EOF
)

Set _CurrentMissile=%_FirstMissile%

:MoveMissiles_Loop

IF NOT DEFINED _CurrentMissile GOTO:EOF

CALL :MoveObject %_CurrentMissile% 0 -1

SET _NextMissile=!%_CurrentMissile%.next!

if !BB_API_RETURN!==1 (

   BATBOX /O !%_CurrentMissile%.x! !%_CurrentMissile%.y! !%_CurrentMissile%.CBottom!

   set _FirstMissile=%_NextMissile%

   set %_CurrentMissile%.x=
   set %_CurrentMissile%.y=
   set %_CurrentMissile%.Height=
   set %_CurrentMissile%.Width=
   set %_CurrentMissile%.CBottom=
   set %_CurrentMissile%.CTop=
   set %_CurrentMissile%.CLeft=
   set %_CurrentMissile%.CRight=
   set %_CurrentMissile%.Sprite=
   set %_CurrentMissile%.next=

)

SET _CurrentMissile=%_NextMissile%

GOTO :MoveMissiles_Loop

:EndOfGame
ECHO.
ECHO Unfortunately, you eat somewhat not commestible

PAUSE>NUL
GOTO:EOF

:Init
SET Window.Width=80
SET Window.Height=39

SET SpaceShip.Sprite=/c 0x09 /g 0 0 /d "   /\   " /g 0 1 /d "   " /a 0x9296E2 /a 0x9196E2 /d "   " /g 0 2 /d "|\_" /a 0x9296E2 /a 0x9196E2 /d "_/|" /g 0 3 /d "\\" /a 0x9296E2 /a 0x9296E2 /a 0x9296E2 /a 0x9196E2 /a 0x9196E2 /a 0x9196E2 /d "/" /g 0 4 /c 0x0E /d " (    ) " /g 0 5 /d "  \/\/  "
SET SpaceShip.CTop=/g 3 0 /d "  "
SET SpaceShip.CBottom=/g 2 5 /d "    "
SET SpaceShip.CLeft=/g 0 2 /d " " /g 0 3 /d " "
SET SpaceShip.CRight=/g 7 2 /d " " /g 7 3 /d " "
SET SpaceShip.x=35
SET SpaceShip.y=18
SET SpaceShip.Width=7
SET SpaceShip.Height=5

BATBOX /o %SpaceShip.x% %SpaceShip.y% %SpaceShip.Sprite%

GOTO:EOF

:InitMissile

IF defined _FirstMissile (
   SET %_LastMissile%.next=%1
   SET _LastMissile=%1
) else (
   SET _FirstMissile=%1
   SET _LastMissile=%1
)

SET %1.Sprite=/c 0x0C /g 0 0 /d "|"
SET %1.CTop=/g 0 0 /d " "
SET %1.CBottom=/g 0 0 /d " "
SET %1.CLeft=/g 0 0 /d " "
SET %1.CRight=/g 0 0 /d " "
SET %1.x=-1
SET %1.y=-1
SET %1.Width=0
SET %1.Height=0

GOTO:EOF

:RegisterObject
:: A function to register an object

:MoveObject
:: A function that moves an object
:: Args :
::
:: :MoveObject Object IncrementX IncrementY
SET BB_API_RETURN=0

SET /a _TempX=!%1.x!+%2
SET /a _TempY=!%1.y!+%3

:: Should call CheckColision to check wether
:: a colision Appeared

SET /a _TempX_Left=%_TempX%+!%1.Width!
SET /a _TempY_Bottom=%_TempY%+!%1.Height!


IF %_TempX_Left% GEQ %Window.Width% goto :_MoveObjectError
IF %_TempX% LSS 0 goto :_MoveObjectError
IF %_TempY% LSS 0 goto :_MoveObjectError
IF %_TempY_Bottom% GEQ %Window.Height% goto :_MoveObjectError

if %2==1 BATBOX /o !%1.x! !%1.y! !%1.CLeft!
if %2==-1 BATBOX /o !%1.x! !%1.y! !%1.CRight!
if %3==1 BATBOX /o !%1.x! !%1.y! !%1.CTop!
if %3==-1 BATBOX /o !%1.x! !%1.y! !%1.CBottom!

BATBOX /o %_TempX% %_TempY% !%1.Sprite!

SET %1.x=%_TempX%
SET %1.y=%_TempY%

GOTO:EOF


:_MoveObjectError
SET BB_API_RETURN=1
GOTO:EOF
