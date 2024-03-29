(module square 
  // all these functions do the same thing.
  (def square6 (x) 
	   return mul (x, x)
	   )
	  
  (def square7 (x) 
	   return < mul < (x, x))
	   
  
  (def square1(x) 
	   (x, x) > mul > return
	   )
	   
  	  
  (def square3(x, asdf)
	   |= mul
	   |< (x, x)
	   |> return
	   )
	   
  
  (def square4(x)
	   (return < |= mul
			     |< x ; first arg to mul
				 |< x ; second arg to mul			 
				 )
	   )
  
  (def square5(x)
	   ;; every function gets compiled down to something
	   ;; that looks like this.
	   (var x1 = x)
	   (var x2 = x)
	   (x1 > mul)
    x2 > mul;
    mul > return;		
  }
}

