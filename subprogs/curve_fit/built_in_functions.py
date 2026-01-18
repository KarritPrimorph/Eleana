import copy
from scipy import constants as spc
import sympy
import numpy as np
import json
from modules.CTkMessagebox import CTkMessagebox
from pathlib import Path
from customtkinter import filedialog
from lmfit.models import ExpressionModel
from assets.Error import Error
from subprogs.edit_values_in_table.edit_values_in_table import EditValuesInTable

class Function:
    physical_constants = {
        "@PC": [spc.h, "Planck constant"],
        "@RPC": [spc.hbar, "reduced Planck constant"],
        "@AC": [spc.N_A, "Avogadro constant"],
        "@RC": [10973731.568157, "Rydberg constant"],
        "@SC": [spc.c, "speed of light in vacuum"],
        "@GC": [spc.G, "Newtonian constant of gravitation"],
        "@EC": [spc.e, "elementary charge"],
        "@BC": [spc.k, "Boltzmann constant"],
        "@FC": [96485.33212331001, "Faraday constant"],
        "@ST": [spc.sigma, "Stefan-Boltzmann constant"],
        "@MC": [spc.R, "molar gas constant"],
        "@NC": [5.0507837393e-27, "nuclear magneton"],
        "@BM": [9.2740100657e-24, "Bohr magneton"],
        "@EA": [spc.m_e, "electron mass"],
        "@MP": [spc.m_p, "proton mass"],
        "@MN": [spc.m_n, "neutron mass"],
        "@AL": [6.644657345e-27, "alpha particle mass"],
        "@MU": [1.883531627e-28, "muon mass"],
        "@TA": [3.16754e-27, "tau mass"],
        "@DE": [3.3435837768e-27, "deuteron mass"],
        "@TR": [5.0073567512e-27, "triton mass"],
        "@AH": [spc.m_u, "atomic mass constant"],
        "@PI": [spc.pi, "pi constant"]
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
                 constant: dict = {},
                 fit_results: dict = {}
                 ):

        # Name of the function
        self.name = name

        # Right side of the equation entered by a user
        self.equation_text = equation_text

        # Right side of the equation ready to fit, parsed by sympy
        self.equation = equation_text

        # Parameters -> list, f. example: ['a', 'b']:
        self.parameters = parameters

        # Name of independent variable -> string for example 'x'
        self.variable = variable

        # Initial values for parameters -> dictionary, for example {'a': 1, 'b': 2}
        self.initial_values = initial_values

        # Boundary conditions for parameters -> dictionary, for example {'a': -1, 'b': -2}
        self.minimum = minimum
        self.maximum = maximum

        # Fit this parameter -> dictionary, for example: {'a': True, 'b': False}
        self.fit_parameters = fit_parameters

        # Define which parameters should be non_negative
        # Dictionary, for example: {'a':  False, 'b': False}
        self.non_negative = nonnegative_parameters

        # Validated -> bool, means that function wasa checked and parsed by sympy
        self.validated = validated

        # Constant values -> defines which parameter must be kept constant.
        # For example {'a': True, 'b': False}
        self.constant = constant

        # Export path
        self.export_path = Path.home()

        # Import path
        self.import_path = Path.home()

        # Optimized results
        self.fit_results = fit_results

    def ci_to_text(self, ci):
        """Convert lmfit CI dict to readable text"""
        lines = []

        for parname, points in ci.items():
            lines.append(f"Parameter: {parname}")

            best = None
            intervals = {}

            for sigma, value in points:
                if sigma == 0.0:
                    best = value
                else:
                    intervals.setdefault(sigma, []).append(value)

            if best is not None:
                lines.append(f"  best value = {best:.6g}")

            for sigma in sorted(intervals):
                vals = intervals[sigma]
                if len(vals) == 2:
                    lo, hi = min(vals), max(vals)
                    lines.append(
                        f"  {sigma:.2f} :  lower = {lo:.6g},  upper = {hi:.6g}"
                    )
                else:
                    lines.append(
                        f"  {sigma:.2f} :  incomplete CI"
                    )

            lines.append("")

        return "\n".join(lines)

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
            return True
        except:
            return False

    def prepare_equation(self):
        ''' Prepare the equation for fitting  '''
        self.equation = copy.copy(self.equation_text)
        for constant_code, value in Function.physical_constants.items():
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
                if key in self.parameters:
                    self.parameters.remove(key)

    def evaluate(self, variable=None, x_vals=None, initial_values=None):
        """
        Calculate function values for given x using the equation from self.equation.

        Parameters
        ----------
        variable : str, optional
            Name of the independent variable (default: self.variable)
        x_vals : np.ndarray
            Array of x values to evaluate
        initial_values : dict, optional
            Parameter values either as dict {'a': 1.0, 'b': 0.5}
        """

        if not self.validated:
            if non_negativeself.eleana.devel_mode:
                print("Please, validate function first.")
            return None

        if x_vals is None:
            if self.eleana.devel_mode:
                print("Function.calculate: No x axis defined.")
            return None

        # Change variables into symbols for sympy
        variable = sympy.Symbol(variable or self.variable)
        param_symbols = [sympy.Symbol(name) for name in self.parameters]

        # Create symbolic expression
        expr = sympy.sympify(self.equation)

        # Generate fast function
        args = [variable] + param_symbols
        f = sympy.lambdify(args, expr, modules=["numexpr"])

        # Prepare parameters' values
        if initial_values is None:
            param_values = [self.initial_values[p] for p in self.parameters]
        else:
            param_values = [initial_values[p] for p in self.parameters]

        # Calculate function values (vector)
        y_vals = f(x_vals, *param_values)
        return np.asarray(y_vals)

    def validate(self):
        ''' Check if the expression is correct and can be used
            for fitting and calculations.
        '''
        try:
            sympy.sympify(self.equation_text)
            self.validated = True
        except sympy.SympifyError:
            self.validated = False
        return self.validated

    def export(self, master):
        ''' Export function to a file'''
        file = filedialog.asksaveasfilename(parent= master,
                                            initialdir=self.export_path,
                                            defaultextension=".elf",
                                            filetypes=[("Eleana function to fit", "*.elf"), ("All files", "*.*")],
                                            title="Export function to file"
                                            )
        if not file:
            return
        file = Path(file)

        f_j = {'Name': self.name,
               'Equation_text': self.equation_text,
               'Variable': self.variable,
               'Parameters': self.parameters,
               'InitVals': self.initial_values,
               'Min': self.minimum,
               'Max': self.maximum,
               'Validated': self.validated,
               'Non-negative': self.non_negative,
               'Fit_parameters': self.fit_parameters
               }

        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(f_j, f, ensure_ascii=False, indent=4)
                self.export_path = file.parent
        except Exception as e:
            Error.show(title='Export function', info='Error while exporting function.', details=e)

    def import_function(self, master):
        ''' Import a function form a file'''

        file = filedialog.askopenfilename(parent=master,
                                          initialdir=self.import_path,
                                          defaultextension=".elf",
                                          filetypes=[("Eleana function to fit", "*.elf"), ("All files", "*.*")],
                                          title="Import function to file"
                                        )
        if not file:
            return
        file = Path(file)

        try:
            with file.open("r", encoding="utf-8") as f:
                function_json = json.load(f)
        except Exception as e:
            Error.show(title='Load user functions', info='Cannot load user defined functions', details=e)
            return False

        try:
            self.name = function_json['Name'],
            self.equation_text = function_json['Equation_text'],
            self.variable = function_json.get('Variable', 'x'),
            self.parameters = function_json.get('Parameters', []),
            self.initial_values = function_json.get('InitVals', {}),
            self.minimum = function_json.get('Min', {}),
            self.maximum = function_json.get('Max', {}),
            self.nonnegative_parameters = function_json.get('Non-negative', []),
            self.validated=function_json.get('Validated', False)
            return self
        except:
            Error.show(title='Load user functions', info='The file is not compatible with Eleana function format.', details=e)
            return False

    def show_in_table(self, master):
        ''' Show parameters ond/or confidence intervals in spreadsheet'''

        if not self.fit_results['ci']:
            return
        headers = self.fit_results['ci'].pop(0)
        rows = self.fit_results['ci']
        table = EditValuesInTable(window_title= 'Confidence intervals',
                                  master = master,
                                  column_names=headers,
                                  complex=False,
                                    spreadsheet = rows
                                  )
        response = table.get()
    # ------------------
    # FITTING PROCEDURES
    # ------------------

    def build_lmfit_model(self):
        """
        Creates lmfit ExpressionModel and Parameters based on the equation
        and parameter settings stored in this object.
        """

        def _safe_float(value, default):
            """
            Convert value (possibly a string) to float.
            If empty / None → return default (np.inf or -np.inf)
            """
            if value is None:
                return default
            if isinstance(value, str):
                v = value.strip().lower()
                if v == "":
                    return default
                if v in ("inf", "+inf"):
                    return np.inf
                if v == "-inf":
                    return -np.inf
            return float(value)

        # Build model and parameters object
        model = ExpressionModel(self.equation, independent_vars=[self.variable])
        params = model.make_params()

        # Loop over declared parameters
        for p in self.parameters:

            # ----- Initial value -----
            if p in self.initial_values:
                params[p].value = self.initial_values[p]
            else:
                Error.show(
                    title="build_lmfit_model",
                    info=f"Parameter '{p}' not found in initial_values."
                )
                return None

            # ----- Minimum -----
            if p in self.minimum:
                params[p].min = _safe_float(self.minimum.get(p), -np.inf)
            else:
                params[p].min = _safe_float(self.minimum.get(p), -np.inf)

            # ----- Maximum -----
            if p in self.maximum:
                params[p].max = _safe_float(self.maximum.get(p), np.inf)
            else:
                params[p].max = _safe_float(self.maximum.get(p), np.inf)

            # ----- Non-negative -----
            if p in self.non_negative:
                params[p].min = max(params[p].min, 0)

            # ----- Constant parameter -----
            if p in self.constant and self.constant[p] is True:
                params[p].vary = False

            # ----- Fit parameter switch -----
            elif p in self.fit_parameters:
                params[p].vary = self.fit_parameters[p]
        return model, params


    def generate_eleana_parameters(self, experimental_data):
        ''' Generate parameters to store in parameters in eleana_dataset'''

        fitting_par = {'data_id': experimental_data.id,
                       'data_name': experimental_data.name,
                       'equation_text': self.equation_text,
                       'independent_variable': self.variable,
                       'parameters': self.initial_values,
                       'fit_report': self.fit_results.get('report_txt', 'No fitting results'),
                       'confidence_intervals': self.fit_results.get('ci', 'No CI results')
                       }
        return fitting_par

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

        {'Name': "Stretched Exp. Decay",
         'Equation_text': 'a*exp(-(x/t)^betha)+c',
         'Variable': 'x',
         'Parameters': ['a', 't', 'betha', 'c'],
         'InitVals': {'a':1, 'betha': 1, 'c':0, 't':10},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Linear",
         'Equation_text': 'a*x+b',
         'Variable': 'x',
         'Parameters': ['a', 'b'],
         'InitVals': {'a': 1, 'b': 0},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Slope",
         'Equation_text': 'a*x',
         'Variable': 'x',
         'Parameters': ['a'],
         'InitVals': {'a': 1},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Gauss",
         'Equation_text': 'a/(width*sqrt(2*@PI))*exp(-((x-center)^2)/(2*width^2))',
         'Variable': 'x',
         'Parameters': ['a', 'center', 'width'],
         'InitVals': {'a': 1, 'center':0, 'width':1},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Lorentz",
         'Equation_text': 'a/@PI*(0.5*width)/((x-center)^2+(0.5*width)^2)',
         'Variable': 'x',
         'Parameters': ['a', 'center', 'width'],
         'InitVals': {'a': 1, 'center': 0, 'width': 1},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Pseudo Voigt",
         'Equation_text': 'ag/(wg*sqrt(2*@PI))*exp(-((x-center)^2)/(2*wg^2))+al/@PI*(0.5*wl)/((x-center)^2+(0.5*wl)^2)',
         'Variable': 'x',
         'Parameters': ['ag', 'al', 'wg', 'wl', 'center'],
         'InitVals': {'ag': 1, 'al' : 1, 'wg': 1, 'wl': 1, 'center': 0},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Lorentz Derivative",
         'Equation_text': 'a/@PI*(0.5*width)*(2*center-2*x)/(((x-center)^2+(0.5*width)^2))^2',
         'Variable': 'x',
         'Parameters': ['a', 'center', 'width'],
         'InitVals': {'a': 1, 'center': 0, 'width': 1},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Gauss Derivative",
         'Equation_text': 'a*(2*center-2*x)/(2*width^3*sqrt(2*$pi))*exp(-((x-center)^2)/(2*width^2))',
         'Variable': 'x',
         'Parameters': ['a', 'center', 'width'],
         'InitVals': {'a': 1, 'center': 0, 'width': 1},
         'Min': {},
         'Max': {},
         'Validated': True
         },

        {'Name': "Pseudo Voigt Derivative",
         'Equation_text': 'ag*(2*center-2*x)/(2*wg^3*sqrt(2*$pi))*exp(-((x-center)^2)/(2*wg^2))+al*(2*center-2*x)/(2*wl^3*sqrt(2*$pi))*exp(-((x-center)^2)/(2*wl^2))',
         'Variable': 'x',
         'Parameters': ['ag', 'al', 'wg', 'wl', 'center'],
         'InitVals': {'ag': 1, 'al' : 1, 'wg': 1, 'wl': 1, 'center': 0},
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


class UserDefinedFunctions:
    def __init__(self, store_file):

        self.store_file = Path(store_file) / 'curve_fit_user_functions.json'
        self.functions = []

        # Load functions from the curve_fit_user_functions.json file
        functions = self.restore_functions(show_error=False)
        if functions:
            for function in functions:
                self.functions.append(
                    Function(
                        name = function['Name'],
                        equation_text = function['Equation_text'],
                        variable = function.get('Variable', 'x'),
                        parameters = function.get('Parameters', []),
                        initial_values=function.get('InitVals', {}),
                        minimum = function.get('Min', {}),
                        maximum = function.get('Max', {}),
                        nonnegative_parameters = function.get('Non-negative', [])

                ))

    def restore_functions(self, show_error = False):
        ''' Load file containing user_functions'''
        self.functions.clear()
        self.functions = []
        try:
            with self.store_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            if show_error:
                Error.show(title = 'Load user functions', info = 'Cannot load user defined functions', details = e)
            return None

        for d in data:
            self.functions.append(self.convert_from_json(d))
        return


    def store(self, show_error = True):
        '''Save file to self.store_file in json format'''
        functions_json = []
        for function in self.functions:
            functions_json.append(self.convert_to_json(function))
        try:
            with self.store_file.open("w", encoding="utf-8") as f:
                json.dump(functions_json, f, ensure_ascii=False, indent=4)
        except Exception as e:
            if show_error:
                Error.show(title = 'Store user functions', info = 'Cannot store user defined functions', details = e)


    def add_new(self, function):
        ''' Add a new function to the self.functions list'''
        name = function.name
        all_functions = self.get_list()

        # Check if function with the same name exists
        if name in all_functions:
            question = CTkMessagebox(icon = 'question', option_1="Replace", option_2='Cancel',title="Store function", message = 'Function with the same name already exists.' )
            response = question.get()
            if response == 'Replace':
                index = all_functions.index(name)
                self.functions.pop(index)
            else:
                return

        self.functions.append(function)
        self.store()

    def delete(self, name):
        ''' Delete name function in self.functions '''
        index = self.get_index(name)
        if index is not None:
            self.functions.pop(index)
        self.store()

    def get_index(self, name):
        ''' Return index of name in self.functions '''
        name_list = self.get_list()
        if name in name_list:
            index = name_list.index(name)
            return index
        else:
            return None


    def get_list(self):
        ''' Return list of names'''
        list_of_names = []
        for fc in self.functions:
            list_of_names.append(fc.name)
        return list_of_names

    def convert_to_json(self, function):
        ''' Convert function instance to dictionary'''
        f_j = {'Name': function.name,
                   'Equation_text': function.equation_text,
                   'Variable': function.variable,
                   'Parameters': function.parameters,
                   'InitVals': function.initial_values,
                   'Min': function.minimum,
                   'Max': function.maximum,
                   'Validated': function.validated,
                   'Non-negative': function.non_negative,
                   'Fit_parameters': function.fit_parameters
                   }
        return f_j

    def convert_from_json(self, function_json):
        ''' Convert function in json format to Function instance'''
        return Function(
                    name = function_json['Name'],
                    equation_text = function_json['Equation_text'],
                    variable = function_json.get('Variable', 'x'),
                    parameters = function_json.get('Parameters', []),
                    initial_values=function_json.get('InitVals', {}),
                    minimum = function_json.get('Min', {}),
                    maximum = function_json.get('Max', {}),
                    nonnegative_parameters = function_json.get('Non-negative', []),
                    validated=function_json.get('Validated', False)
                    )

    def get_by_name(self, name):
        ''' Return function instance based on the name'''
        list_of_names = self.get_list()
        if name not in list_of_names:
            return None
        index = list_of_names.index(name)
        return self.functions[index]



if __name__ == '__main__':
    builtin = BuiltInFunctions()
    lista = builtin.get_list()
    print(lista)