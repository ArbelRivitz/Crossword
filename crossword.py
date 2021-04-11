import sys
import os

PARAMETER_ERROR = 'ERROR: invalid number of parameters. Please enter word_file' \
                  ' ' \
                  'matrix_file output_file directions.'
WORD_ERROR = 'ERROR: Word file '
MATRIX_ERROR = 'ERROR: Matrix file '
MISSING_ERROR = ' does not exist.'
DIRECTION_ERROR = 'ERROR: invalid directions.'


def convert_matrix(filename):
    """This function receives a file with the matrix and converts it to list
     that contains each line from the matrix in a separate list. Each list
     contains only the letters from the matrix."""
    matrix_list = []
    for line in filename:
        corrected_string = (line.rstrip()).replace(",", "").lower()  # converts
        # to lower case, removes the '\n' between lines and the ','.
        matrix_list.append(list(corrected_string))
    return matrix_list


def convert_words(textfilename):
    """This function receives a file containing words and converts it to a list
    of words"""
    words_lst = []
    for line in textfilename:
        word = line.rstrip().lower()
        words_lst.append(word)
    return words_lst


def choose_direction(direction, my_matrix):
    """This function receives the search direction and the matrix, it takes the
     list of the matrix and converts it into separate strings according to the
     search direction. Then it adds all the strings to one list and returns the
     list."""
    final_str_lst = []
    direction_set = set(direction)  # converts the directions to a set in order
    # to eliminate double letters
    for char in direction_set:
        if char == 'u':
            strs_in_direction = down_to_up(my_matrix)
        elif char == 'd':
            strs_in_direction = up_to_down(my_matrix)
        elif char == 'r':
            strs_in_direction = left_to_right(my_matrix)
        elif char == 'l':
            strs_in_direction = right_to_left(my_matrix)
        elif char == 'w':
            strs_in_direction = lower_left_to_right(my_matrix)
        elif char == 'x':
            strs_in_direction = lower_right_to_left(my_matrix)
        elif char == 'y':
            strs_in_direction = upper_left_to_right(my_matrix)
        elif char == 'z':
            strs_in_direction = upper_right_to_left(my_matrix)
        for string in strs_in_direction:
            final_str_lst.append(string)
    return final_str_lst


def left_to_right(matrix):
    matrix_string = []
    for lst in matrix:
        string = ''  # so each iteration has an empty string
        string = ''.join(lst)
        matrix_string.append(string)
    return matrix_string


def right_to_left(matrix):
    return change_direction_str(left_to_right(matrix))


def up_to_down(matrix):
    vertical_str = []
    for column in range(len(matrix[0])):
        string = ''
        for place in range(len(matrix)):
            string += matrix[place][column]
        vertical_str.append(string)
    return vertical_str


def down_to_up(matrix):
    return change_direction_str(up_to_down(matrix))


def in_diagonal(matrix, first_loop, second_loop):
    str_list = []
    for item in range(first_loop + second_loop - 1):
        temp_str = ''
        sum_item = item
        for lst in range(second_loop):
            for place in range(first_loop):
                if lst + place == sum_item:
                    temp_str += matrix[lst][place]
            sum_item += 2
        if temp_str != '':
            str_list.append(temp_str)
    return str_list


def upper_left_to_right(matrix):
    num_of_row = len(matrix[0])
    num_of_column = len(matrix)
    str_list = []
    for item in range(num_of_row + num_of_column - 1):
        temp_str = ''
        sum_item = item
        for lst in range(num_of_column):
            for place in range(num_of_row):
                if lst + place == sum_item:
                    temp_str += matrix[lst][place]
            sum_item += 2
        if temp_str != '':
            str_list.append(temp_str)

    for item in range(num_of_row + num_of_column - 1):
        temp_str = ''
        sum_item = item
        for place in range(num_of_row):
            for lst in range(num_of_column):
                if lst + place == sum_item:
                    temp_str += matrix[lst][place]
            sum_item += 2
        if temp_str != str_list[0] and temp_str != '':
            str_list.append(temp_str)
    return str_list


def upper_right_to_left(matrix):
    num_of_row = len(matrix[0])
    num_of_column = len(matrix)
    str_list = []
    for item in range(num_of_row + num_of_column - 1):
        temp_str = ''
        for lst in range(num_of_column):
            for place in range(num_of_row):
                if lst + place == item:
                    temp_str += matrix[lst][place]
        str_list.append(temp_str)
    return str_list


def lower_left_to_right(matrix):
    return change_direction_str(upper_right_to_left(matrix))


def lower_right_to_left(matrix):
    return change_direction_str(upper_left_to_right(matrix))


def change_direction_str(str_lst):
    """Receives a list of strings in one direction and converts each string to
    a sting in the other direction"""
    backwards_str = []
    for string in str_lst:
        backwards_str.append(string[::-1])
    return backwards_str


def search(wordslst, strlst):
    """This function receives the list of words and the list of strings
    (strings by the different search directions) and returns a list of tuples
    each containing a word and the number of times it appeared in the search.
    """
    word_appearance_list = {}
    lst = []
    for word in wordslst:
        num_of_appearance = 0
        for string in strlst:
            if word in string:
                num_of_appearance += 1
                place = string.find(word)
                updated_str = string[place + 1:]
                while word in updated_str:  # in case word more than once in
                    # string we cut the first letter off the string (so we
                    # don't count the same appearance twice) and check if the
                    # word appears again.
                    place = updated_str.find(word)
                    updated_str = updated_str[place + 1:]
                    num_of_appearance += 1
        if num_of_appearance > 0:  # To eliminate adding words that don't
            # appear.
            word_appearance_list.update({word: num_of_appearance})
    sorted_keys = sorted(word_appearance_list.keys())  # organise the words
    # alphabetically
    for index in sorted_keys:
        lst.append((index, str(word_appearance_list[index])))
    return lst


def main(matrix, words, direction, output):
    """Our main function, it creates the final list of words using the search
    function and then writes them to the output file."""
    final_lst = search(convert_words(words),
                       choose_direction(direction, convert_matrix(matrix)))
    for tup in final_lst:
        if tup != final_lst[0]:
            output.write('\n')
        string = ','.join(tup)
        output.write(string)


def convert_args(sys_argv, sys_word, sys_mat, sys_directions,
                 wanted_directions):
    """This function returns checks if the input from the cmd is correct, if it
    isn't it prints an error otherwise it returns True."""
    if len(sys_argv) != 5:
        print(PARAMETER_ERROR)
    elif os.path.isfile(sys_word) is False:
        print(WORD_ERROR + sys_word + MISSING_ERROR)
    elif os.path.isfile(sys_mat) is False:
        print(MATRIX_ERROR + sys_mat + MISSING_ERROR)
    elif directions_validity(sys_directions, wanted_directions) is False:
        print(DIRECTION_ERROR)
    else:
        return True


def directions_validity(directions, wanted_directions):
    for char in directions:
        if char not in wanted_directions:
            return False


if __name__ == "__main__":
    if convert_args(sys.argv, sys.argv[1], sys.argv[2], sys.argv[4],
                    'udlrwxyz') is True:
        words_link = open(sys.argv[1], 'r')
        matrix_link = open(sys.argv[2], 'r')
        output_file = open(sys.argv[3], 'w')
        search_direction = sys.argv[4]
        main(matrix_link, words_link, search_direction, output_file)
