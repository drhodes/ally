#lang racket
(require racket/class)

;;------------------------------------------------------------------
(define symbol%   
  (class object% (super-new)               
    (init-field pos)
    (init-field name)               
        
    (define/public (get-pos) pos)
    (define/public (get-name) name)
    (define/public (emit) name )
    
    ))

(define (symbol pos name)
  (new symbol% [pos pos] [name name]))


;;------------------------------------------------------------------
(define typedec%   
  (class object% (super-new)               
    (init-field line)
    (init-field kind)               
        
    (define/public (get-line) line)
    (define/public (get-kind) kind)))

(define (typedec line kind)
  (new typedec% [line line] [kind kind]))

;;------------------------------------------------------------------
(define function%   
  (class object% (super-new)
    (init-field blk)
    (init-field line)
    (init-field params)
    (init-field sym)           
    (define/public (get-blk) blk)
    (define/public (get-line) line)
    (define/public (get-params) params)
    (define/public (get-sym) sym)
    (define/public (emit mod-name)
      (display (format "fun")))
))
    
(define (function line sym params blk)
  (new function% [line line] [sym sym] [params params] [blk blk]))

;;------------------------------------------------------------------
(define parameterlist%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)
    
    (init-field syms)
    (define/public (get-syms) syms)))
    
(define (parameterlist line . syms)
  (new parameterlist% [line line] [syms syms]))


;;------------------------------------------------------------------
(define block%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)

    (init-field stmts)
    (define/public (get-stmts) stmts)))
        
(define (block line . stmts)
  (new block% [line line] [stmts stmts]))

;;------------------------------------------------------------------
(define expression%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)

    (init-field exps)
    (define/public (get-exps) exps)))
        
(define (expression line . exps)
  (new expression% [line line] [exps exps]))

;;------------------------------------------------------------------
(define statement%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)

    (init-field exps)
    (define/public (get-exps) exps)))
        
(define (statement line . exps)
  (new statement% [line line] [exps exps]))

;;------------------------------------------------------------------
(define declaration%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)

    (init-field tdec)
    (define/public (get-tdec) tdec)
    
    (init-field sym)
    (define/public (get-sym) sym)
    
    (init-field val)
    (define/public (get-val) val)))
    
        
(define (declaration line tdec sym val)
  (new declaration%
       [line line]
       [tdec tdec]
       [sym sym]
       [val val]       
       ))


;;------------------------------------------------------------------
(define expr1%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)

    (init-field exps)
    (define/public (get-exps) exps)))
        
(define (expr1 line . exps)
  (new expr1% [line line] [exps exps]))


;;------------------------------------------------------------------
(define expr2%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)
    (init-field plc)
    (define/public (get-plc) plc)
    
    (init-field pip)
    (define/public (get-pip) pip)
    
    (init-field arr)
    (define/public (get-arr) arr)))
    
    
    
(define (expr2 line plc pip arr)
  (new expr2%
       [line line]
       [plc plc]
       [pip pip]
       [arr arr]
       ))


;;------------------------------------------------------------------
(define pipe%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)))
        
(define (pipe line . char)
  (new pipe% [line line]))

;;------------------------------------------------------------------
(define place%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)
    (init-field idnt)
    (define/public (get-idnt) idnt)    
    ))

(define (place line idnt)
  (new place% [line line] [idnt idnt]))

;;------------------------------------------------------------------
(define ident%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)
    (init-field sym)
    (define/public (get-sym) sym)    
    ))

(define (ident line sym)
  (new ident% [line line] [sym sym]))

;;------------------------------------------------------------------
(define arrow%   
  (class object% (super-new)
    (init-field line)
    (define/public (get-line) line)
    (init-field char)
    (define/public (get-char) char)    
    ))

(define (arrow line char)
  (new arrow% [line line] [char char]))

;;------------------------------------------------------------------
(define mod%   
  (class object% (super-new)
    (init-field funcs)
    (init-field line)
    (init-field sym)
    
    (define/public (get-funcs) funcs)
    (define/public (get-line) line)
    (define/public (get-sym) sym)    
    
    (define/public (emit)
      (let ([name (send sym emit)]            
            )(display (format "# ~a\n" name))
             (map (lambda (x) (send x emit name)) funcs)))          
    ))
    


(define (mod line sym . funcs)
  (new mod%
       [line line]
       [sym sym]
       [funcs funcs]))

(define prog (mod ""
                  (symbol "add.ally:1" "main")
                  (function "add.ally:2"
                            (symbol "add.ally:2" "add")
                            (parameterlist "add.ally:2"
                                           (symbol "add.ally:2" "a")
                                           (symbol "add.ally:3" "b"))
                            (block "add.ally:3"
                                   (statement "add.ally:3"
                                              (declaration "add.ally:3"
                                                           (typedec "add.ally:3" "var")
                                                           (symbol "add.ally:3" "p1")
                                                           (symbol "add.ally:4" "a")))
                                   (statement "add.ally:4"
                                              (declaration "add.ally:5"
                                                           (typedec "add.ally:5" "var")
                                                           (symbol "add.ally:5" "p2")
                                                           (symbol "add.ally:5" "b")))
                                   (statement "add.ally:6"
                                              (expression "add.ally:6"
                                                          (expr1 "add.ally:6"
                                                                 (place "add.ally:6"
                                                                        (pipe "add.ally:6" "|"))
                                                                 (arrow "add.ally:6" "="))
                                                          (expr2 "add.ally:7"
                                                                 (place "add.ally:7"
                                                                        (ident "add.ally:7"
                                                                               (symbol "add.ally:7" "sum")))
                                                                 (pipe "add.ally:7" "|")
                                                                 (arrow "add.ally:8" "<"))
                                                          (expr2 "add.ally:8"
                                                                 (place "add.ally:8"
                                                                        (ident "add.ally:8"
                                                                               (symbol "add.ally:8" "a")))
                                                                 (pipe "add.ally:9" "|")
                                                                 (arrow "add.ally:9" "<"))
                                                          (expr2 "add.ally:9"
                                                                 (place "add.ally:9"
                                                                        (ident "add.ally:9"
                                                                               (symbol "add.ally:9" "b")))
                                                                 (pipe "add.ally:9" "|")
                                                                 (arrow "add.ally:9" ">"))
                                                          (place "add.ally:11"
                                                                 (ident "add.ally:11"
                                                                        (symbol "add.ally:11" "return")))))))))



(send prog emit)