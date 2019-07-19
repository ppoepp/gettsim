from itertools import product

import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from src.analysis.tax_transfer_funcs.taxes import favorability_check
from src.analysis.tax_transfer_funcs.test_tax_transfers.auxiliary_test_tax import (
    load_input,
)
from src.analysis.tax_transfer_funcs.test_tax_transfers.auxiliary_test_tax import (
    load_output,
)


input_cols = [
    "hid",
    "tu_id",
    "pid",
    "zveranl",
    "child",
    "tax_nokfb_tu",
    "tax_kfb_tu",
    "abgst_tu",
    "kindergeld_basis",
    "kindergeld_tu_basis",
    "year",
]

years = [2010, 2012, 2016]
columns = ["incometax_tu", "kindergeld", "kindergeld_hh", "kindergeld_tu"]
to_test = list(product(years, columns))


@pytest.mark.parametrize("year, column", to_test)
def test_favorability_check(year, column):
    file_name = "test_dfs_favorability_check.xlsx"
    df = load_input(year, file_name, input_cols)
    tb = {}
    tb["zve_list"] = ["nokfb", "kfb"]
    tb["yr"] = year
    calculated = pd.Series(name=column)
    for tu_id in df["tu_id"].unique():
        calculated = calculated.append(
            favorability_check(df[df["tu_id"] == tu_id], tb)[column]
        )
    expected = load_output(year, file_name, column)
    assert_series_equal(calculated, expected)
