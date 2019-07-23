import numpy as np
import pandas as pd
import pytest

from kartothek.serialization import filter_array_like


@pytest.fixture(
    params=[
        np.array(range(10)),
        np.array(range(10)).astype(float),
        pd.Series(np.array(range(10))),
        pd.Series(np.array(range(10)).astype(float)),
        pd.Series(np.array([str(x) for x in range(10)])),
        pd.Series(np.array([str(x) for x in range(10)])).astype("category"),
    ]
)
def array_like(request):
    return request.param


def test_filter_array_like_eq(array_like):
    ix = 3
    value = array_like[ix]
    res = filter_array_like(array_like, "==", value)

    assert all(array_like[res] == array_like[ix])


def test_filter_array_like_larger_eq(array_like):
    ix = 3
    value = array_like[ix]
    res = filter_array_like(array_like, ">=", value)

    assert all(array_like[res] == array_like[ix:])


def test_filter_array_like_lower_eq(array_like):
    ix = 3
    value = array_like[ix]
    res = filter_array_like(array_like, "<=", value)

    assert all(array_like[res] == array_like[: ix + 1])


@pytest.mark.parametrize(
    "op, expected",
    [
        (">", [False, True, False]),
        (">=", [True, True, False]),
        ("<=", [True, False, True]),
        ("<", [False, False, True]),
    ],
)
@pytest.mark.parametrize(
    "cat_type",
    [
        "category",
        pd.CategoricalDtype(["A", "B", "C"]),
        pd.CategoricalDtype(["B", "C", "A"]),
        pd.CategoricalDtype(["A", "B", "C"], ordered=True),
    ],
)
def test_filter_array_like_categoricals(op, expected, cat_type):
    ser = pd.Series(["B", "C", "A"]).astype(cat_type)
    res = filter_array_like(ser, op, "B")

    assert all(res == expected)