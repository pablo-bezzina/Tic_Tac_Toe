import tkinter
import random
import time

YELLOW = "#FFF67E"
RED = "#D91656"
BLUE = "#0A97B0"
FONT_NAME = "Courier"
BT_GRID_COLUMNS = range(0, 3)
BT_GRID_ROWS = range(2, 5)
WIN_RANGES = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
CORNERS = [1, 3, 7, 9]


class Game(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.game_on = True

        self.title("TIC TAC TOE")
        self.config(padx=100, pady=100, bg=YELLOW)

        self.game_label = tkinter.Label(text="Press 'begin' to start playing", font=(FONT_NAME, 24, "bold"),
                                        bg=YELLOW, wraplength=400)
        self.game_label.grid(column=0, columnspan=3, row=0)

        self.icon_label = tkinter.Label(text="", font=(FONT_NAME, 24, "bold"), bg=YELLOW)
        self.icon_label.grid(column=1, row=1)

        self.begin_button = tkinter.Button(text="Begin", command=self.game_mode)
        self.begin_button.grid(column=1, row=2)

        self.reset_button = tkinter.Button(text="Reset", command=self.new_game)
        self.reset_button.grid_forget()

        self.ghost_label = tkinter.Label(text="", font=(FONT_NAME, 24, "bold"), bg=YELLOW)
        self.ghost_label.grid(column=1, row=5)

        self.button1 = tkinter.Button(text=" ", command=lambda: self.press('1'))
        self.button2 = tkinter.Button(text=" ", command=lambda: self.press('2'))
        self.button3 = tkinter.Button(text=" ", command=lambda: self.press('3'))
        self.button4 = tkinter.Button(text=" ", command=lambda: self.press('4'))
        self.button5 = tkinter.Button(text=" ", command=lambda: self.press('5'))
        self.button6 = tkinter.Button(text=" ", command=lambda: self.press('6'))
        self.button7 = tkinter.Button(text=" ", command=lambda: self.press('7'))
        self.button8 = tkinter.Button(text=" ", command=lambda: self.press('8'))
        self.button9 = tkinter.Button(text=" ", command=lambda: self.press('9'))

        photo = tkinter.PhotoImage(file="1x1 pixel.png", width=1, height=1)
        self.buttons = {'1': self.button1, '2': self.button2, '3': self.button3, '4': self.button4, '5': self.button5,
                        '6': self.button6, '7': self.button7, '8': self.button8, '9': self.button9}
        for key, btt in self.buttons.items():
            btt.config(height=120, width=120, state='disabled', image=photo, compound='left')

        self.score = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}
        self.player_goes = False

        self.mainloop()

    def toggle_buttons(self, state_):
        for key, btt in self.buttons.items():
            btt.config(state=state_)

    def game_mode(self):
        self.begin_button.grid_forget()
        self.reset_button.grid(column=1, row=6)

        counter = 1
        for i in BT_GRID_ROWS:
            for j in BT_GRID_COLUMNS:
                self.buttons[str(counter)].grid(column=j, row=i)
                counter += 1

        self.new_game()

    def who_starts(self):
        return random.choice([True, False])

    def new_game(self):
        self.score = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}
        self.buttons = {'1': self.button1, '2': self.button2, '3': self.button3, '4': self.button4, '5': self.button5,
                        '6': self.button6, '7': self.button7, '8': self.button8, '9': self.button9}
        for key, btt in self.buttons.items():
            btt.config(text=" ")

        self.player_goes = self.who_starts()
        self.game_on = True

        if self.player_goes:
            self.player_turn()
        else:
            self.machine_turn()

    def player_turn(self):
        self.game_label.config(text='Your turn!')
        self.icon_label.config(text="O", font=(FONT_NAME, 48, "bold"), fg=BLUE)
        self.toggle_buttons('normal')

    def machine_turn(self):
        self.game_label.config(text="Machine's time")
        self.icon_label.config(text="X", font=(FONT_NAME, 48, "bold"), fg=RED)
        self.update()
        time.sleep(0.5)

        two_in_1_opport, btt_opp = self.check_two_in_line('X')
        two_in_1_risk, btt_risk = self.check_two_in_line('O')
        if two_in_1_opport:  # 1. Detect 2 machine marks in line, to achieve victory.
            self.press(btt_number=btt_opp, who_='machine')
        elif two_in_1_risk:  # 2. Detect 2 player marks in line, to avoid their victory.
            self.press(btt_number=btt_risk, who_='machine')
        elif len(self.buttons) == 9:  # 3. First move of the game - pick a corner, no-brainer.
            available_corners = [str(i) for i in CORNERS if self.buttons.get(str(i)) is not None]
            some_corner = random.choice(available_corners)
            self.press(some_corner, who_='machine')
        else:  # 4. Pick another corner if still available. Else pick whatever.
            available_corners = [str(i) for i in CORNERS if self.buttons.get(str(i)) is not None]
            if len(available_corners) > 0:
                some_corner = random.choice(available_corners)
                self.press(some_corner, who_='machine')
            else:
                some_button = random.choice(list(self.buttons.keys()))
                self.press(some_button, who_='machine')

    def mark_button(self, btt_number, who_):
        font_tuple = (FONT_NAME, 100, 'bold')
        if who_ == 'player':
            color = BLUE
            mark = 'O'
        else:
            color = RED
            mark = 'X'
        self.buttons[btt_number].config(text=mark, font=font_tuple, justify='center', fg=color)
        self.buttons.pop(btt_number)
        self.score.update({btt_number: mark})

        victory_y_n, winner = self.check_three_in_line()

        if victory_y_n:
            self.end_game(winner)
        elif len(self.buttons) == 0:
            self.end_game('nobody')
        else:
            if self.player_goes is True:
                self.player_goes = False
                self.machine_turn()
            else:
                self.player_goes = True
                self.player_turn()

    def check_three_in_line(self):
        three_in_line = False
        for mark in ['X', 'O']:
            for rng in WIN_RANGES:
                combo3 = [self.score[str(rank)] for rank in rng]
                if combo3.count(mark) == 3:
                    winner = mark
                    three_in_line = True
                    break
        if three_in_line is False:
            return False, ''
        else:
            if winner == 'O':
                return True, 'player'
            else:
                return True, 'machine'

    def check_two_in_line(self, mark):
        two_in_line = False
        for rng in WIN_RANGES:
            combo2 = [self.score[str(rank)] for rank in rng]
            if combo2.count(mark) == 2 and combo2.count(0) == 1:
                two_in_line = True
                break
        if not two_in_line:
            return False, ''
        else:
            find_gap = combo2.index(0)
            find_button = rng[find_gap]
            return True, str(find_button)

    def press(self, btt_number, who_='player'):
        self.toggle_buttons('disabled')
        self.mark_button(btt_number, who_=who_)

    def end_game(self, winner_):
        if winner_ == 'player':
            self.game_label.config(text='You won! Press "reset" to go again.')
        elif winner_ == 'nobody':
            self.game_label.config(text='A tie it is! Press "reset" to go again.')
            self.icon_label.config(text=" ", font=(FONT_NAME, 48, "bold"), fg=BLUE)
        else:
            self.game_label.config(text='You lost! Press "reset" to go again.')
