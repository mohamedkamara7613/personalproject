Set Sound = CreateObject("WMPlayer.OCX.7")
Sound.URL = "C:\Users\USER\Desktop\sons\Boom.wav"
Sound.Controls.play
do while Sound.currentmedia.duration = 0
wscript.sleep 100
loop
wscript.sleep (int(Sound.currentmedia.duration)+1)*1000
