Version=13.004
Length unit CNC=mm
Feed unit CNC=mm_min
File extension=nc
External postprocessor=
Use arcs=Y
I/J relative=Y
Program start=
[>>>]
(Projet <project>)
(Créé avec Estlcam <build>)
(Durée de fonctionnement env. <time> heures)

(Outils nécessaires :)
<tools>

G90
G91.1
M03 S<s><!L>
[<<<]
Program end=
[>>>]


M05
M30
[<<<]
Operation start=(N° <order> <op> : <name>)
Tool change=
[>>>]
M05
M06 T<t> (<n>)
M03 S<s><!L>
[<<<]
Laser before down=
All tools before down=N
Laser after down=
[>>>]
M03 S<s>
G04 P<t_pierce_ms>
[<<<]
All tools after down=N
Laser before up=M05
All tools before up=N
Laser after up=
All tools after up=N
Mist coolant on=M08
Mist coolant off=M09
Flood coolant on=M10
Flood coolant off=M11
Name X=X
Format X=
Order X=2
Scale X=1
Enable X=Y
Repeat X=N
Name Y=Y
Format Y=
Order Y=3
Scale Y=1
Enable Y=Y
Repeat Y=N
Name Z=Z
Format Z=
Order Z=4
Scale Z=1
Enable Z=Y
Repeat Z=N
Name I=I
Format I=
Order I=5
Scale I=1
Enable I=Y
Repeat I=Y
Name J=J
Format J=
Order J=6
Scale J=1
Enable J=Y
Repeat J=Y
Name F=F
Format F=
Order F=7
Scale F=1
Enable F=Y
Repeat F=N
Name S=S
Format S=
Order S=8
Scale S=1
Enable S=Y
Repeat S=N
Name N=
Format N=
Order N=1
Scale N=1
Enable N=N
Repeat N=N
Plot axis Z=N
Up Z=
Down Z=
Rapid feed XY=
Rapid feed Z=
Initial value N=1
Command rapid move=G00
Command linear move=G01
Command clockwise arc=G02
Command counterclockwise arc=G03
Command order=1
Command repeat=Y
Encoder=ASCII
Delimiter= 
Decimal point=.
Line end=
Character replacements=
[>>>]
Ä|Ae
Ö|Oe
Ü|Ue
ä|ae
ö|oe
ü|ue
ß|ss
[<<<]
Lock units=N
Special formatter=Off
EOL=1521_CD6B_6785_EB75
