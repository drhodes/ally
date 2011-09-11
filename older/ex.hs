{-
  `Filter is a function that takes a 
  predicate and a list.  Each element of the
  list is tested against the predicate and if
  true is returned, the element is kept, else 
  it's discarded.`;
-}


filter f xs = 
    where 
      init = xs
      accum = list

      init > head |= list
                  |> f +> append <> accum > |= id.2
                                            |> return
 
      init > tail |= list 
                  |> id.1 > init 
                  |> |= emptyP 
                     |+> id.2 
                     |-> id.1
}

