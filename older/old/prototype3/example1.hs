
{-# 
 -XMultiParamTypeClasses 
 -XFlexibleInstances
 #-}

import Prelude hiding ((.))

class Getter a b where
    (.) :: a -> a -> b


data Point = Point Int Int
	   | X
           | Y

instance Getter Point b where 
    (Point x _) . X = x
    (Point _ y) . Y = y


