import tkinter as tki

GAME_TIME = 180
BUTTON_HOVER_COLOR = "gray"
REGULAR_COLOR = "lightgray"
BUTTON_ACTIVE_COLOR = "slateblue"
BUTTON_STYLE = {"font": ("courier", 40),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR,
                "width": 3}

FRAME_STYLE = {"bg": REGULAR_COLOR, "highlightbackground": REGULAR_COLOR, "highlightthickness": 5}


class BoggleGUI:
    """
    This class is responsible for creating all the visual and graphic parts of the game.
    """
    def __init__(self, all_words_solutions):
        """ construction the initial graphic parts of the game."""
        # game vars
        self.buttons = {}
        self.all_words_solutions = all_words_solutions
        self.cur_word = []
        self.used_word = []
        # game window
        root = tki.Tk()
        self._main_window = root
        self._main_window.title("boogle")
        self._main_window.resizable(False, False)
        self.framing_playable_window()
        self.get_display_cur_word()
        self.display_used_word()
        self.time()
        self.time_remaining = GAME_TIME

        # creating buttons : hint del check
        self.game_buttons()

        # creating the start, game, frame
        self.game_menu()

        # creating game over frame
        self.game_over_frames()

    def game_over_frames(self):
        """this function creates the frame that pops when the game is over.
        the frame contains form top to bottom:
        1. Game Over in big words
        2. the finished score
        3. scroll bar with the word that the board contains
        4. play/exit buttons"""
        self.game_over_frame = tki.Frame(self._main_window, **FRAME_STYLE)
        self.game_over = tki.Label(self.game_over_frame, bg=REGULAR_COLOR, text=""
                                                                                "GAME OVER",
                                   font=("courier", 40, "bold"))
        self.all_words_frame = tki.Frame(self.game_over_frame, **FRAME_STYLE)

        self.do_you_want = tki.Frame(self.game_over_frame, **FRAME_STYLE)
        self.score = tki.Label(self.game_over_frame, bg=REGULAR_COLOR, text=""
                                                                            "You finished the game with " +
                                                                            self.score_label["text"] + "\n",
                               font=("courier", 17))
        self.start_again = tki.Label(self.do_you_want, bg=REGULAR_COLOR, text=""
                                                                              "Do you want to play again? ",
                                     font=("courier", 17), fg="green")

        self.one_more_try = tki.Button(self.do_you_want, BUTTON_STYLE, text="Play!")
        self.buttons["PLAY AGAIN"] = self.one_more_try
        self.no_one_more_try = tki.Button(self.do_you_want, BUTTON_STYLE, text="Exit",
                                          command=self._main_window.destroy)

        self.solutions = tki.Label(self.game_over_frame, **FRAME_STYLE,
                                   font=("courier", 12, "bold"), fg="red",
                                   text="These are all " + str(len(self.all_words_solutions))
                                        + " words that were hidden in the board:")
        self.listbox_result = tki.Listbox(self.all_words_frame)
        self.scrollbar_result = tki.Scrollbar(self.all_words_frame)
        for word in self.all_words_solutions:
            self.listbox_result.insert(tki.END, word)
        self.listbox_result.config(yscrollcommand=self.scrollbar_result.set)
        self.scrollbar_result.config(command=self.listbox_result.yview)

    def game_menu(self):
        """this function creates the start game frame,
        the frame contains from top to bottom:
        1. the title of the game and the creators of the program
        2. the number of hidden word in the board
        3.the rules of the game and a start button"""

        self.start_frame = tki.Frame(self._main_window, **FRAME_STYLE)
        self.start_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # making names frame
        self.name_frame = tki.Frame(self.start_frame,
                                    **FRAME_STYLE)
        self.name_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # making welcome label
        self.welcome_label = tki.Label(self.name_frame,
                                       font=("courier", 30, "bold"),
                                       height=2,
                                       bg=REGULAR_COLOR,
                                       fg="Green",
                                       text="THE BOGGLE GAME")
        self.welcome_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # make name label
        self.name_label = tki.Label(self.name_frame,
                                    font=("courier", 15),
                                    height=2,
                                    bg=REGULAR_COLOR,
                                    text=" BY Ram Minsky and Yarin Tsukrun")
        self.name_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # telling user to press start
        self.press_start_label = tki.Label(self.name_frame,
                                           font=("courier", 18),
                                           height=5,
                                           fg="red",
                                           bg=REGULAR_COLOR,
                                           text="There is " + str(
                                               len(self.all_words_solutions)) + " Hidden words in this board, \n "
                                                                                "GO FIND THEM ALL!! \n\n"
                                                                                "Press START to Begin")
        self.press_start_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # rules label
        self.press_start_label = tki.Label(self.name_frame,
                                           font=("courier", 10),
                                           height=8,
                                           bg=REGULAR_COLOR,
                                           text="RULES: \n"
                                                "1. Each letter after the first must be \n horizontal, vertical, "
                                                "or diagonal neighbor of the one before it.\n"
                                                "2. No individual letter cube may be used more than once in a word. \n"
                                                "3. Each word you find will reward you with its length squared in "
                                                "points.\n"
                                                "4. Using a HINT will cost you 3 points")
        self.press_start_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # creating start button
        self.start_button = tki.Button(self.name_frame, **BUTTON_STYLE, text="START")
        self.start_button.pack()

    def framing_playable_window(self):
        """this function create the actual gaming frame,
        the frame contains -

        on the left side:
        1. on the top a display for the chars that the user choose
        2. in the middle button that shows the board of the game
        3. on the bottom button for check word, delete char, getting hint

        on the right side:
        1. on the top the current score and the remaining time
        2. the solutions found on the board"""

        # create window borders
        self.game_frame = tki.Frame(self._main_window, **FRAME_STYLE)

        # frame for board and current word
        self._left_frame = tki.Frame(self.game_frame, **FRAME_STYLE)
        self._left_frame.pack(side=tki.LEFT, fill=tki.BOTH)

        # creating frame for time and used words
        self._right_frame = tki.Frame(self.game_frame, **FRAME_STYLE)
        self._right_frame.pack(side=tki.RIGHT,
                               fill=tki.BOTH,
                               expand=True, )

        # creating frame for time and score
        self.score_time_frame = tki.Frame(self._right_frame, **FRAME_STYLE)
        self.score_time_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=False)

        # creating used word frame
        self._solutions_frame = tki.Frame(self._right_frame, bg=REGULAR_COLOR)
        self._solutions_frame.pack(fill=tki.BOTH, expand=True)

        # creating a scroll bar for the word that the player found
        self.result_frame = tki.Frame(self._right_frame)
        self.result_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=False)
        self.scroll_bar()

        # creating frame for check, del, hint,start
        self._game_buttons_frame = tki.Frame(self._right_frame, **FRAME_STYLE)
        self._game_buttons_frame.pack(fill="y")

        self.current_word = tki.Label(self._left_frame,
                                      font=("courier", 30),
                                      text="",
                                      bg="#9DCA9F",
                                      width=15,
                                      height=2,
                                      relief="ridge")
        self.current_word.pack(pady=45)

        # making a label for the score
        self.score_label = tki.Label(self.score_time_frame,
                                     font=("courier", 22, "bold"),
                                     height=2,
                                     bg=REGULAR_COLOR,
                                     fg="Green",
                                     text="SCORE: " + str(0))
        self.score_label.pack()

    def scroll_bar(self):
        def scroll_list(event):
            self.listbox.yview_scroll(-1 * (event.delta // 120), "units")

        self.scrollbar = tki.Scrollbar(self.result_frame, orient=tki.VERTICAL)
        # Create a listbox with the scrollbar attached
        self.listbox = tki.Listbox(self.result_frame, yscrollcommand=self.scrollbar.set, font=15, bg=REGULAR_COLOR)
        # Bind the mouse wheel event to the listbox
        self.listbox.bind("<MouseWheel>", scroll_list)
        # Configure the scrollbar to control the listbox
        self.scrollbar.config(command=self.listbox.yview)
        # Pack the listbox and scrollbar in the window
        self.listbox.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
        self.scrollbar.pack(side=tki.RIGHT, fill=tki.Y)

    def get_display_cur_word(self):
        """gets the word that displays on the screen"""
        return self.current_word["text"]

    def run(self):
        self._main_window.mainloop()

    def grid_board(self, board):
        """creates grid of buttons that contains the boards chars"""

        # create label for the board
        self._board_label = tki.Label(self._left_frame,
                                      bg=REGULAR_COLOR,
                                      width=7,
                                      relief="ridge")

        self._board_label.pack()

        # create grid of the board
        for i in range(len(board)):
            for j in range(len(board[0])):
                text = board[i][j]
                row = str(i)
                col = str(j)
                index = row + "," + col
                button = tki.Button(self._board_label,
                                    **BUTTON_STYLE,
                                    text=text)
                button.grid(row=i, column=j)
                self.buttons.update({index: button})

    def display_used_word(self):
        """shows the used word in the down right side"""

        self.used_words = tki.Label(self._solutions_frame, font=("courier", 15), bg=REGULAR_COLOR,
                                    width=15, height=2, text="Words Found:")
        self.used_words.pack(side=tki.TOP)

    def time(self):
        """shows the time for the game in the top right side"""
        self.timer = tki.Label(self.score_time_frame,
                               font=("courier", 15, "bold"),
                               height=2,
                               fg="#cc0d00",
                               bg=REGULAR_COLOR,
                               text="TIME: 00:03:00")
        self.timer.pack(side=tki.BOTTOM)

    def update_timer(self):
        """the functions count the time for the game,
         when the time is up the function will change
          the frame from the game frame to game over frame"""

        # updates and countdown the time off the game
        if self.time_remaining > 0:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.timer.config(text=f"Time Remaining: {minutes:02d}:{seconds:02d}")
            self.time_remaining -= 1
            self._main_window.after(1000, self.update_timer)
            # Schedule the function to run again in 1000ms (1 second)

        else:
            # when the time is up, finnish games and switch to the game over frame
            self.finish_game()

    def game_buttons(self):
        """creates the buttons for the game frame:
        check word, delete char and get hint"""
        game_buttons_frame = tki.Frame(self._left_frame)
        BUTTON_STYLE["font"] = ("courier", 17)
        BUTTON_STYLE["width"] = 5

        # creating start button
        check_button = tki.Button(game_buttons_frame, **BUTTON_STYLE, text="CHECK")
        check_button.grid(row=0, column=0)
        self.buttons.update({"CHECK": check_button})

        # creating delete button
        del_move = tki.Button(game_buttons_frame, **BUTTON_STYLE, text="DEL")
        del_move.grid(row=0, column=1)
        self.buttons.update({"DEL": del_move})

        # creating hint button
        hint = tki.Button(game_buttons_frame, **BUTTON_STYLE, text="HINT")
        hint.grid(row=0, column=2)
        self.buttons.update({"HINT": hint})
        game_buttons_frame.pack(side=tki.BOTTOM)

    def finish_game(self):
        """ Running a sequence of actions to end the game"""
        self.time_remaining = 0
        self.timer.config(text="Time's up!")
        self.game_frame.forget()
        self.game_over_frame.pack()
        self.game_over.pack()
        self.score.configure(text="You finished the game with " + self.score_label["text"] + "\n")
        self.score.pack()
        self.solutions.pack()
        self.listbox_result.pack(side=tki.LEFT, fill=tki.BOTH)
        self.scrollbar_result.pack(side=tki.RIGHT, fill=tki.BOTH)
        self.start_again.pack()
        self.one_more_try.pack()
        self.no_one_more_try.pack()
        self.all_words_frame.pack()
        self.do_you_want.pack()
        self.listbox_result.pack(side=tki.LEFT, fill=tki.BOTH)
        self.scrollbar_result.pack(side=tki.RIGHT, fill=tki.BOTH)

    @property
    def main_window(self):
        return self._main_window
