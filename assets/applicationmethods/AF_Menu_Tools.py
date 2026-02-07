from subprogs.select_data.select_items import SelectItems
from subprogs.user_input.single_dialog import SingleDialog
from modules.CTkMessagebox import CTkMessagebox
class MenuToolsMixin:

    def clear_selected_ranges(self):

        ''' Graphtools '''

        self.grapher.clear_selected_ranges()
        self.grapher.clear_all_annotations()

    def create_simple_static_plot(self):

        ''' Create Simple Plot '''

        if bool(self.switch_comparison.get()) == True:
            info = CTkMessagebox(master = self.mainwindow, title="Info", message="This function is not yet available for comparison view.")
            return
        static_plot = self.grapher.get_static_plot_data()
        if not static_plot:
            info = CTkMessagebox(master = self.mainwindow, title="Info", message="An error occurred or there is no data for graph creation.")
            return
        dialog = SingleDialog(master=self.mainwindow, title='Enter a name for the graph', label='Enter the graph name', text='')
        name = dialog.get()
        if not name:
            return
        static_plot['name'] = name
        self.eleana.storage.static_plots.append(static_plot)
        self.main_menubar.create_showplots_menu()
        self.show_static_graph_window(len(self.eleana.storage.static_plots)-1)

    def delete_simple_static_plot(self):

        ''' Delete simple static plot '''

        plots = self.eleana.storage.static_plots
        if not plots:
            return
        av_plots = []
        for plot in plots:
            av_plots.append(plot['name_nr'])
        select_items = SelectItems(master=self.mainwindow, title='Select plots',
                                  items=av_plots)
        names = select_items.get()
        if not names:
            return
        to_delete = []
        for name in names:
            to_delete.append(names.index(name))
        to_delete.sort(reverse=True)
        for i in to_delete:
            self.eleana.storage.static_plots.pop(i)
        self.main_menubar.create_showplots_menu()
