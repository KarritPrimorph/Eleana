from subprogs.user_input.single_dialog import SingleDialog
from subprogs.select_data.select_data import SelectData
import copy

class SimpleArithmetics:
    def __init__(self, master, eleana, operation):
        self.eleana = eleana
        self.master = master
        self.operation = operation

        if operation[1] == "*":
            self.dtitle = f"Multiply {operation[0]} by constant."
        elif operation[1] == "/":
            self.dtitle = f"Divide {operation[0]} by constant."
        elif operation[1] == "+":
            self.dtitle = f"Add constant to {operation[0]}."
        elif operation[1] == "-":
            self.dtitle = f"Subtract constant from {operation[0]}."
        else:
            return
        self.label = "\nExample or real value: 4.2\nExample for complex: 4+2j\n"
        self.run()

    def run(self):
        while True:
            number = self.open_dialog()
            if number is None:
                break
            elif number is False:
                self.label = "INVALID VALUE!\nExample or real value: 4.2\nExample for complex: 4+2j\n"
            else:
                self.calc(number)
                break

    def open_dialog(self):
        dialog = SingleDialog(master = self.master,
                              title = self.dtitle,
                              enable_dot=True,
                              label=self.label)
        text = dialog.get()
        dialog.cancel()
        if text is None:
            return None
        text = text.strip()

        try:
            number = ('real', float(text))
        except:
            number = False
            try:
                number = ('complex', complex(text))
            except:
                number = False
        return number

    def calc(self, number):
        if self.operation[0] == "group":
            indexes = self.eleana.get_indexes_from_group()
            names_nr = []
            for idx in indexes:
                names_nr.append(self.eleana.dataset[idx].name_nr)
            selections = SelectData(master = self.master,
                                          title = "Select data",
                                        group = self.eleana.selections['group'],
                                        items = names_nr)
            response = selections.get()
            if not response:
                return
            indexes = []
            for name in response:
                indexes.append(self.eleana.get_index_by_name(name))
        else:
            indexes = [self.eleana.selections[self.operation[0]]]
        for index in indexes:
            if index < 0:
                return
            data = copy.deepcopy(self.eleana.dataset[index])
            if number[0] == 'complex':
                data.complex = True
            data.y = number[1] * data.y
            self.eleana.results_dataset.append(data)