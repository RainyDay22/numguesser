
# Import the libraries inputimeout, TimeoutOccurred 
from inputimeout import inputimeout 
import time
  
# # Try block of code 
# # and handle errors 
# try: 
  
#     # Take timed input using inputimeout() function 
#     time_over = inputimeout(prompt='Name your best friend:', timeout=3) 
  
# # Catch the timeout error 
# except Exception: 
  
#     # Declare the timeout statement 
#     time_over = 'Your time is over!'
#     print(time_over) 
  
# # Print the statement on timeoutprint(time_over) 

##########okay now let's try the wanky workaround

limit = 5
start = time.time()

while (time.time()-start<=limit):
    curr = time.time()
    try: 
    # Take timed input using inputimeout() function 
        time_over = inputimeout(prompt='Name your best friend:', timeout=limit-(curr-start)) 
  
# Catch the timeout error 
    except Exception: 
    
        # Declare the timeout statement 
        time_over = 'Your time is over!'
        print(time_over, time.time()-start) 
        break