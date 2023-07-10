import tkinter as tk

class Option:
    def __init__(self, label, value, action=None):
        self.label = label
        self.value = value
        self.action = action

class UserInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Interface do Usuário")
        self.window.attributes('-fullscreen', True)

        self.options = [
            Option("Reconhecimento Facial", "1", self.option1_action),
            Option("Impressão Digital", "2", None),
            Option("Senha", "3", self.option3_action)
        ]

        self.sub_options = {
            "2": [
                Option("Entrar com Impressão Digital", "4", self.option2_suboption1_action),
                Option("Acionar Impressão Digital", "5", self.option2_suboption2_action),
                Option("Deletar Impressão Digital", "6", self.option2_suboption3_action)
            ]
        }

        self.current_options = self.options

        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        self.options_label = tk.Label(self.window, text="Selecione uma opção:", font=("Arial", 24))
        self.options_label.pack()

        self.option_labels = []
        for option in self.current_options:
            label = tk.Label(self.window, text=f"{option.value}. {option.label}", font=("Arial", 20))
            label.pack()
            self.option_labels.append(label)

        self.selected_option_label = tk.Label(self.window, text="Opção selecionada: ", font=("Arial", 20))
        self.selected_option_label.pack()

    def bind_events(self):
        self.window.bind('<KeyPress>', self.on_key_press)

    def on_key_press(self, event):
        option_value = event.char
        self.show_selected_option(option_value)

    def show_selected_option(self, option_value):
        selected_option = next((option for option in self.current_options if option.value == option_value), None)

        if selected_option:
            self.selected_option_label.configure(text="Opção selecionada: " + option_value)

            if option_value in self.sub_options:
                self.current_options = self.sub_options[option_value]
            else:
                self.current_options = self.options

            self.update_option_labels()

            if selected_option.action:
                selected_option.action()

    def update_option_labels(self):
        for index, option_label in enumerate(self.option_labels):
            option = self.current_options[index]
            option_label.configure(text=f"{option.value}. {option.label}")

    def option1_action(self):
        print("Executando ação da opção 1 (Reconhecimento Facial)")

    def option2_suboption1_action(self):
        print("Executando ação da sub-opção 1 (Entrar com Impressão Digital)")

    def option2_suboption2_action(self):
        print("Executando ação da sub-opção 2 (Acionar Impressão Digital)")

    def option2_suboption3_action(self):
        print("Executando ação da sub-opção 3 (Deletar Impressão Digital)")

    def option3_action(self):
        print("Executando ação da opção 3 (Senha)")

if __name__ == '__main__':
    user_interface = UserInterface()
    tk.mainloop()
