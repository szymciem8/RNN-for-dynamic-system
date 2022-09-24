import random
import sympy as sym
from sympy.abc import s, t, y, x, y, z
from sympy.integrals import laplace_transform
from sympy.integrals import inverse_laplace_transform
import numpy as np

class DynamicModel:
    
    def __init__(self, definition, initial_values=None):
        self.symbolic_definition = definition
        self.initial_values = initial_values
        
    @property
    def differential(self):
        return inverse_laplace_transform(self.symbolic_definition, s, t)

class DynamicProcess():
    
    def __init__(self, model, step_value, sim_step = 0.1):
        self.step_value = step_value
        self.model = model.symbolic_definition
        self.sim_time = 0
        self.step = sim_step
        self.output = 0
        self.U, self.u = self.create_input_process()
        self.y = self.create_output_process()
        
    def change_input(self, step_value):
        self.step_value = step_value
        
    def generate_inverse_laplace_inputs(self):
        for U in self.U:
            u1 = inverse_laplace_transform(U1, s, t)
            
    def generate_time_series(self, duration, n_steps, new_inputs=False):
        ts = np.linspace(0,duration,n_steps)
        us = np.zeros(len(ts))
        ys = np.zeros(len(ts))
        
        if new_inputs:
            self.U, self.u = self.create_input_process()
            self.y = self.create_output_process()
        
        for u in self.u:
            for i in range(len(ts)):
                us[i] += u.subs(t, ts[i])

        for y in self.y:
            for i in range(len(ts)):
                ys[i] += y.subs(t, ts[i])

        return ts, us, ys
    
    def create_input_process(self, segments=5):
        from sympy.abc import s, t, y, x, y, z
        U, u = [], []
        
        for i in range(segments):
            k = random.randint(-10, 10)
            delay = round(random.uniform(-10, 0), 2)
            U_symbolic = k/s*sym.exp(delay*s)
            U.append(U_symbolic)
            u.append(inverse_laplace_transform(U_symbolic, s, t))
            
        return U, u
        
    def create_output_process(self):
        y = []
        model = self.model.copy()
        for U in self.U:
            sub = model * U
            y.append(inverse_laplace_transform(sub, s, t))
        return y
        
    def output_value(self):
        self.output = self.step_value * self.model.subs(t, self.sim_time)
        # self.output += self.model.subs(t, self.sim_time)
        self.sim_time += self.step
        return self.output