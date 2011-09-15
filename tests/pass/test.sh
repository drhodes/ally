for file in $(ls | grep .ally$); do 
	../../parser.py $file > /dev/null 2> /dev/null 
	if [ "$?" -ne 0 ]; then
		echo fail: $file;
	else 
		echo pass: $file 
	fi
done;
