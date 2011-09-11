import Data.Ord
import Data.List

data Token = Operator String
           | Primitive String
           | Grouper String
             deriving (Show, Eq, Ord)
                     
tokenate grp ops x = if x `elem` ops
                     then Operator x
                     else if x `elem` grp
                          then Grouper x
                          else Primitive x

tokenize grp ops xs = map (tokenate grp ops) (words xs)

--(* (+ (+ 12 34) 56) 78) 
program = "( 23 * ( 12 + 34 * 101 * 345 ) + 56 ) * 78"

data Term = Lop { lop_name :: String
                , lop_prec :: Int                         
                , lop_val :: Term 
                , lop_id :: Int
                } 

          | Rop { rop_name :: String
                , rop_prec :: Int                         
                , rop_val :: Term 
                , rop_id :: Int
                }

          | Binop { binop_name :: String
                  , binop_prec :: Double
                  , binop_lval :: Term
                  , binop_rval :: Term 
                  , binop_id :: Int
                  } 

          | Termite String Int 
          | Term [Term] Int
          | Empty
            deriving (Show, Eq, Ord)

cluster_ depth idz (t:[]) = [case t of
                               (Primitive s) -> Termite s idz
                               (Operator "+") -> Binop "+" (2 * depth) Empty Empty idz
                               (Operator "*") -> Binop "*" (4 * depth) Empty Empty idz
                               (Operator "->") -> Binop "->" (1 * depth) Empty Empty idz]

cluster_ depth idz ((Grouper "("):ts) = cluster_ (depth * 100) idz ts
cluster_ depth idz ((Grouper ")"):ts) = cluster_ (depth / 100) idz ts
cluster_ depth idz (t:ts) = result ++ (cluster_ depth (idz+1) ts)
    where result = cluster_ depth idz [t]
                                                                 
cluster tokens = cluster_ 1 1 tokens

isBinop (Binop _ _ _ _ _) = True
isBinop _ = False
            
getMaxOp ts = if (binop_prec max_binop) == -1
              then Nothing
              else Just $ binop_id max_binop
    where 
      max_binop = maximumBy (comparing binop_prec) (filter isBinop ts)

absorbTerms cluster = if target == 0
                      then Nothing 
                      else Just (pre2 ++ [newTerm] ++ postrest)
    where
      target = case getMaxOp cluster of
                 Nothing -> 0                
                 (Just x) -> x

      pre1 = takeWhile (\x -> if isBinop x then (binop_id x) /= target else True) cluster
      lval = last pre1
      pre2 = take ((length pre1) -1) pre1
      
      rest = dropWhile (\x -> if isBinop x then (binop_id x) /= target else True) cluster
             
      maxProc = head $ rest 
      rval = head (drop 1 rest)
      postrest = drop 2 rest
      newTerm = Binop (binop_name maxProc) (-1) lval rval (binop_id maxProc)                

reduce ::  [Term] -> Term
reduce [] = Empty
reduce cluster = case absorbTerms cluster of
                   Nothing -> head cluster
                   (Just absorbtion) -> reduce absorbtion

pretty_ level (Termite s _) = " " ++ s ++ " "
pretty_ level (Binop n _ lval rval _) = name ++ left ++ right
    where 
      name = " (" ++ n 
      left = (pretty_ (level + 1) lval)
      right = (pretty_ (level + 1) rval) ++ ")"

{-
      space1 = take level (repeat ' ')
      space2 = space1 ++ " "
      name = space1 ++ n ++ "\n"
      left = space2 ++ (pretty_ (level + 1) lval) ++ "\n"
      right = space2 ++ (pretty_ (level + 1) rval)
-}

pretty = pretty_ 0 

main = do
  {

  ; 
  ; let ops = ["*", "+", "->"]
  ; let grp = ["(", ")"]              
  ; let tokes = tokenize grp ops program    
  ; let clust = cluster tokes
  --; print clust
  ; putStr $ pretty (reduce clust)
{- 
  ; let (Just clust2) = absorbTerms clust
  --; print $ absorbTerms clust2

  ; let (Just clust3) = absorbTerms clust2
  ; print $ absorbTerms clust3

  ; let (Just clust4) = absorbTerms clust3
  --; print $ absorbTerms clust4

  --  ; print clust3
 -}
  --; print "OK"
  }

