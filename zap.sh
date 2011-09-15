find ./ | grep "~$" | xargs trash
find ./ | grep ".pyc" | xargs trash 
rm -f ./temp/tmpfile*