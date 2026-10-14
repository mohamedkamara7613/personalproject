Commençons la reflexion maintenant qu'on a les elements. Une discussion avec le prof m'a indiquer de comparer deux corrections possible, l'un en appliquant unematrice de rotation au donnée de l'accélération, l'angle trouvé grace au magnetometre mais moi je pense que le gyroscope suffirait car j'ai remarqué un fichier dans le repo qu'il me semble vient de L'IMU :
mkamara@mkamara-Inspiron-15-3520:~/Bureau/repos/pi_itineraire_26_28/code/Code_fusion$ cat data.csv 
Timestamp,Accel X,Accel Y,Accel Z,Gyro X,Gyro Y,Gyro Z
1778687728.431044,1.022299,0.0046359999999999995,0.06893,0.0,-0.22750000000000004,-0.17500000000000002

et qu'il y a des données gyro, je ne sais pas encore ce que ça represnte reellement.
Mais aussi toujours dans la premiere methode, initialiser les valeurs d'integrations notament vitesse initial en se basant sur la trame nmea qui fourni des vitesses en plus de la position.
Et sans parler de l'utilisation de HTOP ou HDOP je ne sais plus les termes, c'est un truc a explorer.

Ensuite l'autre methode qui consiste a appliquer EKF(je ne maitrise pas encore ), et j'avais vu quelque part qu'on pouvait ne pas calculer la jacobienne qu'il y aurait une methode plus simple toujours dans EKF.(on fera cette partie mm si j'ai missionner quelqu'un pour travailler dessus comme ça on comparera)


Ensuite il faudra absolument tester, il ne me reste plus bcp de temps.
Penses tu qu'il faut refaire des acquisitions ou bien les donnees IMU et GPS vont suffirent pour notre travail ?