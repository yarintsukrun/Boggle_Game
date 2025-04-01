from typing import List, Tuple, Iterable, Optional
Board = List[List[str]]
Path = List[Tuple[int, int]]

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    this function will build a word from the path and the board, and will check if that word
    is in the words list.
    :return: the word if the path is valid, None if not
    """
    # finding the size of the board:
    ROW_NUM_BOARD = len(board)
    COL_NUM_BOARD = len(board[0])

    new_word = ""
    path_index = 0
    for row, col in path:
        # if the path is out of the board
        if not 0 <= row < ROW_NUM_BOARD or not 0 <= col < COL_NUM_BOARD:
            return None
        if path_index != 0:
            # If the two letters are not next to each other
            if abs(path[path_index][0] - path[path_index - 1][0]) > 1 or abs(path[path_index][1] - path[path_index - 1][1]) > 1 or path[path_index] == path[path_index - 1]:
                return None
        path_index += 1
        # building the word
        new_word = new_word + board[row][col]
    # checking if the word is in words
    if new_word in words:
        return new_word
    return None


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    :return: A list of all valid paths of length n describing words in the collection of words.
    """
    # finding the size of the board:
    ROW_NUM_BOARD = len(board)
    COL_NUM_BOARD = len(board[0])

    # collecting all letter buttons that have more than one letter such as 'QU'(exceptions letters)
    exceptions_letters = []
    for _ in board:
        for item in _:
            if len(item) != 1:
                exceptions_letters.append((item, len(item)))
    words_of_len_n = []

    # Filter all words without path length of n:
    for word in words:
        len_word = len(word)
        # for every exception letter
        for exc_item in exceptions_letters:
            string, length = exc_item
            # if the word starting with that exception letter and the path length is valid
            if string == word[:length] and len_word - length == n - 1:
                words_of_len_n.append(word)
        # if the word's length is valid
        if len_word == n:
            words_of_len_n.append(word)
    result_length_path = []

    # starting the backtracking for every valid word with path length of n:
    for a_word in words_of_len_n:
        # for every square in the board
        for a_row in range(ROW_NUM_BOARD):
            for a_col in range(COL_NUM_BOARD):
                the_path = find_path_for_word(a_row, a_col, "", [], board, a_word, [], [])
                if the_path is not None:
                    for path in the_path:
                        if len(path) == n:
                            result_length_path.append(path)
    return result_length_path


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    :return: all possible paths to a word of length n
    """
    # finding the size of the board:
    ROW_NUM_BOARD = len(board)
    COL_NUM_BOARD = len(board[0])

    # Filter all words without length of n:
    words_of_len_n = []
    for word in words:
        if len(word) == n:
            words_of_len_n.append(word)
    result_length_n = []

    # starting the backtracking for every valid word with n length
    for a_word in words_of_len_n:
        for a_row in range(ROW_NUM_BOARD):
            for a_col in range(COL_NUM_BOARD):
                the_path = find_path_for_word(a_row, a_col, "", [], board, a_word, [], [])
                if the_path is not None:
                    for path in the_path:
                        result_length_n.append(path)
    return result_length_n


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    this function will find the maximum paths for winning a game by running over all the
    possible paths for every word and picking the longest one.
    :param board:
    :param words:
    :return: list of paths
    """
    # finding the size of the board:
    ROW_NUM_BOARD = len(board)
    COL_NUM_BOARD = len(board[0])

    all_dict_paths = {}
    for word in words:
        for a_row in range(ROW_NUM_BOARD):
            for a_col in range(COL_NUM_BOARD):
                # if the word starting with this letter of the board
                if board[a_row][a_col][0] == word[0]:
                    # calling to a recursive function for finding every solution for this word
                    the_path = find_path_for_word(a_row, a_col, "", [], board, word, [], [])
                    if the_path != [] and the_path is not None:
                        for path in the_path:
                            # filtering the duplicated ones with the length of the path
                            if word not in all_dict_paths or len(path) > len(all_dict_paths[word]):
                                all_dict_paths[word] = path
    return list(all_dict_paths.values())


def find_path_for_word(cur_row, cur_col, cur_word, cur_path, board, word, result, used_indexes):
    """
    This function will find all the paths in the board that are starting from this particular
    location (row and col) without using the same indexes for the same word
    :param cur_row: starting location    :param cur_col: starting location
    :param cur_word: current word that is bein assembled
    :param cur_path: current path that is bein assembled
    :param board: the board
    :param word: the desired word
    :param result: all paths for this word
    :param used_indexes: used index for the word to not repeat them
    :return: result, all paths for this word
    """
    ROW_NUM_BOARD = len(board)
    COL_NUM_BOARD = len(board[0])

    # return if we already used this index
    if (cur_row, cur_col) in used_indexes:
        return

    # updating the indicators
    used_indexes.append((cur_row, cur_col))
    cur_path.append((cur_row, cur_col))
    cur_word = cur_word + board[cur_row][cur_col]

    # if we succeed and reached to the word
    if cur_word == word:
        result.append(cur_path[:])
        cur_path.pop()
        used_indexes.pop()
        return result

    # if the word that is being build is not starting like the desired word we go back
    if cur_word not in word:
        cur_path.pop()
        used_indexes.pop()
        return

    # RECURSIVE CALLS:
    # if we can go a row above:
    if cur_row != 0:
        # if we can go to the left corner:
        if cur_col != 0:
            find_path_for_word(cur_row - 1, cur_col - 1, cur_word, cur_path, board, word, result, used_indexes)
        # if we can go to the right corner:
        if cur_col != COL_NUM_BOARD - 1:
            find_path_for_word(cur_row - 1, cur_col + 1, cur_word, cur_path, board, word, result, used_indexes)
        # you can go up
        find_path_for_word(cur_row - 1, cur_col, cur_word, cur_path, board, word, result, used_indexes)

    # if we can go a row beneath:
    if cur_row != ROW_NUM_BOARD - 1:
        # if we can go to the left corner:
        if cur_col != 0:
            find_path_for_word(cur_row + 1, cur_col - 1, cur_word, cur_path, board, word, result, used_indexes)
        # if we can go to the right corner:
        if cur_col != COL_NUM_BOARD - 1:
            find_path_for_word(cur_row + 1, cur_col + 1, cur_word, cur_path, board, word, result, used_indexes)
        # you can go down
        find_path_for_word(cur_row + 1, cur_col, cur_word, cur_path, board, word, result, used_indexes)

    # if we can go left and len(result) == 0:
    if cur_col != 0:
        find_path_for_word(cur_row, cur_col - 1, cur_word, cur_path, board, word, result, used_indexes)
    if cur_col != COL_NUM_BOARD - 1:
        find_path_for_word(cur_row, cur_col + 1, cur_word, cur_path, board, word, result, used_indexes)

    # backtracking
    cur_path.pop()
    used_indexes.pop()
    return result
