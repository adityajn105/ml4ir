from typing import List

import numpy as np
import pandas as pd

from ml4ir.applications.ranking.model.metrics.helpers.metric_key import Metric


def compute_dcg(relevance_grades: List[float]):
    """
    Compute the discounted cumulative gains on a list of relevance grades

    Parameters
    ----------
    relevance_grades: list of float
        Relevance grades to be used to compute DCG metric
        The rank is the position in the list

    Returns
    -------
    float
        Computed DCG for the ranked list of relevance grades

    Notes
    -----
    Reference -> https://en.wikipedia.org/wiki/Discounted_cumulative_gain
    """
    return np.sum([((np.power(2, relevance_grades[i]) - 1.) / np.log2(i + 1 + 1)) for i in range(len(relevance_grades))])


def compute_ndcg(relevance_grades: List[float]):
    """
    Compute the normalized discounted cumulative gains on a list of relevance grades

    Parameters
    ----------
    relevance_grades: list of float
        Relevance grades to be used to compute NDCG metric
        The rank is the position in the list

    Returns
    -------
    float
        Computed NDCG for the ranked list of relevance grades

    Notes
    -----
    Reference -> https://en.wikipedia.org/wiki/Discounted_cumulative_gain
    """
    return compute_dcg(relevance_grades) / compute_dcg(sorted(relevance_grades, reverse=True))


def compute_aux_metrics(
        aux_label_values: pd.Series,
        ranks: pd.Series,
        click_rank: int,
        prefix: str = "",
):
    """
    Computes the secondary ranking metrics using a aux label for a single query

    Parameters
    ----------
    aux_label_values: pd.Series
        Series object containing the aux label values for a given query
    ranks: pd.Series
        Series object containing the ranks corresponding to the aux label values
    click_rank: int
        Rank of the clicked record
    prefix: str
        Prefix attached to the metric name

    Returns
    -------
    dict
        Key value pairs of the metric names and the associated computed values
        using the aux label

    Notes
    -----
    An auxiliary label is any feature/value that serves as a proxy relevance assessment that
    the user might be interested to measure on the dataset in addition to the primary click labels.
    For example, this could be used with an exact query match feature. In that case, the metric
    sheds light on scenarios where the records with an exact match are ranked lower than those without.
    This would provide the user with complimentary information (to typical click metrics such as MRR and ACR)
    about the model to help make better trade-off decisions w.r.t. best model selection.
    """
    all_failure = 0.
    # We need to have at least one relevant document.
    # If not, any ordering is considered ideal
    intrinsic_failure = 0.
    rank_match_failure = 0.

    try:
        click_aux_label_value = aux_label_values[ranks == click_rank].values[0]
        pre_click_aux_label_values = aux_label_values[ranks < click_rank]

        if pre_click_aux_label_values.size > 0:
            # Query failure only if failure on all records
            all_failure = (
                1
                if (pre_click_aux_label_values < click_aux_label_value).all()
                else 0
            )

    except IndexError:
        # Ignore queries with missing or invalid click labels
        pass

    # Compute intrinsic NDCG metric on the aux label
    # NOTE: Here we are passing the relevance grades ordered by the ranking
    if aux_label_values.sum() > 0:
        intrinsic_failure = 1. - compute_ndcg(aux_label_values.values[np.argsort(ranks.values)])

    return {
        f"{prefix}{Metric.AUX_ALL_FAILURE}": all_failure,
        f"{prefix}{Metric.AUX_INTRINSIC_FAILURE}": intrinsic_failure,
        f"{prefix}{Metric.AUX_RANK_MATCH_FAILURE}": rank_match_failure
    }


def compute_aux_metrics_on_query_group(
        query_group: pd.DataFrame,
        label_col: str,
        old_rank_col: str,
        new_rank_col: str,
        aux_label: str,
        group_keys: List[str] = []
):
    """
    Compute the old and new auxiliary ranking metrics for a given
    query on a list of aux labels

    Parameters
    ----------
    query_group : `pd.DataFrame` object
        DataFrame group object for a single query to compute auxiliary metrics on
    label_col : str
        Name of the label column in the query_group
    old_rank_col : str
        Name of the column that represents the original rank of the records
    new_rank_col : str
        Name of the column that represents the newly computed rank of the records
        after reordering based on new model scores
    aux_label : str
        Features used to compute auxiliary failure metrics
    group_keys : list, optional
        List of features used to compute groupwise metrics

    Returns
    -------
    `pd.Series` object
        Series object containing the ranking metrics
        computed using the list of aux labels
        on the old and new ranks generated by the model
    Returns
    -------
    """
    aux_metrics_dict = {
        k: v[0] for k, v in query_group[group_keys].to_dict(orient="list").items()
    }
    try:
        # Compute failure stats for before and after ranking with model
        aux_metrics_dict.update(
            compute_aux_metrics(
                aux_label_values=query_group[aux_label],
                ranks=query_group[old_rank_col],
                click_rank=query_group[query_group[label_col] == 1][old_rank_col].values[0]
                if (query_group[label_col] == 1).sum() != 0
                else float("inf"),
                prefix="old_",
            )
        )
        aux_metrics_dict.update(
            compute_aux_metrics(
                aux_label_values=query_group[aux_label],
                ranks=query_group[new_rank_col],
                click_rank=query_group[query_group[label_col] == 1][new_rank_col].values[0]
                if (query_group[label_col] == 1).sum() != 0
                else float("inf"),
                prefix="new_",
            )
        )
    except IndexError:
        # Ignore queries with no/invalid click ranks
        pass

    return pd.Series(aux_metrics_dict)
