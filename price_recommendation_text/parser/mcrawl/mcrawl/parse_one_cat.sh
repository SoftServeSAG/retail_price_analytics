#!/bin/bash

start=$1
finish=$2

counter=$start

while [ $counter -le $finish ]
do
echo $counter
scrapy runspider spiders/mercari.py -a ppc=30 -a start_cat=$counter -a finish_cat=$counter -t csv -o $counter.csv -s LOG_LEVEL=INFO

((counter++))
done

echo All done
