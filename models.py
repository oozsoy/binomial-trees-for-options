import numpy as np

class binomial_tree_model:
    
    def __init__(self, u, r, T, num_steps):
        
        self.u = u 
        self.d = 1/u
        self.r = r
        self.T = T
        self.num_steps = num_steps
    
        self.dt = T/num_steps # time increments    
        self.df = np.exp(-r * self.dt)  # discount factor per step
            
        self.q = (np.exp(r * self.dt) - self.d) / (self.u - self.d) # risk-neutral probability