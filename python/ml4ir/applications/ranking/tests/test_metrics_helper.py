import unittest
from unittest.mock import patch

import pandas as pd
import numpy as np
from pandas import testing as pd_testing

from ml4ir.applications.ranking.model.metrics.metrics_helper import *


class ComputeAuxMetricsTest(unittest.TestCase):
    """Test suite for ml4ir.applications.ranking.model.metrics.metrics_helper"""

    def test_compute_aux_metrics_1(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([10, 10, 10, 10, 10, 10, 10, 10, 1]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 1.,
                "test_label_failure_all": 0,
                "test_label_failure_any": 0,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 0,
                "test_label_failure_any_count": 0,
                "test_label_failure_any_fraction": 0.0}),
            check_less_precise=True)

    def test_compute_aux_metrics_2(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 10]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.30392,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 9,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 8,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_metrics_3(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([10, 10, 10, 1]),
            ranks=pd.Series(list(range(1, 5))),
            click_rank=4,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 1.,
                "test_label_failure_all": 0,
                "test_label_failure_any": 0,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 0,
                "test_label_failure_any_count": 0,
                "test_label_failure_any_fraction": 0.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_4(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 1, 1, 10]),
            ranks=pd.Series(list(range(1, 5))),
            click_rank=4,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.432,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 4,
                "test_label_failure_any_rank": 4,
                "test_label_failure_any_count": 3,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_5(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 1, 1, 5]),
            ranks=pd.Series(list(range(1, 5))),
            click_rank=4,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.475,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 4,
                "test_label_failure_any_rank": 4,
                "test_label_failure_any_count": 3,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_6(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([5, 5, 5, 10]),
            ranks=pd.Series(list(range(1, 5))),
            click_rank=4,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.47287,
                "test_label_failure_all": 1.0,
                "test_label_failure_any": 1.0,
                "test_label_failure_all_rank": 4.0,
                "test_label_failure_any_rank": 4.0,
                "test_label_failure_any_count": 3.0,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_7(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 1, 1, 1, 5, 5, 5, 5, 10]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.326,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 9,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 8,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_8(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([5, 5, 5, 5, 1, 1, 1, 1, 10]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.358,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 9,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 8,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_9(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 5, 1, 5, 1, 5, 1, 5, 10]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.33548,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 9,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 8,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_10(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([5, 1, 5, 1, 5, 1, 5, 1, 10]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.348953,
                "test_label_failure_all": 1,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 9,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 8,
                "test_label_failure_any_fraction": 1.0
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_11(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 1, 1, 1, 10, 10, 10, 10, 5]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.545,
                "test_label_failure_all": 0,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 4,
                "test_label_failure_any_fraction": 0.5
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_12(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([10, 10, 10, 10, 1, 1, 1, 1, 5]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.999,
                "test_label_failure_all": 0,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 4,
                "test_label_failure_any_fraction": 0.5
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_13(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([1, 10, 1, 10, 1, 10, 1, 10, 5]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.6776,
                "test_label_failure_all": 0,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 4,
                "test_label_failure_any_fraction": 0.5
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_14(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([10, 1, 10, 1, 10, 1, 10, 1, 5]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=9,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.8665,
                "test_label_failure_all": 0,
                "test_label_failure_any": 1,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 9,
                "test_label_failure_any_count": 4,
                "test_label_failure_any_fraction": 0.5
            }),
            check_less_precise=True)

    def test_compute_aux_label_metrics_invalid_click(self):
        computed_metrics = compute_aux_metrics(
            aux_label_values=pd.Series([10, 1, 10, 1, 10, 1, 10, 1, 5]),
            ranks=pd.Series(list(range(1, 10))),
            click_rank=15,
            aux_label="test_label")
        pd_testing.assert_series_equal(
            pd.Series(computed_metrics),
            pd.Series({
                "test_label_NDCG": 0.866541,
                "test_label_failure_all": 0,
                "test_label_failure_any": 0,
                "test_label_failure_all_rank": 0,
                "test_label_failure_any_rank": 0,
                "test_label_failure_any_count": 0,
                "test_label_failure_any_fraction": 0.
            }),
            check_less_precise=True)

    @patch("ml4ir.applications.ranking.model.metrics.metrics_helper.compute_aux_metrics")
    def test_compute_aux_metrics_on_query_group(self, mock_compute_aux_metrics):
        query_group = pd.DataFrame({
            "old_rank": [1, 2, 3, 4, 5],
            "new_rank": [3, 2, 1, 5, 4],
            "click": [0, 0, 1, 0, 0],
            "aux_label": [5, 5, 5, 2, 2]
        })
        mock_compute_aux_metrics.return_value = {}
        compute_aux_metrics_on_query_group(
            query_group=query_group,
            label_col="click",
            old_rank_col="old_rank",
            new_rank_col="new_rank",
            aux_label="aux_label")

        assert mock_compute_aux_metrics.call_count == 2 * 1

        call_args = [args[1] for args in mock_compute_aux_metrics.call_args_list]
        i = 0
        for state in ["old", "new"]:
            assert pd.Series.equals(
                call_args[i]["aux_label_values"], query_group["aux_label"])
            assert pd.Series.equals(call_args[i]["ranks"], query_group["{}_rank".format(state)])
            assert call_args[i]["click_rank"] == query_group[query_group["click"]
                                                             == 1]["{}_rank".format(state)].values[0]
            assert call_args[i]["aux_label"] == "aux_label"
            assert call_args[i]["prefix"] == "{}_".format(state)

            i += 1

    def test_compute_aux_metrics_on_query_group_invalid_click(self):
        query_group = pd.DataFrame({
            "old_rank": [1, 2, 3, 4, 5],
            "new_rank": [3, 2, 1, 5, 4],
            "click": [0, 0, 0, 0, 0],
            "aux_label": [5, 5, 5, 2, 2]
        })

        aux_metrics = compute_aux_metrics_on_query_group(
            query_group=query_group,
            label_col="click",
            old_rank_col="old_rank",
            new_rank_col="new_rank",
            aux_label="aux_label")
        ndcg_rows = aux_metrics.index.str.contains("NDCG")
        self.assertEqual((aux_metrics[ndcg_rows] > 0).sum(),
                         len(aux_metrics[ndcg_rows]),
                         "NDCG should be >0 in all cases")
        self.assertEqual(aux_metrics[~ndcg_rows].sum(),
                         0,
                         "All metrics should have default values")

    def test_compute_dcg(self):
        with self.subTest("Worst ordering of grade values"):
            self.assertTrue(np.isclose(compute_dcg([1., 2., 3.]), 6.39278, atol=3))

        with self.subTest("Best ordering of grade values"):
            self.assertTrue(np.isclose(compute_dcg([3., 2., 1.]), 9.392789, atol=3))

        with self.subTest("Equal grade values"):
            self.assertTrue(np.isclose(compute_dcg([1., 1., 1.]), 2.1309, atol=3))

        with self.subTest("Zero grade values"):
            self.assertTrue(np.isclose(compute_dcg([0., 0., 0.]), 1.065, atol=3))

    def test_compute_ndcg(self):
        with self.subTest("Worst ordering of grade values"):
            self.assertTrue(np.isclose(compute_ndcg([1., 2., 3.]), 0.6806, atol=3))

        with self.subTest("Best ordering of grade values"):
            self.assertTrue(np.isclose(compute_ndcg([3., 2., 1.]), 1., atol=3))

        with self.subTest("Equal grade values"):
            self.assertTrue(np.isclose(compute_ndcg([1., 1., 1.]), 1., atol=3))
