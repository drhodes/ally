-- builtin tests
-- builtin profiling
-- builtin refactor


data AyScope = Scope 

data AyIdentifier = String

data AyArgs = AyArgs { args_ids :: [AyIdentifier] }

data AyBlock = AyBlock

data AyStruct = AyStruct { struct_ids :: [AyIdentifier] }


data AyFunc = Func { func_name :: AyString
                   , func_args :: AyArgs
                   , func_block :: AyBlock
                   }
      
                 
    (Func
     (Identifier String)
     (Arguments [Identifier])
     
     