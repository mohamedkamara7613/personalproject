@echo off
for /f "tokens=2 delims= " %%i in ('tasklist ^| findstr /i /c:"explorer"') do echo %%i
pause>nul