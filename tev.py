import time 
import random as rand

var: float = 0.0

while var < 10:
    time.sleep(round(rand.uniform(0.2, 1.8), 1))
    var += round(rand.uniform(0.2, 1.8), 1)
    var = min(var, 10)
    print(var)