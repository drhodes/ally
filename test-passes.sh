./pass1.py $1 &&
./pass2.py ./temp/tmpfile-pass-1.ally &&
./pass3.py ./temp/tmpfile-pass-2.ally &&
cat ./temp/tmpfile-pass-3.ally | grep -v ^$
