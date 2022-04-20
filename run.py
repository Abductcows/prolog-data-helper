"""Generates the houses.pl and requests.pl from their .txt files respectively.

    .txt file format is exactly as copy pasted from the project pdf tables. Also
    generates an intermediate .csv format.

    Values for predicate names cannot be supplied as program args. Edit prolog_stuff.py
    default values instead.
"""

from files import txt_to_csv, csv_to_pl, pretty_pl_sort
from prolog_stuff import default_house_predicates, default_request_predicates


def houses_txt_to_pl(base_file_name: str):
    txt_to_csv(base_file_name, None)
    csv_to_pl(base_file_name, default_house_predicates)
    pretty_pl_sort(f'{base_file_name}.pl', default_house_predicates[0])


def requests_txt_to_pl(base_file_name: str):
    txt_to_csv(base_file_name, lambda i: i - 1)
    csv_to_pl(base_file_name, default_request_predicates)
    pretty_pl_sort(f'{base_file_name}.pl', default_request_predicates[0])


if __name__ == '__main__':
    for fun, arg in ((houses_txt_to_pl, 'res/houses'), (requests_txt_to_pl, 'res/requests')):
        try:
            fun(arg)
        except FileNotFoundError:
            pass
