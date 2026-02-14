from subprogs.normalize.normalize import Normalize
from subprogs.trim_data.Trim_data import TrimData
from subprogs.set_zero_on_x_axis.set_zero_on_x_axis import SetZeroOnX
from subprogs.offset_correction.offset_correction import OffsetCorr
from subprogs.polynomial_baseline.Polynomial_baseline import PolynomialBaseline
from subprogs.spline_baseline.Spline_baseline import SplineBaseline
from subprogs.filter_savitzky_golay.sav_gol import SavGol
from subprogs.filter_fft.fft_filter import FFTFilter
from subprogs.pseudomodulation.pseudomodulation import PseudoModulation
from subprogs.fft.fast_fourier_transform import FastFourierTransform
from subprogs.spectra_subtraction.spectra_subtration import SpectraSubtraction
from subprogs.simple_arithmetics.simple_arithmetics import SimpleArithmetics
import numpy as np

class MenuModificationsMixin:
    def normalize(self):

        ''' Normalize amplitude '''

        normalize = Normalize(self, which='first')


    def trim_data(self):

        ''' Crop data '''

        subprog_trim_data = TrimData(self, which="first")


    def set_zero_on_x_axis(self):

        ''' Select zero on X axis'''

        subprog_set_zero = SetZeroOnX(self, which='first')


    def offset_correction(self):

        ''' Offset correction '''

        subprog_offset_corr = OffsetCorr(self, which='first')


    def polynomial_baseline(self):

        ''' Subtract polynomial baseline'''

        subprog_polynomial_baseline = PolynomialBaseline(self, which='first')


    def spline_baseline(self):

        '''Subtract spline baseline'''

        subprog_spline_baseline = SplineBaseline(self, which='first')





    def spectra_subtraction(self):

        ''' Interactive spectra arithmetics '''

        subprog_spectra_subtraction = SpectraSubtraction(self, which='first')


    def simple_arithmetics(self, operation):

        ''' Simple arithmetics'''

        simarith = SimpleArithmetics(master = self.mainwindow,operation=operation, eleana=self.eleana)
        self.update.list_in_combobox('sel_result')
        self.update.list_in_combobox('r_stk')
        # Set the position to the last added item
        list_of_results = self.sel_result._values
        position = list_of_results[-1]
        self.sel_result.set(position)
        self.result_selected(position)


    def filter_savitzky_golay(self):

        ''' Savitzky-Golay filter'''

        subprog_sav_gol = SavGol(self, which='first')


    def filter_fft_lowpass(self):

        ''' FFT filter'''

        subprog_fft_lowpass = FFTFilter(self, which = 'first')


    def pseudomodulation(self):

        ''' Pseudomodulation '''

        subprog_pseudomodulation = PseudoModulation(self, which = 'first')


    def fast_fourier_transform(self):

        ''' FFT '''

        subprog_fft = FastFourierTransform(self, which = 'first')


    def complex_modifications(self, operation, which = None):

        ''' Complex numbers'''

        refresh_first = None
        refresh_second = None
        if which is None:
            selected_data = self.select_data_from_group(title = operation)
        elif which == 'first':
            selected_data = [self.sel_first.get()]
        elif which == 'second':
            selected_data = [self.sel_second.get()]
        else:
            return

        if not selected_data:
            return
        for name in selected_data:
            index = self.eleana.get_index_by_name(name)
            if index is not None:
                data = self.eleana.dataset[index]
                if data.complex:
                    data.complex = False

                    if operation == 'Drop imaginary part':
                        data.y = np.asarray(data.y.real, dtype=float)
                    elif operation == 'Drop real part':
                        data.y = np.asarray(data.y.imag, dtype=float)
                    elif operation == 'Magnitude':
                        data.y = np.asarray(np.abs(data.y), dtype=float)
                    elif operation == 'Swap Re/Im':
                        data.y = data.y.imag + 1j * data.y.real
                        data.complex = True

                if data.name_nr == self.sel_first.get():
                    refresh_first = data.name_nr
                if data.name_nr == self.sel_second.get():
                    refresh_second = data.name_nr

            if refresh_first:
                self.first_selected(refresh_first)
            if refresh_second:
                self.second_selected(refresh_second)



