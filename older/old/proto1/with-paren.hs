
data Token = Operator String
           | Primitive String
           | Open
           | Close
             deriving (Show, Eq, Ord)

data Term = Group [Term]
          | Termite Token         
          | Term [Term]
            deriving (Show, Eq, Ord)

tokenate _ "(" = Open
tokenate _ ")" = Close
tokenate ops x = if x `elem` ops
                 then Operator x
                 else Primitive x

tokenize ops xs = map (tokenate ops) (words xs)
 
program = "( 12 + 32 ) * 31 -> Int"

cluster :: [Token] -> [Term]
cluster (Open:ts) = Term (cluster ts)
cluster (Close:ts) = (cluster ts)


cluster [] = []

main = do
  {
  ; let ops = ["*", "+", "->"]
  ; let tokes = tokenize ops program    
  ; print $ cluster tokes

  ; print "OK"
  }