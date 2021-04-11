###############################################################################
# FILE: ex4.py
# WRITER: Lior_Fishman, Arbel Rivitz, liorf, Arbelr, 208305797, 207904632
# EXERCISE: intro2cs ex5 2017-2018
# DESCRIPTION: This exercise searches for words from a given list in a given 3d
# matrix.
###############################################################################


import crossword
import sys

ASTERISK = ['*', '*', '*']


def convert_3d_matrix(filename):
    """Receives a matrix file, using the crossword.convert_matrix function it
    separates it to different matrixes"""
    converted_matrix = crossword.convert_matrix(filename)
    converted_matrix.append(ASTERISK)
    final_matrix_lst = []
    sub_lst = []
    for lst in converted_matrix:
        if lst != ASTERISK:
            sub_lst.append(lst)
        else:
            final_matrix_lst.append(sub_lst)
            sub_lst = []
    return final_matrix_lst


def choose_3d_direction(direction, matrix):
    """This function receives the search direction and the converted matrix,
    and returns updated matrixes in the correct search directions."""
    my_matrix = convert_3d_matrix(matrix)
    final_mat_lst = []
    direction_set = set(direction)
    for char in direction_set:
        if char == 'a':
            updated_matrix = my_matrix
        elif char == 'b':
            updated_matrix = convert_b(my_matrix)
        else:
            updated_matrix = convert_c(my_matrix)
        for mat in updated_matrix:
            final_mat_lst.append(mat)
    return final_mat_lst


def convert_b(matrix):
    b_lst = []
    for lines in range(len(matrix[0])):
        inner_lst = []
        for inner in matrix:
            inner_lst.append(inner[lines])
        b_lst.append(inner_lst)
    return b_lst


def convert_c(matrix):
    c_lst = []
    for columns in range(len(matrix[0])):
        sub_lst = []
        for inner in matrix:
            sub_sub_lst = []
            for rows in range(len(inner)):
                sub_sub_lst.append(inner[rows][columns])
            sub_lst.append(sub_sub_lst)
        c_lst.append(sub_lst)
    return c_lst


def main(matrix, words, direction, output):
    """This is our main function. It starts by converting the words to a list
    and converting the matrix file to a list of separated matrixes using the
    choose_3d_direction function and then using the choose_direction function
    from the crossword file converts each matrix to strings in all the search
    directions. Then using the search function from crossword checks if any of
    the words are in the matrix strings and updates a dictionary."""
    converted_words = crossword.convert_words(words)
    final_lst = []
    tuple_dict = {}
    matrix_lst = choose_3d_direction(direction, matrix)
    for single_mat in matrix_lst:
        matrix_string_lst = crossword.choose_direction('udlrwxyz', single_mat)
        searched_lst = crossword.search(converted_words, matrix_string_lst)
        for tup in searched_lst:  # adds tuples from the different matrixes to
            # the dictionary
            if tup[0] in tuple_dict.keys():
                tuple_dict[tup[0]] = int(tuple_dict[tup[0]]) + int(tup[1])
            else:
                tuple_dict.update({tup})
    sorted_keys = sorted(
        tuple_dict.keys())  # organise the words alphabetically
    for i in sorted_keys:
        final_lst.append((i, str(tuple_dict[i])))
    for tup in final_lst:  # writes to file
        if tup != final_lst[0]:
            output.write('\n')
        string = ','.join(tup)
        output.write(string)


if __name__ == '__main__':
    if crossword.convert_args(sys.argv, sys.argv[1], sys.argv[2], sys.argv[4],
                              'abc') is True:
        words_link = open(sys.argv[1], 'r')
        matrix_link = open(sys.argv[2], 'r')
        output_file = open(sys.argv[3], 'w')
        search_direction = sys.argv[4]
        main(matrix_link, words_link, search_direction, output_file)
