./pass1.py $1
./pass2.py ./temp/tmpfile.ally
./pass3.py ./temp/tmpfile.ally
cat ./temp/tmpfile.ally | grep -v ^$
