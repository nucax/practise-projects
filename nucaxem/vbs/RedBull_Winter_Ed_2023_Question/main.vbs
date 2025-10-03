Dim answer
answer = MsgBox("Do you like Red Bull Winter Edition 2023?", vbYesNo + vbQuestion, "https://github.com/nucax")

If answer = vbYes Then
    CreateObject("Wscript.Shell").Run "python yes.py"
Else
    CreateObject("Wscript.Shell").Run "python no.py"
End If
