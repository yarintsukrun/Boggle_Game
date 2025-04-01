import ex11_utils
import random


class ModelOfBoggle:
    """
    This is the model for the game. in this class all the methods are for making the logic
    calculations and decision for the game.
    """

    def __init__(self, board, all_solutions, all_words):
        """
        construction the initial data of the game.
        :param board: saving the board.
        :param all_solutions: saving the paths for all the solutions.
        :param all_words:  saving the words for all the solutions.
        """
        self.all_words = all_words
        self.board = board
        self.all_solutions = all_solutions
        self.cur_path = []
        self.my_solutions = []
        self.cur_word = ""
        self.score = 0
        self.hint_path = None

    def set_solution(self, action_str: str, index=None):
        """ updating the current path and current word by the type of the action - delete and add"""
        if action_str == "DEL" and len(self.cur_path) > 0:
            self.cur_path.pop()
        elif action_str == "add":
            row, col = index
            self.cur_path.append((row, col))

    def check_for_solution(self):
        """
        checking if the current path is a solution by using the is_valid_path function and checking if
        the solution is not used and if it is in the all possible solution list.
        :return: bool
        """
        word_check = ex11_utils.is_valid_path(self.board, self.cur_path, self.all_words)
        if word_check is not None and self.cur_path in self.all_solutions and word_check not in self.my_solutions:
            self.score += len(self.cur_path) ** 2
            self.my_solutions.append(word_check)
            self.all_solutions.remove(self.cur_path)
            self.cur_path.clear()
            return True
        return False

    def hint(self):
        """getting the user an index that can be part of a solution,
        if the current path is already a solution return CHECK
        if the current path cannot assemble a valid solution return DEL"""
        len_path = len(self.cur_path)
        # the current path is empty
        if self.cur_path == []:
            self.hint_path = random.choice(self.all_solutions)
            index = str(self.hint_path[len_path][0]) + "," + str(self.hint_path[len_path][1])
            return index
        # if the current path is a valid solution return CHECK
        word_check = ex11_utils.is_valid_path(self.board, self.cur_path, self.all_words)
        if word_check is not None and self.cur_path in self.all_solutions and word_check not in self.my_solutions:
            return "CHECK"
        # if the current path is part of a solution and the solution is not used
        # then return the next index of the solution
        for path in self.all_solutions:
            hint_check = ex11_utils.is_valid_path(self.board, path, self.all_words)
            if self.cur_path == path[:len_path] and hint_check not in self.my_solutions:
                len_path = len(self.cur_path)
                index = str(path[len_path][0]) + "," + str(path[len_path][1])
                return index
        # if there is no solution for the current path return DEL
        return "DEL"

    def make_action(self, text):
        """ arranging the buttons for types of actions"""
        if "," in text and len(text) == 3:
            return "add_letter"
        else:
            return text
