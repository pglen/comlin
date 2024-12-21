BEGIN	    { done = 0 ;}
   	    	{ mm =	match($0, var)
			if(mm == 0) 
				{
				mmm = match($0, "localhost ")
				if(mmm == 0)
					{
					printf("%s\n", $0); 
					}
				}
			else 
				{
                done = 1
				#printf("match: '%s'\n", $0); 
		 		printf("%s %s %s.localdomain\n", var, host, host); 
		 		#printf("match: %s '%s'\n", substr($0, length(var) + mm)); 
				}
		    } 
END		    { 
            if(done == 0)
                {
                printf("%s %s %s.localdomain\n", var, host, host); 
                }		 		
            }

