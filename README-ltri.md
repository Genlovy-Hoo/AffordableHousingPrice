<small>本文档由AI自动生成</small>

# 合理房价(Affordable Housing Price, AHP)计算器 

小程序来啦，扫码使用
![小程序码](./MiniApp.png)

# 合理房价（租金收益法）

根据租金收益法计算合理房价的 Python 模块；实现位于 `ahp_ltri.py`（LTRI：Long Term Rent Income 长期租金收益）。

## 功能介绍

本模块提供一个核心函数 `calc_ahp_ltri`，用于根据月租金、存款年利率及相关参数计算合理的房价（元/平米）及租售比。

计算逻辑基于以下因素：
- 月租金收入
- 存款年利率（作为折现率）
- 房产面积
- 长期出租年数（有限年数或无限）

## 计算原理

### 核心思想

本模块从房产作为投资品的收益回报角度出发，将未来租金现金流按存款年利率折现，反向推导合理的房价水平。

### 计算公式

#### 1. 有限出租年数

将未来每月租金折现到现在，得到房屋总价的合理现值：

$$
PV = \sum_{n=1}^{N} \frac{M}{(1 + \frac{r_{annual}}{12})^n}
$$

其中：
- $PV$：房屋合理总价（元）
- $M$：月租金（元）
- $N$：总出租月数（= 出租年数 × 12）
- $r_{annual}$：存款年利率（小数，如 0.02 表示 2%）

#### 2. 无限出租年数（极限值）

当出租年数趋于无穷大时，上述等比数列收敛为：

$$
PV_{\infty} = \frac{12M}{r_{annual}}
$$

#### 3. 计算合理房价

$$
P_{per\_sqm} = \frac{PV}{A}
$$

其中 $A$ 为房产面积（平米）。

#### 4. 计算租售比

$$
\text{租售比} = \frac{M}{PV} = \frac{1}{PV \div M}
$$

返回格式为文本 `1:xxx`，其中 `xxx` 为 $\frac{PV}{M}$ 四舍五入取整后的值。

### 计算示例

假设某房产月租金为 3000 元，存款年利率 2%，面积 80 平米，出租 50 年：

| 参数 | 值 |
|------|-----|
| 月租金 | 3,000 元 |
| 存款年利率 | 2%（0.02） |
| 房产面积 | 80 平米 |
| 出租年数 | 50 年 |

计算过程：
1. 月折现率：$0.02 \div 12 \approx 0.001667$
2. 总月数：$50 \times 12 = 600$ 个月
3. 房屋总价：约 $1,137,265.57$ 元（逐月折现求和）
4. 合理房价：$1,137,265.57 \div 80 \approx 14,215.82$ 元/平米
5. 租售比：$1:379$

若出租年数为无限：
1. 房屋总价：$12 \times 3000 \div 0.02 = 1,800,000$ 元
2. 合理房价：$1,800,000 \div 80 = 22,500$ 元/平米
3. 租售比：$1:600$

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
from ahp_ltri import calc_ahp_ltri

# 使用默认参数计算（默认50年，利率2%）
price, ratio = calc_ahp_ltri(monthly_rent=3000, area=80)
print(f"合理房价: {price:.5f} 元/平米")
print(f"租售比: {ratio}")
# 输出: 合理房价: 14215.81962 元/平米
# 输出: 租售比: 1:379
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `monthly_rent` | float | **必填** | 月租金（元） |
| `area` | float | **必填** | 房产面积（平米） |
| `annual_rate` | float | 0.02 | 存款年利率（小数，如0.02表示2%） |
| `years` | int/float/str | 50 | 长期出租年数；传入 `"无限"` 或 `"无穷大"` 按无穷大计算极限值 |

**返回值**：`(合理房价元/平米, 租售比)`，其中租售比格式为 `1:xxx` 文本。

### 示例

```python
from ahp_ltri import calc_ahp_ltri

# 示例1：30年出租，利率3.5%
price, ratio = calc_ahp_ltri(
    monthly_rent=3000,
    area=80,
    annual_rate=0.035,
    years=30,
)
# 房价: 8351.06 元/平米, 租售比: 1:223

# 示例2：默认50年，默认利率2%
price, ratio = calc_ahp_ltri(
    monthly_rent=3000,
    area=80,
)
# 房价: 14215.82 元/平米, 租售比: 1:379

# 示例3：无限年数出租
price, ratio = calc_ahp_ltri(
    monthly_rent=3000,
    area=80,
    years="无限",
)
# 房价: 22500.00 元/平米, 租售比: 1:600
```

## 许可证

MIT License
