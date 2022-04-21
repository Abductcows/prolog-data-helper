import argparse
from dataclasses import dataclass, field
from enum import Enum


class GenMode(Enum):
    NONE = 0
    RECORDS = 1
    RULES = 2
    BOTH = 3

    def __or__(self, obj):
        return GenMode(self.value | obj.value)

    def __and__(self, obj) -> bool:
        return self.value & obj.value > 0


@dataclass
class Config:
    house_files: list[str] = field(default_factory=list)
    request_files: list[str] = field(default_factory=list)
    generation_mode: GenMode = GenMode.BOTH


config = Config()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generates the houses.pl and requests.pl from their .txt files provided'
    )
    parser.add_argument(
        '--records', help='instruct the parser to output only records',
        action='store_true'
    )
    parser.add_argument(
        '--rules', help='instruct the parser to produce only rules',
        action='store_true'
    )
    parser.add_argument(
        '--house-files', help='use these files for houses',
        nargs='*', default=['res/houses']
    )
    parser.add_argument(
        '--request-files', help='use these files for requests',
        nargs='*', default=['res/requests']
    )
    args = vars(parser.parse_args())

    # gen mode

    if args['rules'] or args['records']:
        config.generation_mode = GenMode.NONE
    if args['rules']:
        config.generation_mode = config.generation_mode | GenMode.RULES
    if args['records']:
        config.generation_mode = config.generation_mode | GenMode.RECORDS

    # house files
    config.house_files = args['house_files']

    # request files
    config.request_files = args['request_files']
