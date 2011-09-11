import Ally
import Text.Parsec


test1 f str = print $ parse f "" str

main = do 
  {

  ; test1 let_stat "let a = 5;"
  ; test1 arrow_stat "a > 5;";
  ; test1 arrow_stat "a => 5;"
  ; test1 arrow_stat "asdfa >> asdf ;"
  ; test1 arrow_stat "a > 5 > 5 <> ert ;"

  --; test1 function "id a { let a = c; b => return; a <> b; }"
  
  ; ex1 <- readFile "ex1.ally"
  ; test1 program ex1
  ; let (Right prg) = parse program "" ex1
  ; output (Program prg)

  ; print "Ok"

  
  }