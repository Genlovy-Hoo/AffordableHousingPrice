# -*- coding: utf-8 -*-
"""合理房价计算API服务。

本文件由AI自动生成
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ahp import calc_ahp

app = FastAPI(
    title="合理房价计算API",
    description="根据人均可支配收入计算合理房价的API服务",
    version="1.0.0",
)


class AHPRequest(BaseModel):
    """房价计算请求参数模型。"""

    monthly_disposable_income: float = Field(
        ..., description="人均月可支配收入（元）", gt=0, examples=[10000]
    )
    house_area_per_person: float = Field(
        default=35, description="人均住房面积（平米）", gt=0
    )
    house_expense_ratio: float = Field(
        default=0.3, description="住房支出占收入比例", gt=0, lt=1
    )
    debt_year: float = Field(default=30, description="还款年限（年）", gt=0)
    debt_rate: float = Field(default=0.035, description="贷款年利率", ge=0, lt=1)
    down_payment_ratio: Optional[float] = Field(
        default=0.3, description="首付比例", ge=0, lt=1
    )
    down_payment_value: Optional[float] = Field(
        default=None, description="首付金额（元）", ge=0
    )
    year_for_down_payment: Optional[float] = Field(
        default=None, description="攒首付需要的合理年数", ge=0
    )
    house_expense_ratio_to_down_payment: float = Field(
        default=0.5, description="攒首付时住房支出占收入比", gt=0, le=1
    )


class AHPResponse(BaseModel):
    """房价计算响应模型。"""

    price_per_sqm: float = Field(..., description="合理房价（元/平米）")
    total_price: float = Field(..., description="房屋总价（元）")
    monthly_payment: float = Field(..., description="每月还款额（元）")
    price_to_income_ratio: float = Field(..., description="房价收入比（房价/月收入）")


@app.get("/")
async def root():
    """根路径，返回API信息。"""
    return {
        "name": "合理房价计算API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.post("/api/calc_ahp", response_model=AHPResponse)
async def calculate_ahp(request: AHPRequest):
    """计算合理房价。

    根据人均可支配收入及相关参数计算合理的房价（元/平米）。

    Args:
        request: 房价计算请求参数。

    Returns:
        包含房价、总价、月供的计算结果。

    Raises:
        HTTPException: 当参数设置不正确时抛出。
    """
    try:
        price_per_sqm, price_to_income_ratio = calc_ahp(
            monthly_disposable_income=request.monthly_disposable_income,
            house_area_per_person=request.house_area_per_person,
            house_expense_ratio=request.house_expense_ratio,
            debt_year=request.debt_year,
            debt_rate=request.debt_rate,
            down_payment_ratio=request.down_payment_ratio,
            down_payment_value=request.down_payment_value,
            year_for_down_payment=request.year_for_down_payment,
            house_expense_ratio_to_down_payment=request.house_expense_ratio_to_down_payment,
        )

        total_price = price_per_sqm * request.house_area_per_person
        monthly_payment = (
            request.monthly_disposable_income * request.house_expense_ratio
        )

        return AHPResponse(
            price_per_sqm=round(price_per_sqm, 5),
            total_price=round(total_price, 5),
            monthly_payment=round(monthly_payment, 5),
            price_to_income_ratio=round(price_to_income_ratio, 5),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
