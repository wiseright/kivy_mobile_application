from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
import random

class Tabelline(App):
    def __init__(self):
        super().__init__()
        self.oper_1 = 0
        self.oper_2 = 0
        self.num_oper = 0
        self.idx_oper = 0
        self.corrette = 0
        self.isMultiplication = True

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        Window.size = (360, 800)


        # Popup for insertion error


        # create content and add to the popup
        content = Button(text='OK',
                         size_hint=(0.8,0.2))

        self.popup = Popup(title='Errore: inserisci il numero di operazioni',
                           content=content,
                           size_hint=(None, None),
                           size=(400, 200),
                           auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=self.popup.dismiss)

        # add image
        self.window.add_widget(Image(
            source='logo.png'
        ))

        # select operation type
        self.label_type_oper = Label(
            size_hint=(1, 0.4),
            font_size='20sp',
            halign='left',
            text='Moltiplicazioni: '
        )
        self.window.add_widget(self.label_type_oper)

        def on_checkbox_active(checkbox, value):
            if value:
                self.isMultiplication = True
                self.label_type_oper.text = 'Moltiplicazioni: '
            else:
                self.isMultiplication = False
                self.label_type_oper.text='Divisioni: '

        self.checkbox = CheckBox(size_hint=(1, 0.4), active=True)
        self.checkbox.bind(active=on_checkbox_active)

        self.window.add_widget(self.checkbox)

        # textinput for number of operation
        self.label_num_oper = Label(
            size_hint=(1, 0.4),
            font_size='20sp',
            halign='left',
            text = 'Quante operazioni: '
        )
        self.window.add_widget(self.label_num_oper)

        self.textinput_num_oper = TextInput(
            size_hint=(1, 0.4),
            font_size='15sp',
            padding_y='12sp',
            halign='center'
        )
        self.window.add_widget(self.textinput_num_oper)

        # textinput to insert the value of operation
        self.label_res = Label(
            size_hint=(1, 0.4),
            font_size='20sp',
            halign='left',
            text = 'Scrivi il risultato: '
        )
        self.window.add_widget(self.label_res)

        self.textinput_res = TextInput(
            size_hint=(1, 0.4),
            font_size='15sp',
            padding_y='12sp',
            halign='center'
        )
        self.window.add_widget(self.textinput_res)
        self.textinput_res.disabled=True

        # button to start the game
        self.button_go = Button(
            text='GO!',
            size_hint=(1, 0.4),
            bold=True,
            background_color='#0099ff'
        )
        self.window.add_widget(self.button_go)
        self.button_go.bind(on_press=self.start_game)

        self.label_res = Label(
            size_hint=(1, 0.4),
            font_size='20sp',
            halign='left',
            text=''
        )
        self.window.add_widget(self.label_res)

        # button to submit the value
        self.button_submit = Button(
            text='PROVA!',
            size_hint=(1, 0.4),
            bold=True,
            background_color='#0099ff'
        )
        self.window.add_widget(self.button_submit)
        self.button_submit.bind(on_press=self.crea_operazione)
        self.button_submit.disabled = True

        # Label oeprazione da eseguire
        self.label_question = Label(
            text='',
            font_size='20sp'
        )
        self.window.add_widget(self.label_question)

        # Label numero di operazione
        self.label_num_oper = Label(
            text='',
            font_size='20sp'
        )
        self.window.add_widget(self.label_num_oper)

        return self.window


    def start_game(self, instance):
        if not self.textinput_num_oper.text == '':
            self.button_go.disabled = True
            self.button_submit.disabled = False
            self.textinput_res.disabled = False

            # Create start operation
            self.oper_1 = random.randint(1, 9)
            self.oper_2 = random.randint(1, 9)
            oper_str = 'x' if self.isMultiplication == True else '/'
            if self.isMultiplication:
                self.label_question.text = f"{self.oper_1} {oper_str} {self.oper_2} = "
            else:
                self.label_question.text = f"{self.oper_1 * self.oper_2} {oper_str} {self.oper_2} = "

            self.num_oper = int(self.textinput_num_oper.text)
            self.idx_oper = 1
            self.label_num_oper.text = f'Operazione {self.idx_oper}/{self.num_oper}'
        else:
            self.popup.open()


    def crea_operazione(self, instance):
        # Verifica operazione precedente
        if self.isMultiplication:
            # operation: multiplication
            if (self.oper_1 * self.oper_2) == int(self.textinput_res.text):
                self.button_submit.background_color  = '#11680b'
                self.corrette = self.corrette + 1
            else:
                self.button_submit.background_color = '##a51c30'
        else:
            # operation: division
            if (self.oper_1 * self.oper_2 / self.oper_2) == int(self.textinput_res.text):
                self.button_submit.background_color  = '#11680b'
                self.corrette = self.corrette + 1
            else:
                self.button_submit.background_color = '##a51c30'

        # clear inputtext result operation
        self.textinput_res.text = ''


        if self.idx_oper == self.num_oper:
            # Ended whole operation
            self.label_num_oper.text = f'Operazioni Corrette = {self.corrette}/{self.num_oper}'
            # Reset counter
            self.button_submit.disabled = True
            self.button_go.disabled = False
            self.textinput_res.disabled = True
            self.corrette = 0
            self.idx_oper = 0
            return

        # Crea nuova operazione:
        self.oper_1 = random.randint(1, 9)
        self.oper_2 = random.randint(1, 9)
        oper_str = '*' if self.isMultiplication == True else '/'
        if self.isMultiplication:
            self.label_question.text = f"{self.oper_1} {oper_str} {self.oper_2} = "
        else:
            self.label_question.text = f"{self.oper_1 * self.oper_2} {oper_str} {self.oper_2} = "
        self.idx_oper += 1
        self.label_num_oper.text = f'Operazione {self.idx_oper}/{self.num_oper}'
        return


Tabelline().run()
