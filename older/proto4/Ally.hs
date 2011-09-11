{-# OPTIONS_GHC -XNoMonomorphismRestriction #-}

module Ally where

import Text.Parsec.Char
import Text.Parsec.String
import Text.Parsec

lit_double_arrow = try $ string ">>"
lit_single_arrow = string ">"
lit_both_arrow = string "<>"
lit_id_arrow = try $ string "=>"
lit_left_stache = string "{"
lit_right_stache = string "}"
lit_let = string "let"
lit_semi = string ";"
lit_return = string "return"
lit_mac = string "mac"

arrow = try lit_double_arrow <|>
        try lit_single_arrow <|>
        try lit_both_arrow <|>
        try lit_id_arrow        

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ident = many1 $ oneOf $ "1234567890!@#$%^&*()._+-=?/|:" ++ letters

-----------------------------------------------------------------------------
data ArrowStat = ArrowStat [(Ident, Arrow)] Ident deriving Show

data Ident = Ident String 
           | ArgName String
           | AnonIdent
             deriving Show

data Arrow = DoubleArr
           | SingleArr
           | BothArr
           | IdArr
           | UnknownArrow
             deriving (Show)

arr_construct ">>" = DoubleArr
arr_construct ">" = SingleArr
arr_construct "<>" = BothArr
arr_construct "=>" = IdArr
arr_construct _ = UnknownArrow

arrow_pair = do idt <- ident
                spaces
                arr <- try arrow
                spaces
                return (Ident idt, arr_construct arr)

arrow_stat = do pairs <- many1 (try arrow_pair)
                spaces
                end <- ident
                spaces
                string ";"
                return $ ArrowStat pairs (Ident end)
                   
-----------------------------------------------------------------------------
data Macro = Macro [String] String deriving Show

some_idents = many $ do { x <- ident
                        ; spaces
                        ; return x
                        }

macro = do lit_mac
           spaces
           idents <- some_idents
           spaces
           lit_left_stache
           spaces
           body <- manyTill anyChar $ string "}"
           spaces
           return $ Macs (Macro idents body)

-----------------------------------------------------------------------------
data LetStat = LetStat String String deriving Show
let_stat = do lit_let
              spaces
              var <- ident
              spaces
              try $ string "="                     
              spaces
              val <- ident
              spaces
              string ";"
              return $ LetStat var val

-----------------------------------------------------------------------------
data Function = Function Ident [Ident] [LetStat] [ArrowStat]
                deriving (Show)

function = do 
  {
  ; func_name <- ident
  ; spaces
  ; args <- many $ do { 
                   ; x <- ident
                   ; spaces
                   ; return x
                   }            

  ; spaces
  ; string "{"
  ; spaces
  ; lets <- many $ do { 
                   ; a_let <- let_stat
                   ; spaces
                   ; return $ a_let
                   }
  
  ; arrows <- many1 $ do { 
                      ; arr <- arrow_stat
                      ; spaces
                      ; return $ arr
                      }
              
  ; string "}"
  ; spaces
  ; return $ Funs $ Function (Ident func_name) (map ArgName args) lets arrows
  }      
         
data Program = Program [Program]
             | Macs Macro
             | Funs Function
             | NoProg
               deriving (Show)

program = many $ try function <|> try macro 
             

---------------------------------------------------------------
output_prog (Macs (Macro name body)) = do
  {
  ; print "Macro ___________________________________________"
  ; print name
  ; print body
  ; return ()
  }

output_prog (Funs (Function name args lets arrs)) = do
  { 
  ; print "Function _____________________________________"
  ; print name
  ; print args
  ; print lets
  ; print arrs
  ; return ()
  }

output (Program ps) = do
  {
  ; mapM_ output_prog ps
  }
   
                        
                
           
