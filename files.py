from prolog_stuff import str_to_prolog_value, pl_predicate
from collections import defaultdict


def txt_to_csv(base_file_name, first_int_index_transform):
    """
    Generates a .csv file from the .txt, where each value is matched to a table column, as per the pdf
    :param base_file_name: the file name without extension
    :param first_int_index_transform: stupid hack parameter to work for both houses and requests
    """
    with open(f'{base_file_name}.txt', encoding='UTF-8') as file, \
            open(f'{base_file_name}.csv', 'w', encoding='UTF-8') as out:
        for line in file:
            if line.isspace():
                continue
            words = line.rstrip().split(' ')
            first_number_index = next((i for i, word in enumerate(words) if word.isdigit()))
            if first_int_index_transform is not None:
                first_number_index = first_int_index_transform(first_number_index)
            columns = [' '.join(words[:first_number_index + 1])]
            columns.extend(words[first_number_index + 1:])
            csvs = ','.join(columns)
            out.write(f'{csvs}\n')


def csv_to_pl(base_file_name, predicates_used):
    """
    Generates the .pl file from the csv, using the predicate labels given
    :param base_file_name: the file name without extension
    :param predicates_used: the predicate names for the .pl generation
    """
    with open(f'{base_file_name}.csv', encoding='UTF-8') as file, \
            open(f'{base_file_name}.pl', 'w', encoding='UTF-8') as out:
        category_name, predicates = predicates_used

        # records
        for line in file:
            if line.isspace():
                continue
            values = list(map(str_to_prolog_value, line.rstrip().split(',')))
            out.write(pl_predicate(category_name, *values))

        max_pred_length = max(map(len, predicates))

        # "getters" for non-key fields
        for i in range(1, len(predicates)):
            padding = ''.rjust(max_pred_length - len(predicates[i]))
            next_list = select_attribute_i_list(len(predicates), i - 1)
            out.write(
                f'{predicates[i]}(X, Value) :- {padding} {pl_predicate(category_name, *next_list)}'
            )
        just_key = pl_predicate(category_name, *select_attribute_i_list(len(predicates))).rstrip('.\n')

        # getter for key
        padding = ''.rjust(max_pred_length - len(predicates[0]))
        out.write(f'{predicates[0]}(X, Value) :- {padding} {just_key}, Value = X.\n')

        # key based only category name predicate (to identify a house or request)
        padding = ''.rjust(max_pred_length - len(category_name) + len(', Value'))
        out.write(f'{category_name}(X) :- {padding} {just_key}.\n')


def select_attribute_i_list(n, index=None):
    """
    Generates the list ['X', _, _, _, ..., (i-th element) 'Value', _, ..] of total length n.

    If index is not supplied, then all elements after the first are '_'
    """
    start = ['X']
    if index is not None:
        rest = ['_'] * (n - 2)
        rest.insert(index, 'Value')
    else:
        rest = ['_'] * (n - 1)

    return start + rest


def sort_file_overwrite(relative_filename: str):
    """
    Sorts the file alphabetically on rows. Uses os utils if possible or defaults to in-memory sort
    :param relative_filename: the file name relative to the script file being executed
    """
    # if os.name == 'posix':
    #     adjusted_filename = f'"./{relative_filename}"'
    #     delete = 'rm'
    #     move = 'mv'
    # else:
    #     adjusted_filename = relative_filename.replace('/', '\\')
    #     adjusted_filename = f'".\\{adjusted_filename}"'
    #     delete = 'del'
    #     move = 'move'
    #
    # exit_code = os.system(f'sort {adjusted_filename} > {adjusted_filename}.temp')
    #
    # if exit_code == 0:
    #     os.system(f'{move} {adjusted_filename}.temp {adjusted_filename}')
    #     return
    # else:
    #     os.system(f'{delete} {adjusted_filename}.temp')
    #
    # # in-memory sort
    # print('Sort failed, sorting in memory')
    with open(relative_filename, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    with open(relative_filename, 'w', encoding='UTF-8') as out:
        out.writelines(sorted(lines))


def pretty_pl_sort(relative_filename: str, category_name: str):
    with open(relative_filename, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    key_indexed_lines = defaultdict(list)

    for line in lines:
        key_indexed_lines[choose_key(line, category_name)].append(line)

    with open(relative_filename, 'w', encoding='UTF-8') as out:
        for key in sorted(key_indexed_lines):
            out.writelines(key_indexed_lines[key])


def choose_key(s: str, category_name):
    if s.startswith(f'{category_name}('):
        return 0

    body = s[s.find(':-') + 2:]
    rparen = body.find(')')
    val = body.find('Value')
    if val < rparen:
        return 1
    return 2
