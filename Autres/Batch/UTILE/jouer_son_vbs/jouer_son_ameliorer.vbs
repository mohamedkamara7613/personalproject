Dim Chemin
Call AskQuestion()
'*****************************************************************************
Sub Play(URL)
    Dim Sound
    Set Sound = CreateObject("WMPlayer.OCX")
    Sound.URL = URL
    Sound.settings.volume = 100
    Sound.Controls.play
    do while Sound.currentmedia.duration = 0
        wscript.sleep 100
    loop
    wscript.sleep (int(Sound.currentmedia.duration)+1)*1000
End Sub
Sub AskQuestion()
    Dim Question,MsgFR
    MsgFR = "Voulez-vous ouvrir un fichier audio?" & vbcr & "Oui = Pour écouter" & vbcr & "Non = Pour arrêter" & vbcr & String(50,"*")
   Question = MsgBox(MsgFR,vbYesNO+vbQuestion+vbSystemModal,Title)
    If Question = VbYes Then
   Call chercher()'chercher le fichier audio
   Call Play (Chemin)'jouer
    End If
    If Question = VbYes Then
        MsgBox  "Il y a une autre instance en cours d'exécution !"
       WScript.Quit()
    End If
    If Question = VbNo  Then
        Call Kill("wscript.exe")
    End If
    If Question = VbNo  Then
        Call Kill("wscript.exe")
    End If
End Sub
'*****************************************************************************
'Fonction pour ajouter les doubles quotes dans une variable
Function DblQuote(Str)
    DblQuote = Chr(34) & Str & Chr(34)
End Function
'******************************************************************************
Function CommandLineLike(ProcessPath)
    ProcessPath = Replace(ProcessPath, "\", "\\")
    CommandLineLike = "'%" & ProcessPath & "%'"
End Function
'******************************************************************************
Sub Kill(MyProcess)
    Dim Titre,colItems,objItem,Processus,Question
    Titre = " Processus "& DblQuote(MyProcess) &" en cours d'exécution "
    Set colItems = GetObject("winmgmts:").ExecQuery("Select * from Win32_Process " _
    & "Where Name like '%"& MyProcess &"%' AND commandline like " & CommandLineLike(WScript.ScriptFullName) & "",,48)
    For Each objItem in colItems
        objItem.Terminate(0)' Tuer ce processus
    Next
End Sub
'******************************************************************************
Sub chercher()
sIniDir = "C:\Windows\*"
sFilter = "Fichier MP3 (*.mp3)|*mp3|Fichier Wave(*.wav)|*wav|Fichier WMA(*.wma)|*wma|"
sTitle = "GetFileDlg by omen999 2014 - http://omen999.developpez.com"
rep = GetFileDlgEx(Replace(sIniDir,"\","\\"),sFilter,sTitle)
Chemin=rep & vbcrlf & Len(rep)
Chemin= left(Chemin , len(Chemin)-2)
'Chemin=InputBox("Copiez pour mettre le chemin dans le presse-papier", "Chercher chemin fichier", Chemin)
End Sub
Function GetFileDlgEx(sIniDir,sFilter,sTitle)
  Set oDlg = CreateObject("WScript.Shell").Exec("mshta.exe ""about:<object id=d classid=clsid:3050f4e1-98b5-11cf-bb82-00aa00bdce0b></object><script>moveTo(0,-9999);eval(new ActiveXObject('Scripting.FileSystemObject').GetStandardStream(0).Read("&Len(sIniDir)+Len(sFilter)+Len(sTitle)+41&"));function window.onload(){var p=/[^\0]*/;new ActiveXObject('Scripting.FileSystemObject').GetStandardStream(1).Write(p.exec(d.object.openfiledlg(iniDir,null,filter,title)));close();}</script><hta:application showintaskbar=no />""")
  oDlg.StdIn.Write "var iniDir='" & sIniDir & "';var filter='" & sFilter & "';var title='" & sTitle & "';"
  GetFileDlgEx = oDlg.StdOut.ReadAll
End Function
