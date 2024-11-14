#!/bin/bash
echo " Introduceti nr:"
read numar 

if [ $numar -gt 0 ]; then
    echo "Pozitiv"
elif [ $numar -lt 0 ]; then 
    echo "Negativ"
else
    echo "Zero"
fi