import sympy
import copy
from scipy import constants as spc
from sympy import symbols, sympify, exp, lambdify

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
                 name = '',
                 equation_text = '',
                 variable = 'x',
                 parameters = [],
                 initial_values:dict = {},
                 minimum:dict = {},
                 maximum :dict = {},
                 fit_parameters:dict = {},
                 nonnegative_parameters = [],
                 validated = False,
                 constant: dict = {}
                 ):

        # Name of the function
        self.name = name

        # Right side of the equation
        self.equation_text = equation_text

        # Right side of the equation ready to fit
        self.equation = equation_text

        # Parameters:
        self.parameters = parameters

        # Name of independent variable
        self.variable = variable

        # Initial values for parameters
        self.initial_values = initial_values

        # Boundary conditions for parameters
        self.minimum = minimum
        self.maximum = maximum

        # Fit this parameter:
        self.fit_parameters = fit_parameters

        # Define which parameters should be non_negative
        self.non_negative = nonnegative_parameters

        # Validated
        self.validated = validated

        # Constant values
        self.constant = constant

    def sort_parameters(self, reverse = False):
        self.parameters.sort(key=str.lower, reverse=reverse)

    def find_parameters(self):
        ''' Parse expression and get the parameters from the equation'''
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
        self.constant_parameters()

    def constant_parameters(self):
        ''' Replace parameters with values if constant checkbutton is selected
            It eliminates the parameter from fitting
        '''
        if not self.constant:
            return
        for key, val in self.constant.items():
            if val and key in self.equation:
                self.equation = self.equation.replace(key, str(val))
                self.parameters.pop(key)

    def calculate(self, x=None):
        ''' Calculate function values for given x using the equation from self.equation'''
        if not x:
            if self.eleana.devel_mode:
                print("Function.calculate: No x axis defined.")
            return

        # Define parameters
        parameters = {name: symbols(name) for name in self.parameters}

        equation = sympify(self.equation, locals=parameters)
        ordinate = []
        for arg in x:
            result = equation.subs(self.initial_values).evalf()
            ordinate.append(result)


    def validate(self):
        pass

class BuiltInFunctions:
    definitions = [
        {'Name': "Boltzman",
         'Equation_text': 'a2+(a1-a2)/(1+exp((x-x0)/dx))',
         'Variable': 'x',
         'Parameters': ['a1', 'a2', 'x0', 'dx'],
         'InitVals': {'a1':2, 'a2':1, 'x0':0, 'dx':1},
         'Min': {},
         'Max': {},
         'Validated': True},

        {'Name': "Exp. Decay 1",
         'Equation_text': 'a*exp(-x/t)+c',
         'Variable': 'x',
         'Parameters': ['a', 't', 'c'],
         'InitVals': {},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Exp. Decay 2",
         'Equation_text': 'a1*exp(-x/t1)+a2*exp(-x/t2)+c',
         'Variable': 'x',
         'Parameters': ['a1', 'a2', 't1', 't2', 'c'],
         'InitVals': {},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Exp. Decay 2",
         'Equation_text': 'a1*exp(-x/t1)+a2*exp(-x/t2)+c',
         'Variable': 'x',
         'Parameters': ['a1', 'a2', 't1', 't2', 'c'],
         'InitVals': {'a1': 1, 'a2': 1, 't1': 2, 't2': 3, 'c':0},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Exp. Decay 3",
         'Equation_text': 'a1*exp(-x/t1)+a2*exp(-x/t2)+a3*exp(-x/t3)+c',
         'Variable': 'x',
         'Parameters': ['a1', 'a2', 'a3', 't1', 't2', 't3', 'c'],
         'InitVals': {},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Exp. Growth",
         'Equation_text': 'a*exp(x/t)+c',
         'Variable': 'x',
         'Parameters': ['a', 't', 'c'],
         'InitVals': {},
         'Min': {},
         'Max': {},
         'Validated': True
         },
    ]

    def __init__(self):
        self.functions = []
        for function in BuiltInFunctions.definitions:
            self.functions.append(
                Function(
                    name = function['Name'],
                    equation_text = function['Equation_text'],
                    variable = function.get('Variable', 'x'),
                    parameters = function.get('Parameters', []),
                    initial_values=function.get('InitVals', {}),
                    minimum = function.get('Min', {}),
                    maximum = function.get('Max', {}),
                    nonnegative_parameters = function.get('Non-negative', []),
                    validated=function.get('Validated', False)

            ))

    def get_list(self):
        list_of_names = []
        for fc in self.functions:
            list_of_names.append(fc.name)
        return list_of_names

    def get_by_name(self, name):
        list_of_names = self.get_list()
        if name not in list_of_names:
            return None
        index = list_of_names.index(name)
        return self.functions[index]


# class UserDefinedFunctions:
#     def __init__(self):
#         self.builtin_functions = []
#
#         for function in BuiltInFunctions.definitions:
#             self.builtin_functions.append(
#                 Function(
#                     name = function['Name'],
#                     equation_text = function['Equation_text'],
#                     variable = function.get('Variable', 'x'),
#                     parameters = function.get('Parameters', []),
#                     initial_values=function.get('InitVals', {}),
#                     minimum = function.get('Min', {}),
#                     maximum = function.get('Max', {}),
#                     nonnegative_parameters = function.get('Non-negative', [])
#
#             ))
#
#     def get_list(self):
#         list_of_names = []
#         for fc in self.builtin_functions:
#             list_of_names.append(fc.name)
#         return list_of_names

if __name__ == '__main__':
    builtin = BuiltInFunctions()
    lista = builtin.get_list()
    print(lista)