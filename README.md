<small>本文档由AI自动生成</small>

# 合理房价 (Affordable Housing Price, AHP) 计算器

小程序来啦，扫码使用
![小程序码](./MiniApp.png)

本项目提供两种计算合理房价的方法，点击以下链接查看对应计算方法的详细说明：

## 计算方法

- [**住房支出 / 可支配收入法**](README-pcdi.md) — 基于人均月可支配收入、住房支出比例、贷款条件等参数，计算合理房价（元/平米）及房价收入比。
- [**租金收益法**](README-ltri.md) — 基于月租金、存款年利率等参数，将未来租金现金流折现，计算合理房价（元/平米）及租售比。

## 快速开始

```bash
# 克隆项目
git clone <repository-url>
cd AffordableHousingPrice

# 安装依赖（使用 uv）
uv sync

# 运行示例
python ahp_pcdi.py
python ahp_ltri.py
```

## 许可证

MIT License
