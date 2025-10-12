import sympy
import numpy
import copy
from scipy import constants as spc

class Function:
    constants = {
        "$PC": [spc.h, "Planck constant"],
        "$RPC": [spc.hbar, "reduced Planck constant"],
        "$AC": [spc.N_A, "Avogadro constant"],
        "$RC": [10973731.568157, "Rydberg constant"],
        "$SC": [spc.c, "speed of light in vacuum"],
        "$GC": [spc.G, "Newtonian constant of gravitation"],
        "$EC": [spc.e, "elementary charge"],
        "$BC": [spc.k, "Boltzmann constant"],
        "$FC": [96485.33212331001, "Faraday constant"],
        "$ST": [spc.sigma, "Stefan-Boltzmann constant"],
        "$MC": [spc.R, "molar gas constant"],
        "$NC": [5.0507837393e-27, "nuclear magneton"],
        "$BM": [9.2740100657e-24, "Bohr magneton"],
        "$EA": [spc.m_e, "electron mass"],
        "$MP": [spc.m_p, "proton mass"],
        "$MN": [spc.m_n, "neutron mass"],
        "$AL": [6.644657345e-27, "alpha particle mass"],
        "$MU": [1.883531627e-28, "muon mass"],
        "$TA": [3.16754e-27, "tau mass"],
        "$DE": [3.3435837768e-27, "deuteron mass"],
        "$TR": [5.0073567512e-27, "triton mass"],
        "$AH": [spc.m_u, "atomic mass constant"],
        "$PI": [spc.pi, "pi constant"]
    }

    def __init__(self,
                 name,
                 equation,
                 variable = 'x',
                 parameters = [],
                 initaial_values:dict = {},
                 minimum:dict = {},
                 maximum :dict = {},
                 fit_parameters:dict = {}
                 ):

        # Name of the function
        self.name = name

        # Right side of the equation
        self.equation_text = equation

        # Right side of the equation ready to fit
        self.equation = equation

        # Parameters:
        self.parameters = parameters

        # Name of independent variable
        self.variable = variable

        # Initial values for parameters
        self.initial_values = initaial_values

        # Boundary conditions for parameters
        self.minimum = minimum
        self.maximum = maximum

        # Fit this parameter:
        self.fit_parameters = fit_parameters

    def find_parameters(self):
        ''' Parse expression and get the parameters'''
        try:
            expression = sympy.sympify(self.equation)
            symbols = expression.free_symbols
            self.parameters.clear()
            self.parameters = []

            for symbol in symbols:
                if str(symbol) != self.variable:
                    self.parameters.append(str(symbol))
        except:
            print("Please call 'prepare_equation' first.")

    def prepare_equation(self):
        ''' Prepare the equation for fitting  '''
        self.equation = copy.copy(self.equation_text)
        for constant_code, value in Function.constants.items():
            self.equation = self.equation.replace(constant_code, str(value[0]))
        if self.fit_parameters:
            for key, val in self.fit_parameters.items():
                self.equation = self.equation.replace(key, str(val))
        self.equation = self.equation.replace('^', '**')


functions = [
                {'Name': "Boltzman",
                 'Function': 'a2+(a1-a2)/(1+exp((x-x0)/dx))',
                 'Variable': 'x',
                 'Parameters' : ['a1', 'a2', 'x0', 'dx'],
                 'InitVals'   : [],
                 'Min':         [],
                 'Max':         []
                 },

                {'Name': "Exp. Decay 1",
                 'Function': 'a*exp(-x/t)+c',
                 'Variable': 'x',
                 'Parameters' : ['a', 't', 'c'],
                 'InitVals'   : [],
                 'Min':         [],
                 'Max':         []
                 },

                {'Name': "Exp. Decay 2",
                 'Function': 'a1*exp(-x/t1)+a2*exp(-x/t2)+c',
                 'Variable': 'x',
                 'Parameters' : ['a1', 'a2', 't1', 't2', 'c'],
                 'InitVals'   : [],
                 'Min':         [],
                 'Max':         []
                 },

                {'Name': "Exp. Decay 2",
                 'Function': 'a1*exp(-x/t1)+a2*exp(-x/t2)+c',
                 'Variable': 'x',
                 'Parameters' : ['a1', 'a2', 't1', 't2', 'c'],
                 'InitVals'   : [],
                 'Min':         [],
                 'Max':         []
                 },

                {'Name': "Exp. Decay 3",
                 'Function': 'a1*exp(-x/t1)+a2*exp(-x/t2)+a3*exp(-x/t3)+c',
                 'Variable': 'x',
                 'Parameters' : ['a1', 'a2', 'a3', 't1', 't2', 't3', 'c'],
                 'InitVals'   : [],
                 'Min':         [],
                 'Max':         []
                 },

    ]

if __name__ == '__main__':
    expr = Function(name = 'Expon', variable = 'x', equation = 'a*exp(x/t)+c^2+d1+$PC', fit_parameters={'t': 25})
    expr.prepare_equation()
    expr.find_parameters()
    print(expr.equation)
    print(expr.parameters)
