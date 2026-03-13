# -*- coding: utf-8 -*-
"""房价计算模块。

根据人均可支配收入计算合理的房价。
"""

import math
from typing import Union


def calc_ahp(
    monthly_disposable_income: Union[float, int],
    house_area_per_person: Union[int, float] = 35,
    house_expense_ratio: float = 0.3,
    debt_year: Union[int, float] = 30,
    debt_rate: float = 3.5/100,
    down_payment_ratio: float = 0.3,
    year_for_down_payment: Union[int, float] = None,
    house_expense_ratio_to_down_payment: float = 0.5,
    down_payment_value: Union[float, int] = None,
) -> float:
    """根据人均可支配收入计算合理的房价。

    根据人均可支配月收入、人均住房面积、住房支出占收入比、还款年限、贷款年利率等参数，
    计算合理的房价（元/平米）。

    Args:
        monthly_disposable_income: 人均月可支配收入（元）。
        house_area_per_person: 人均住房面积（平米），默认为35。
        house_expense_ratio: 住房支出占收入比例，默认为0.3。
        debt_year: 还款年限（年），默认为30。
        debt_rate: 贷款年利率，默认为3.5%。
        down_payment_ratio: 首付比例，默认为0.3。
            与year_for_down_payment和down_payment_value三选一。
        year_for_down_payment: 攒首付需要的合理年数，默认为None。
            与down_payment_ratio和down_payment_value三选一。
        house_expense_ratio_to_down_payment: 攒首付时住房支出（房租+攒房存款）占收入比，默认为0.5。
        down_payment_value: 首付金额（元），默认为None。
            与down_payment_ratio和year_for_down_payment三选一。

    Returns:
        合理的房价（元/平米）。

    Raises:
        ValueError: 当首付计算方式参数设置不正确时抛出。

    Example:
        >>> calc_ahp(10000)
        27268.773669129267
    """
    # 每月预期房贷花费额
    monthly_pay = monthly_disposable_income * house_expense_ratio

    # 现值计算
    months = math.ceil(12 * debt_year)
    pv_ratios = [(1 + debt_rate / 12) ** n for n in range(1, months + 1)]
    pv_monthly = [monthly_pay / r for r in pv_ratios]
    pv_total = sum(pv_monthly)

    # 首付计算（三种方式只能选其一）
    if any([x is not None for x in [down_payment_value, year_for_down_payment]]):
        down_payment_ratio = None
    choices = [down_payment_ratio, down_payment_value, year_for_down_payment]
    if sum([x is not None for x in choices]) != 1:
        raise ValueError("首付计算方式只能三选一：按比例、按金额、按存款年限和占收入比。")

    # 按比例
    if down_payment_ratio is not None:
        total = pv_total / (1 - down_payment_ratio)
    # 按金额
    elif down_payment_value is not None:
        total = down_payment_value + pv_total
    # 按准备首付的存款年限和期间总住房支出占收入比
    else:
        total = (
            pv_total
            + year_for_down_payment
            * 12
            * monthly_disposable_income
            * house_expense_ratio_to_down_payment
        )

    return total / house_area_per_person


if __name__ == "__main__":
    res = calc_ahp(
        monthly_disposable_income=15000,
        house_area_per_person=35,
        house_expense_ratio=0.3,
        debt_year=30,
        debt_rate=5 / 100,
        down_payment_ratio=None,
        down_payment_value=None,
        year_for_down_payment=3,
        house_expense_ratio_to_down_payment=0.5,
    )
    print(res)
    res = calc_ahp(10000)
    print(res)
