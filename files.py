import os

from prolog_stuff import str_to_prolog_value, pl_predicate


def txt_to_csv(base_file_name, first_int_index_transform):
    """
    Generates a .csv file from the .txt, where each value is matched to a table column, as per the pdf
    :param base_file_name: the file name without extension
    :param first_int_index_transform: stupid hack parameter to work for both houses and requests
    """
    with open(f'{base_file_name}.txt', encoding='UTF-8') as file, \
            open(f'{base_file_name}.csv', 'w', encoding='UTF-8') as out:
        for line in file:
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

        for line in file:
            values = list(map(str_to_prolog_value, line.rstrip().split(',')))
            key = values[0]

            # base
            out.write(pl_predicate(category_name, key))

            # attributes excepting key
            for i in range(1, len(predicates)):
                out.write(pl_predicate(predicates[i], key, values[i]))

        # key category mapping to itself
        out.write(
            f'{predicates[0]}(X, Y) :- {category_name}(X), Y = X.'
        )


def sort_file_overwrite(relative_filename: str):
    """
    Sorts the file alphabetically on rows. Uses os utils if possible or defaults to in-memory sort
    :param relative_filename: the file name relative to the script file being executed
    """
    if os.name == 'posix':
        adjusted_filename = f'"./{relative_filename}"'
        delete = 'rm'
        move = 'mv'
    else:
        adjusted_filename = relative_filename.replace('/', '\\')
        adjusted_filename = f'".\\{adjusted_filename}"'
        delete = 'del'
        move = 'move'

    exit_code = os.system(f'sort {adjusted_filename} > {adjusted_filename}.temp')

    if exit_code == 0:
        os.system(f'{move} {adjusted_filename}.temp {adjusted_filename}')
        return
    else:
        os.system(f'{delete} {adjusted_filename}.temp')

    # in-memory sort
    print('Sort failed, sorting in memory')
    with open(relative_filename, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    with open(relative_filename, 'w', encoding='UTF-8') as out:
        out.writelines(sorted(lines))
