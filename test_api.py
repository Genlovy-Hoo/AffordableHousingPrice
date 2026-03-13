# -*- coding: utf-8 -*-
"""API测试脚本。

本文件由AI自动生成
"""

import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture
def client():
    """创建测试客户端。"""
    return TestClient(app)


class TestRoot:
    """测试根路径。"""

    def test_root(self, client):
        """测试根路径返回正确信息。"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "合理房价计算API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"


class TestCalcAHP:
    """测试房价计算API。"""

    def test_calc_ahp_default(self, client):
        """测试使用默认参数计算房价。"""
        response = client.post(
            "/api/calc_ahp",
            json={"monthly_disposable_income": 10000},
        )
        assert response.status_code == 200
        data = response.json()
        assert "price_per_sqm" in data
        assert "total_price" in data
        assert "monthly_payment" in data
        assert abs(data["price_per_sqm"] - 27268.77) < 1
        assert data["monthly_payment"] == 3000.0

    def test_calc_ahp_custom_params(self, client):
        """测试使用自定义参数计算房价。"""
        response = client.post(
            "/api/calc_ahp",
            json={
                "monthly_disposable_income": 15000,
                "house_area_per_person": 40,
                "house_expense_ratio": 0.35,
                "debt_year": 25,
                "debt_rate": 0.04,
                "down_payment_ratio": 0.25,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["price_per_sqm"] > 0
        assert data["total_price"] > 0
        assert data["monthly_payment"] == 15000 * 0.35

    def test_calc_ahp_down_payment_value(self, client):
        """测试使用首付金额计算房价。"""
        response = client.post(
            "/api/calc_ahp",
            json={
                "monthly_disposable_income": 15000,
                "down_payment_ratio": None,
                "down_payment_value": 500000,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["price_per_sqm"] > 0

    def test_calc_ahp_year_for_down_payment(self, client):
        """测试使用存款年限计算房价。"""
        response = client.post(
            "/api/calc_ahp",
            json={
                "monthly_disposable_income": 15000,
                "down_payment_ratio": None,
                "down_payment_value": None,
                "year_for_down_payment": 3,
                "house_expense_ratio_to_down_payment": 0.5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["price_per_sqm"] > 0

    def test_calc_ahp_invalid_down_payment_options(self, client):
        """测试首付计算方式参数设置不正确时返回错误。"""
        response = client.post(
            "/api/calc_ahp",
            json={
                "monthly_disposable_income": 10000,
                "down_payment_ratio": None,
                "down_payment_value": None,
                "year_for_down_payment": None,
            },
        )
        assert response.status_code == 400
        assert "首付计算方式只能三选一" in response.json()["detail"]

    def test_calc_ahp_invalid_income(self, client):
        """测试月收入为负数时返回错误。"""
        response = client.post(
            "/api/calc_ahp",
            json={"monthly_disposable_income": -10000},
        )
        assert response.status_code == 422  # Validation error

    def test_calc_ahp_zero_income(self, client):
        """测试月收入为零时返回错误。"""
        response = client.post(
            "/api/calc_ahp",
            json={"monthly_disposable_income": 0},
        )
        assert response.status_code == 422  # Validation error

    def test_calc_ahp_missing_required_field(self, client):
        """测试缺少必填字段时返回错误。"""
        response = client.post(
            "/api/calc_ahp",
            json={},
        )
        assert response.status_code == 422  # Validation error
