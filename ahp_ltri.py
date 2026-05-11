# -*- coding: utf-8 -*-
"""
根据租金收益法计算合理的房价。
"""

from typing import Tuple, Union


def calc_ahp_ltri(
    monthly_rent: float,
    area: float,
    annual_rate: float = 0.02,
    years: Union[int, float, str] = 50,
) -> Tuple[float, str]:
    """根据租金收益法计算合理的房价。

    基于未来租金现金流的现值计算合理房价，折现率为存款年利率。
    若出租年限为无穷大，则使用永续年金极限公式。

    Args:
        monthly_rent: 月租金（元）。
        area: 房产面积（平米）。
        annual_rate: 存款年利率（小数，如0.035表示3.5%），默认为0.02。
        years: 长期出租年数（int/float）或字符串"无限"/"无穷大"表示无穷大，默认为50。

    Returns:
        元组，包含两个值：
        - 合理房价（元/平米）
        - 租售比，格式为"1:xxx"，其中xxx为总房价/月租金四舍五入取整

    Raises:
        ValueError: 当租金、面积、年利率非正数，或年数类型/值不合法时抛出。

    Example:
        >>> calc_ahp_ltri(3000, 80, 0.035, 30)
        (8351.061936170838, '1:223')
        >>> calc_ahp_ltri(3000, 80)
        (14215.819615236694, '1:379')
        >>> calc_ahp_ltri(3000, 80, years="无限")
        (22500.0, '1:600')
        >>> calc_ahp_ltri(3000, 80, years="无穷大")
        (22500.0, '1:600')
    """
    if monthly_rent <= 0:
        raise ValueError("月租金必须大于0")
    if area <= 0:
        raise ValueError("房产面积必须大于0")
    if annual_rate <= 0:
        raise ValueError("存款年利率必须大于0")

    r_monthly = annual_rate / 12

    if isinstance(years, str):
        if years in ("无限", "无穷大"):
            # 无穷大时极限值：PV = 12 * M / r_annual
            total_price = 12 * monthly_rent / annual_rate
        else:
            raise ValueError('出租年数字符串仅支持"无限"或"无穷大"')
    elif isinstance(years, (int, float)):
        if years <= 0:
            raise ValueError("出租年数必须大于0")
        # 有限年数时求和：PV = Σ M / (1 + r/12)^n, n = 1..(years*12)
        months = int(years * 12)
        discount = 1 + r_monthly
        total_price = sum(monthly_rent / (discount ** n) for n in range(1, months + 1))
    else:
        raise ValueError("出租年数必须是数值或字符串")

    price_per_sqm = total_price / area
    rent_to_price_str = f"1:{round(total_price / monthly_rent)}"

    return price_per_sqm, rent_to_price_str


if __name__ == "__main__":
    # 示例1：30年出租
    res = calc_ahp_ltri(monthly_rent=3000, area=80, annual_rate=0.035, years=30)
    print(f"房价: {res[0]:.5f} 元/平米, 总价: {res[0] * 80:.2f} 元, 租售比: {res[1]}")

    # 示例2：默认50年出租，使用默认利率2%
    res = calc_ahp_ltri(monthly_rent=3000, area=80)
    print(f"房价: {res[0]:.5f} 元/平米, 总价: {res[0] * 80:.2f} 元, 租售比: {res[1]}")

    # 示例3：无穷大出租（"无限"）
    res = calc_ahp_ltri(monthly_rent=3000, area=80, years="无限")
    print(f"房价: {res[0]:.5f} 元/平米, 总价: {res[0] * 80:.2f} 元, 租售比: {res[1]}")

    # 示例4：无穷大出租（"无穷大"）
    res = calc_ahp_ltri(monthly_rent=3000, area=80, years="无穷大")
    print(f"房价: {res[0]:.5f} 元/平米, 总价: {res[0] * 80:.2f} 元, 租售比: {res[1]}")

    # 示例5：无穷大出租（"无限"）
    res = calc_ahp_ltri(monthly_rent=4500, area=60, annual_rate=0.054, years="无限")
    print(f"房价: {res[0]:.5f} 元/平米, 总价: {res[0] * 60:.2f} 元, 租售比: {res[1]}")
