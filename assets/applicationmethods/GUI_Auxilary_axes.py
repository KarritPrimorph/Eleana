from modules.CTkMessagebox import CTkMessagebox
from subprogs.select_data.select_data import SelectData
import copy

class AuxilaryAxesMixin:

    def auxilary_axes(self):
        ''' Changes in status of auxilary axes '''

        self.eleana.gui_state.auxilary_axes = bool(self.app.check_aux)
        if self.eleana.gui_state.auxilary_axes:
            self.aux_reset_frame.grid()
        else:
            self.aux_reset_frame.grid_remove()
        self.grapher.toggle_aux_axis()


    def reset_auxilary_axes(self):
        ''' Set scales in auxilary to main axes'''
        self.grapher.plot_graph()
        self.grapher.on_mouse_release()


    def reset_auxilary_x(self):
        ''' Set x axis in auxilary scale the sami as in main'''
        x_lim = self.grapher.aux_ax.get_xlim()
        self.grapher.ax.set_xlim(x_lim)
        self.grapher.canvas.draw_idle()
        self.grapher.on_mouse_release()


    def reset_auxilary_y(self):
        ''' Set y axis in auxilary scale the sami as in main'''
        y_lim = self.grapher.aux_ax.get_ylim()
        self.grapher.ax.set_ylim(y_lim)
        self.grapher.canvas.draw_idle()
        self.grapher.on_mouse_release()


    def apply_scaling(self):
        ''' Multiply scales in selected data according to the scaling factor '''

        # Check if first and second is selected and on
        fir = False if self.eleana.selections['first'] < 0 else True
        fon = bool(self.eleana.selections['f_dsp'])
        first = fir and fon

        sec = False if self.eleana.selections['second'] < 0 else True
        son = bool(self.eleana.selections['s_dsp'])
        second = sec and son

        if not first or not second:
            info = CTkMessagebox(master=self.mainwindow,
                             message='Both First and Second mus be displayed to activate auxilary axes.',
                             icon='warning',
                             title="Apply scaling")

            return


        index = self.eleana.selections['first']
        if index < 0:
            return
        main_x_scale = self.grapher.ax.get_xlim()
        auxi_x_scale = self.grapher.aux_ax.get_xlim()

        main_y_scale = self.grapher.ax.get_ylim()
        auxi_y_scale = self.grapher.aux_ax.get_ylim()

        factor_y = (auxi_y_scale[1] - auxi_y_scale[0]) / (main_y_scale[1] - main_y_scale[0])
        delta_y = main_y_scale[0] * factor_y - auxi_y_scale[0]

        factor_x = (auxi_x_scale[1] - auxi_x_scale[0]) / (main_x_scale[1] - main_x_scale[0])
        delta_x = main_x_scale[0] * factor_x - auxi_x_scale[0]

        dialog = CTkMessagebox(title = 'Apply scalling',
                               message = 'Select data to calculate',
                               option_3="First",
                                option_1 = 'All in group',
                                option_2 = "Select from list",
                                )

        response = dialog.get()
        indexes = []
        if response is None:
            return
        elif response == "First":
            indexes = [self.eleana.selections['first']]
        elif response == "All in group":
            indexes = self.eleana.get_indexes_from_group()
        elif response == "Select from list":
            group = self.eleana.selections['group']
            items = []
            for idx in self.eleana.assignmentToGroups[group]:
                items.append(self.eleana.dataset[idx].name_nr)

            select = SelectData(master=self.mainwindow,
                                multiple_selections=True,
                                title = 'Select data fro scaling',
                                group = group,
                                items = items
                                )
            indexes = select.get()

        if not indexes:
            return
        self._apply_scaling_operation(indexes = indexes,
                                      factor_y = factor_y,
                                      factor_x = factor_x,
                                      delta_x = delta_x,
                                      delta_y = delta_y
                                      )

    def _apply_scaling_operation(self, indexes, factor_x, delta_x, factor_y, delta_y):

        for index in indexes:
            data = copy.deepcopy(self.eleana.dataset[index])

            data.y = data.y * factor_y
            data.y = data.y - delta_y

            data.x = data.x * factor_x
            data.x = data.x - delta_x

            data.name = data.name + ':RESCALED'

            self.eleana.results_dataset.append(data)

        self.update.dataset_list()
        self.update.all_lists()

        self.result_selected(data.name)
        self.sel_result.set(data.name)

    # def apply_scaling(self):
    #     ''' Multiply scales in selected data according to the scaling factor '''
    #     index = self.eleana.selections['first']
    #     if index < 0:
    #         return
    #     # data = copy.deepcopy(self.eleana.dataset[index])
    #     main_x_scale = self.grapher.ax.get_xlim()
    #     auxi_x_scale = self.grapher.aux_ax.get_xlim()
    #
    #     main_y_scale = self.grapher.ax.get_ylim()
    #     auxi_y_scale = self.grapher.aux_ax.get_ylim()
    #
    #     factor_y = (auxi_y_scale[1] - auxi_y_scale[0]) / (main_y_scale[1] - main_y_scale[0])
    #     delta_y = main_y_scale[0] * factor_y - auxi_y_scale[0]
    #     # data.y = data.y * factor_y
    #     # data.y = data.y - delta_y
    #
    #     factor_x = (auxi_x_scale[1] - auxi_x_scale[0]) / (main_x_scale[1] - main_x_scale[0])
    #     delta_x = main_x_scale[0] * factor_x - auxi_x_scale[0]
    #
    #     # data.x = data.x * factor_x
    #     # data.x = data.x - delta_x
    #     #
    #     # data.name = data.name + ':RESCALED'
    #
    #     self.eleana.results_dataset.append(data)
    #     self.update.dataset_list()
    #     self.update.all_lists()
    #
    #     self.result_selected(data.name)
    #     self.sel_result.set(data.name)
