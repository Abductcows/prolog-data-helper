def str_to_prolog_value(s: str):
    if s in value_map:
        return value_map[s]
    elif s.isdigit():
        return s
    else:
        return f'"{s}"'


def pl_predicate(name, *args):
    s = ', '.join(args)
    return f'{name}({s}).\n'


value_map = {
    'ναι': '1',
    'yes': '1',
    'όχι': '0',
    'οχι': '0',
    'no': '0'
}

# In same order as table in project pdf. Key is address
default_house_predicates = (
    'house',
    [
        'address',
        'bedrooms',
        'area',
        'in_city_center',
        'floor_number',
        'has_elevator',
        'allows_pets',
        'yard_area',
        'rent_amount'
    ]
)

# same as pdf. Key is name
default_request_predicates = (
    'customer',
    [
        'customer_name',
        'min_area',
        'min_bedrooms',
        'needs_pet',
        'needs_elevator_above_floor',
        'max_rent_cutoff',
        'max_rent_for_city_center',
        'max_rent_for_suburbs',
        'max_rate_per_extra_area_unit',
        'max_rate_per_yard_area_unit'
    ]
)
