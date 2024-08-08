@echo off
cls
Set Sleep=0
:start
if %Sleep% == 100 ( goto end )
python3 pubsub.py pubsub-384921 publish stocks
echo This is a loop
Set /A Sleep+=1
echo %Sleep%
goto start
:end
echo "am 30 now"
pause