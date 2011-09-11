#! /usr/bin/env python

from ally import (
    LetStatement,
    ArrowStatment,
    Program
    )



print LetStatement.parseString("let 4 = 4;")
print ArrowStatment.parseString("a > a;")
print ArrowStatment.parseString("a > b <> c;")
print ArrowStatment.parseString("a => b.0 <> c;")



