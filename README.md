<small>本文档由AI自动生成</small>

# 合理房价(Affordable Housing Price, AHP)计算器 

根据人均可支配收入计算合理房价的 Python 模块。

## 功能介绍

本模块提供一个核心函数 `calc_ahp`，用于根据人均月可支配收入及相关参数计算合理的房价（元/平米）。

计算逻辑基于以下因素：
- 每月住房支出占收入比例
- 贷款还款年限与利率
- 首付计算方式（三种可选）
- 人均住房面积

## 计算原理

### 核心思想

本模块从购房者的实际支付能力出发，基于月可支配收入、合理支出比例、贷款条件等参数，反向推导合理的房价水平。

### 计算步骤

#### 1. 计算每月可用于还贷的金额

$$
M = I \times r_{expense}
$$

其中：
- $M$：每月还款额
- $I$：人均月可支配收入
- $r_{expense}$：住房支出占收入比例（默认30%）

#### 2. 计算贷款现值

将未来所有月供折现到现在，得到贷款本金的现值：

$$
PV = \sum_{n=1}^{N} \frac{M}{(1 + \frac{r_{annual}}{12})^n}
$$

其中：
- $PV$：贷款现值（贷款本金）
- $N$：总还款月数（= 还款年限 × 12）
- $r_{annual}$：贷款年利率

#### 3. 计算房屋总价

根据首付计算方式（三选一）计算房屋总价：

**方式一：按首付比例**

$$
P_{total} = \frac{PV}{1 - r_{down}}
$$

其中 $r_{down}$ 为首付比例。

**方式二：按首付金额**

$$
P_{total} = DP + PV
$$

其中 $DP$ 为首付金额。

**方式三：按存款年限**

$$
P_{total} = PV + Y \times 12 \times I \times r_{saving}
$$

其中：
- $Y$：攒首付的年限
- $r_{saving}$：存款期间住房支出占收入比

#### 4. 计算合理房价

$$
P_{per\_sqm} = \frac{P_{total}}{A}
$$

其中 $A$ 为人均住房面积（默认35平米）。

### 计算示例

假设某人月可支配收入为 10000 元，使用默认参数：

| 参数 | 值 |
|------|-----|
| 月可支配收入 | 10,000 元 |
| 人均住房面积 | 35 平米 |
| 住房支出比例 | 30% |
| 还款年限 | 30 年 |
| 贷款年利率 | 3.5% |
| 首付比例 | 30% |

计算过程：
1. 每月还款额：$10,000 \times 0.3 = 3,000$ 元
2. 贷款现值：约 667,945 元
3. 房屋总价：$667,945 \div (1 - 0.3) \approx 954,207$ 元
4. 合理房价：$954,207 \div 35 \approx 27,268.77$ 元/平米

## 安装

本项目使用 [uv](https://docs.astral.sh/uv/) 进行 Python 环境管理。

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目
git clone <repository-url>
cd AffordableHousingPrice

# 安装依赖
uv sync
```

## 使用方法

### 方式一：Python 模块

```python
from ahp import calc_ahp

# 使用默认参数计算
price = calc_ahp(monthly_disposable_income=10000)
print(f"合理房价: {price:.2f} 元/平米")
# 输出: 合理房价: 27268.77 元/平米
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `monthly_disposable_income` | float/int | **必填** | 人均月可支配收入（元） |
| `house_area_per_person` | int/float | 35 | 人均住房面积（平米） |
| `house_expense_ratio` | float | 0.3 | 住房支出占收入比例 |
| `debt_year` | int/float | 30 | 还款年限（年） |
| `debt_rate` | float | 0.035 | 贷款年利率（默认3.5%） |
| `down_payment_ratio` | float | 0.3 | 首付比例（三选一） |
| `down_payment_value` | float/int | None | 首付金额（三选一） |
| `year_for_down_payment` | int/float | None | 攒首付需要的合理年数（三选一） |
| `house_expense_ratio_to_down_payment` | float | 0.5 | 攒首付时住房支出占收入比 |

### 首付计算方式

首付计算支持三种方式（只能三选一）：

1. **按比例**：设置 `down_payment_ratio`（如 0.3 表示 30% 首付）
2. **按金额**：设置 `down_payment_value`（如 500000 元）
3. **按存款年限**：设置 `year_for_down_payment`，根据存款年限和期间住房支出占比计算

### 示例

```python
# 示例1：按首付比例计算
price = calc_ahp(
    monthly_disposable_income=15000,
    down_payment_ratio=0.3
)

# 示例2：按首付金额计算
price = calc_ahp(
    monthly_disposable_income=15000,
    down_payment_value=500000
)

# 示例3：按存款年限计算（3年攒首付）
price = calc_ahp(
    monthly_disposable_income=15000,
    year_for_down_payment=3,
    house_expense_ratio_to_down_payment=0.5
)
```

### API 服务

```bash
# 启动服务
uv run python api.py

# 或使用 uvicorn
uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

启动后访问：
- API 文档：http://localhost:8000/docs
- 交互式文档：http://localhost:8000/redoc

#### API 调用示例

**请求**

```bash
curl -X POST "http://localhost:8000/api/calc_ahp" \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_disposable_income": 10000,
    "house_area_per_person": 35,
    "house_expense_ratio": 0.3,
    "debt_year": 30,
    "debt_rate": 0.035,
    "down_payment_ratio": 0.3
  }'
```

**响应**

```json
{
  "price_per_sqm": 27268.77,
  "total_price": 954407.0,
  "monthly_payment": 3000.0
}
```

## 许可证

MIT License
