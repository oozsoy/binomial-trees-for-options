import numpy as np


class european_option:
    def __init__(self, model, S0, K, T, is_call=True):
        
        self.model = model
        
        # contract terms and observables
        self.S0 = S0
        self.K = K
        self.T = T
        self.is_call = is_call
        
        if self.T != self.model.T:
            
            raise ValueError("Option maturity T does not match model maturity T.")

    def price(self):
        
        # get the binomial model parameters
        N = self.model.num_steps
        u = self.model.u
        d = self.model.d
        q = self.model.q
        df = self.model.df
      

        # stock price at the maturity,
        j = np.arange(N+1) # at the Nth node there are N + 1 possible j vals
        S = self.S0 * (u ** j) * (d ** (N - j)) 

        # option pay-off (without exercise)
        if self.is_call:
            V = np.maximum(S - self.K, 0)
        else:
            V = np.maximum(self.K - S, 0)

        # Backward induction through time steps of the tree
        for i in reversed(range(N)):
            
            # Stock prices at time i 
            j = np.arange(i + 1)
            S = self.S0 * (u ** j) * (d ** (i - j))
            
            # discounted future expectation as the value at each previous time step 
            V = df * (q * V[1:i+2] + (1-q)* V[0:i+1])
        
        return V[0]
    
class american_option:
        
    def __init__(self, model, S0, K, T, is_call=False):
            
        self.model = model
            
        # contract terms and observables
        self.S0 = S0
        self.K = K
        self.T = T
        self.is_call = is_call
        
        if self.T != self.model.T:
            
            raise ValueError("Option maturity T does not match model maturity T.")

    def price(self):
        
        # get binomial model params
        N = self.model.num_steps
        u = self.model.u
        d = self.model.d
        q = self.model.q
        df = self.model.df
      

        # stock price at the maturity,
        j = np.arange(N+1) # at the Nth node there are N + 1 possible j vals
        S = self.S0 * (u ** j) * (d ** (N - j)) 

        # option pay-off (without exercise)
        if self.is_call:
            V = np.maximum(S - self.K, 0)
        else:
            V = np.maximum(self.K - S, 0)

        # Backward induction through time steps of the tree
        for i in reversed(range(N)):
            
            # Stock prices at time i 
            j = np.arange(i + 1)
            S = self.S0 * (u ** j) * (d ** (i - j))
            
            # continuation value: at each time step i, we have i + 1 possible nodes
            V = df * (q * V[1:i+2] + (1-q)* V[0:i+1])
            # intrinsic value 
            intrinsic = np.maximum(S - self.K, V) if self.is_call else np.maximum(self.K - S, V)
            
            V = np.maximum(V, intrinsic)

        return V[0]
    

class barrier_option:
    def __init__(self, model, S0, K, H, T, option_type='call', barrier_type='down-and-out'):
        self.model = model
        self.S0 = S0
        self.K = K
        self.H = H
        self.T = T

        if self.T != self.model.T:
            raise ValueError("Option maturity T does not match model maturity T.")

        self.is_call = option_type.lower() == 'call'
        self.is_knock_in = 'in' in barrier_type.lower()
        self.is_up = 'up' in barrier_type.lower()

    def price(self):
        N = self.model.num_steps
        u = self.model.u
        d = self.model.d
        q = self.model.q
        df = self.model.df

        j = np.arange(N + 1)
        S = self.S0 * u ** j * d ** (N - j)

        # Terminal payoff for vanilla option
        V = np.maximum(S - self.K, 0) if self.is_call else np.maximum(self.K - S, 0)

        # boolean flags for barrier hit: True or False 
        if self.is_up:
            barrier_hit = S >= self.H
        else:
            barrier_hit = S <= self.H

        # Knock-out: kill values where barrier is touched at the maturity
        V_KO = V.copy()
        V_KO[barrier_hit] = 0

        # Knock-in: nodes that hit the barrier at the maturity is non-zero
        V_KI = V.copy()
        V_KI[~barrier_hit] = 0

        breached = barrier_hit.copy()  # terminal breach status

        # Backward induction
        for i in reversed(range(N)):
            j = np.arange(i + 1)
            S = self.S0 * u ** j * d ** (i - j)

            # Discounted values
            V_KO = df * (q * V_KO[1:i+2] + (1 - q) * V_KO[0:i+1])
            V_KI = df * (q * V_KI[1:i+2] + (1 - q) * V_KI[0:i+1])

            if self.is_up:
                barrier_hit = S >= self.H
            else:
                barrier_hit = S <= self.H

            breached = barrier_hit | breached[0:i+1] | breached[1:i+2]

            # Knock-out logic
            V_KO[barrier_hit] = 0

            # Knock-in logic
            V_KI[~breached] = 0

        return V_KI[0] if self.is_knock_in else V_KO[0]