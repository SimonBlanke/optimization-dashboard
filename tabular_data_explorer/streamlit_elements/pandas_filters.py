# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np
import numbers


def _get_numeric_data_types(search_data):
    para_names = search_data.columns

    numeric_data_types = []
    for para_name in para_names:
        value0 = search_data[para_name][0]

        if isinstance(value0, numbers.Number):
            numeric_data_types.append(para_name)

    return numeric_data_types


def add_parameters(search_data, col1, key):
    para_names = list(search_data.columns)
    para_names_f = col1.multiselect(
        label="Parameters:",
        options=para_names,
        key=key + "_remove",
        default=para_names,
    )
    return search_data[para_names_f]


def filter_parameter(search_data, col1, key):
    para_names = search_data.columns
    numeric_data_types = _get_numeric_data_types(search_data)

    para_names_rem = col1.multiselect(
        label="Remove Parameters:",
        options=para_names,
        key=key + "_remove",
    )

    search_data = search_data.drop(para_names_rem, axis=1)
    para_names_ = search_data.columns
    para_names = list(set(numeric_data_types).intersection(para_names_))

    para_names_fil = col1.multiselect(
        label="Filter Parameters:",
        options=para_names,
        key=key + "_filter",
    )

    for para_name in para_names_fil:
        para_data = search_data[para_name].values
        min_ = float(np.min(para_data))
        max_ = float(np.max(para_data))
        step = (max_ - min_) / 100

        (lower, upper) = col1.slider(
            "Filter: " + str(para_name),
            min_value=min_,
            max_value=max_,
            value=(min_, max_),
            step=step,
        )
        col1.text("")

        search_data = search_data[
            (search_data[para_name] >= lower) & (search_data[para_name] <= upper)
        ]

    return search_data
