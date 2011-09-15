find ./ | grep "~$" | xargs trash
find ./ | grep ".pyc" | xargs trash 
trash ./temp/tmpfile*.ally