#!/bin/bash
#donne le nom de la machine
var=machine
machine=$(hostname)
echo "Ma machine courante est : " ${!var}