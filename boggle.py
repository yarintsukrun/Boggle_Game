from ex11_utils import *
from boggleGUI import *
from ModelBoggle import *
import boggle_board_randomizer


class BoggleTheController:
    """"
    This is the controller for controlling the GUI and the Model for the game Boggle"""
    def __init__(self, file):
        """
        will implement the model and the GUI, and will configure the buttons
        of game
        """
        # saving the file
        self.file = file
        # saving the board
        board = boggle_board_randomizer.randomize_board()
        # saving all the possible paths for finding a word
        all_solutions = max_paths_for_words(board, self.file)
        # saving all the possible words in the board
        all_words = all_available_words(board, all_solutions)
        # implement the model and the GUI
        self.model = ModelOfBoggle(board, all_solutions, all_words)
        self.gui = BoggleGUI(all_words)
        self.gui.grid_board(board)

        # configuring the buttons
        self.gui.start_button.configure(command=self.start_game)
        self.gui.one_more_try.configure(command=self.play_again)
        for a_button in self.gui.buttons:
            action = self.model.make_action(a_button)
            if action is not None:
                self.make_action(action, a_button)

    def make_action(self, action, a_button):
        """
        this func will determent the action for every button and its use
        :param action: type of action
        :param a_button: name of the button
        :return: None
        """
        # getting the button object
        button_obj = self.gui.buttons[a_button]

        def change_cur_word():
            """
            this inner function will be called from the letter buttons and delete button for
            adding or removing a letter for the current word.
            :return: None
            """
            # if the button is a letter button
            if len(a_button) == 3 and a_button[1] == ",":
                index = tuple((int(a_button[0]), int(a_button[2])))
                # adding a letter for the current word at the model
                self.model.set_solution("add", index)
                # update the cur word at gui
                self.gui.cur_word.append(button_obj["text"])
                # updating the current word display at gui
                self.gui.current_word.configure(text="".join(self.gui.cur_word))
            # if press del
            if a_button == "DEL":
                if len(self.gui.cur_word) > 0:
                    # updating the screen and the cur word at gui
                    self.gui.cur_word.pop()
                    self.gui.current_word.configure(text="".join(self.gui.cur_word))
                    # updating the model
                    self.model.set_solution(a_button)
        # if press hint
        if a_button == "HINT":
            button_obj.configure(command=self.hint)
        # if press char or del
        elif action == "add_letter" or action == "DEL":
            button_obj.configure(
                command=change_cur_word)
        elif action == "CHECK":
            button_obj.configure(command=self.check_result)

    def play_again(self):
        """
        this function will run the game again by destrying the main window and making a new window
        with a new board
        """
        new_game = BoggleTheController(self.file)
        self.gui.main_window.destroy()
        new_game.run()

    def start_game(self):
        """ will close the menu window and will open the game frame
        """
        self.gui.start_frame.forget()
        self.gui.game_frame.tkraise()
        self.gui.game_frame.pack()
        self.gui.update_timer()

    def run(self):
        """ will start the game"""
        self.gui.run()

    def check_result(self):
        """
        this function will check if the user's solution (the current word) is valid.
        if the solution is valid the function will update the score and the list of answers
        :return:
        """
        check = self.gui.buttons["CHECK"]
        # if the solution is valid
        if self.model.check_for_solution():
            word = self.gui.get_display_cur_word()
            check.configure(activebackground="green")
            check.flash()
            check.configure(activebackground="slateblue")
            self.gui.used_word.append("".join(self.gui.cur_word))
            self.gui.listbox.insert(tki.END, f"{word}")
            self.gui.score_label.configure(text="SCORE: " + str(self.model.score))
            self.gui.cur_word.clear()
            self.gui.current_word.configure(text="".join(self.gui.cur_word))
        else:
            check.configure(activebackground="red")
            check.flash()
            check.configure(activebackground="slateblue")
        if len(self.gui.all_words_solutions) == len(self.gui.used_word):
            self.gui.finish_game()

    def hint(self):
        """if there is score to "pay",
        flashes the button that you can use green,
         else flashes the hint button red"""
        if self.model.score >= 3 and len(self.gui.all_words_solutions) != len(self.gui.used_word):
            self.model.score -= 3
            self.gui.score_label.configure(text="SCORE: " + str(self.model.score))
            index = self.model.hint()
            # if the model.hint return a char index
            if index[1] == ",":
                char = self.gui.buttons[index]
                char.configure(activebackground="blue")
                char.flash()
                char.configure(activebackground="slateblue")
            # the model hint return the button CHECK/DEL
            else:
                self.gui.buttons[index].configure(activebackground="blue")
                self.gui.buttons[index].flash()
                self.gui.buttons[index].configure(activebackground="slateblue")

        else:
            # flashes red if there is no score to "pay" for the hint
            self.gui.buttons["HINT"].configure(activebackground="red")
            self.gui.buttons["HINT"].flash()
            self.gui.buttons["HINT"].configure(activebackground="slateblue")


def max_paths_for_words(board: Board, words: Iterable[str]) -> List[Path]:
    """
    :param board:
    :param words:
    :return: all possible paths for all words in the game (will return duplications)
    """
    all_paths = []
    for word in words:
        for a_row in range(len(board)):
            for a_col in range(len(board[0])):
                if board[a_row][a_col][0] == word[0]:
                    the_path = ex11_utils.find_path_for_word(a_row, a_col, "", [], board, word, [], [])
                    if the_path is not None:
                        for path in the_path:
                            all_paths.append(path)
    return all_paths


def all_available_words(board, solutions):
    """
    This function will filter the paths that leads to the same words for checking how much
    words are hidden in the board
    :param board:
    :param solutions:
    :return: list words that are hidden in the board
    """
    duplicated_list = []
    filtered_list = []
    for path in solutions:
        duplicated_list.append(is_valid_path(board, path, new_file))
    for word in duplicated_list:
        if word not in filtered_list:
            filtered_list.append(word)
    return filtered_list


if __name__ == '__main__':
    f = list(open("boggle_dict.txt", "r"))
    new_file = []
    for word in f:
        new_file.append(word[:-1])
    controller = BoggleTheController(new_file)
    controller.run()
