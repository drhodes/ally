#lang racket
(require racket/class)

(module asdf 
  (define place%
    (class object% (super-new)
      (init-field val)
      
      
      ))
  
  (define (place val)
    (new place% [val val]))

  );;end module


