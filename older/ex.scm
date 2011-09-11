;(MODULE "module")
;(symbol "ex3")


(define (function name paralist blk))


(function
 (symbol "filter")
 (parameterlist
  (symbol "f")
  (symbol "xs"))
 (block
  (statement
   (declaration
    (typedec "var")
    (symbol "init")
    (symbol "xs")))
  (statement
   (declaration
    (typedec "var")
    (symbol "accum")
    (symbol "list")))
  (statement
   (expression
    (expr1
     (place
      (ident
       (symbol "init")))
     (arrow ">"))
    (expr2
     (place
      (ident
       (symbol "head")))
     (pipe "|")
     (arrow "="))
    (expr2
     (place
      (ident
       (symbol "list")))
     (pipe "|")
     (arrow ">"))
    (expr1
     (place
      (ident
       (symbol "f")))
     (arrow "+>"))
    (expr1
     (place
      (ident
       (symbol "append")))
     (arrow "<>"))
    (expr1
     (place
      (ident
       (symbol "accum")))
     (arrow ">"))
    (expr1
     (place
      (pipe "|"))
     (arrow "="))
    (expr2
     (place
      (ident
       (symbol "id")
       (dot ".")
       (symbol "2")))
     (pipe "|")
     (arrow ">"))
    (place
     (ident
      (symbol "return")))))
  (statement
   (expression
    (expr1
     (place
      (ident
       (symbol "init")))
     (arrow ">"))
    (expr2
     (place
      (ident
       (symbol "tail")))
     (pipe "|")
     (arrow "="))
    (expr2
     (place
      (ident
       (symbol "list")))
     (pipe "|")
     (arrow ">"))
    (expr1
     (place
      (ident
       (symbol "id")
       (dot ".")
       (symbol "1")))
     (arrow ">"))
    (expr2
     (place
      (ident
       (symbol "init")))
     (pipe "|")
     (arrow ">"))
    (expr1
     (place
      (pipe "|"))
     (arrow "="))
    (expr2
     (place
      (ident
       (symbol "emptyP")))
     (pipe "|")
     (arrow "+>"))
    (expr2
     (place
      (ident
       (symbol "id")
       (dot ".")
       (symbol "2")))
     (pipe "|")
     (arrow "->"))
    (place
     (ident
      (symbol "id")
      (dot ".")
      (symbol "1"))))))))