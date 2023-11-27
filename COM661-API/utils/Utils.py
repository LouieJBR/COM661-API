import random
import uuid

from flask import Flask, request, jsonify, make_response


def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast',
             'Lisburn', 'Ballymena', 'Derry', 'Newry',
             'Enniskillen', 'Omagh', 'Ballymena']
    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint(0, len(towns) - 1)]
        rating = random.randint(1, 5)
        business_dict[id] = {
            "name": name, "town": town,
            "rating": rating, "reviews": {}
        }
    return business_dict


def pagination():
    page_num, page_size = 1, 10

    if request.args.get('pn'):
        try:
            page_num = int(request.args.get('pn'))
            if page_num < 1:
                raise ValueError("Page number must be greater than 0.")
        except ValueError:
            return make_response(jsonify({"error": "Invalid page number."}), 400)

    if request.args.get('ps'):
        try:
            page_size = int(request.args.get('ps'))
            if page_size < 1:
                raise ValueError("Page size must be greater than 0.")
        except ValueError:
            return make_response(jsonify({"error": "Invalid page size."}), 400)

    page_start = (page_size * (page_num - 1))

    return page_num, page_size, page_start

def check_sort_params():
    order_by = request.args.get('orderBy', None)

    # Default sorting behavior (e.g., sorting by price in ascending order)
    default_sort_field = 'price'
    default_sort_order = 1

    if order_by and order_by.startswith('-'):
        # If order_by starts with '-', it means descending order
        order_by = order_by[1:]
        default_sort_order = -1

    # Define allowed fields for sorting
    allowed_sort_fields = ['price', 'name']

    # Validate order_by parameter
    if order_by not in allowed_sort_fields and order_by is not None:
        return make_response(jsonify({"error": "Invalid sort field"}), 400)

    # Use the specified order_by or default values
    sort_field = order_by if order_by in allowed_sort_fields else default_sort_field
    sort_order = default_sort_order

    return sort_field, sort_order


