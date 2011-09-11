rm -f Ally.o Ally.hi test.o test
ghc --make test.hs
rm -f Ally.o Ally.hi test.o test.hi 
echo
echo ---------------------------------------------
./test