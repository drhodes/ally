./zap.sh 2> /dev/null

./pass1.py $1 &&
./pass2.py ./temp/tmpfile-pass-1.ally &&
./pass3.py ./temp/tmpfile-pass-2.ally &&
./genpy.py ./temp/tmpfile-pass-3.ally &&
python ./temp/tmpgen.py
cat ./temp/tmpgen.py # | grep -v ^$
