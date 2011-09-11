import Text.XML.Light
data Node = Node { chdrn :: [Element]
                 , line :: String
                 }

data Loc = Loc String
           deriving (Show, Eq)

data AllyT = Comment Loc
           | Rawstring Loc String
           | Literal Loc 
           | Symbol Loc
           | Typedec Loc
           | Dot Loc
           | Tfi Loc
           | Ift Loc
           | Iff Loc
           | Ffi Loc
           | Dub Loc
           | Ls Loc
           | Rs Loc
           | Fwd Loc
           | Bak Loc
           | Ptfi Loc
           | Pift Loc
           | Piff Loc
           | Pffi Loc
           | Pdub Loc
           | Pls Loc
           | Prs Loc
           | Pfwd Loc
           | Pbak Loc
           | Pipeq Loc

           | Arr Loc
           | Arrow Loc
           | Ident Loc
           | Assign Loc
           | Place Loc
           | Expression Loc
           | Declaration Loc
           | Statement Loc
           | Block Loc [AllyT]
           | ParameterList Loc [Maybe AllyT]
           | Function Loc AllyT AllyT AllyT
           | Mod Loc
           | NullT
             deriving (Show, Eq)

node_name = qName . elName
node_children n = elChildren n
node_line_no = attrVal . head . elAttribs

node_new n = Node (node_children n) 

main = do {
       ; txt <- readFile "../tmp.xml"
       ; let nodes = parseXML txt
       --; print nodes
       ; let c1 = head $ onlyElems nodes 
       --; print c1
       ; print $ node_name c1      
       ; print $ length $ node_children c1
       ; let ch = head $ node_children c1
       ; print $ node_children ch
       ; print ch
       ; let tmp = case node_name c1 of
                     "mod" -> Mod (Loc $ node_line_no c1)
                     _ -> NullT
       ; print tmp

       ; print "OK"
       }