# 自动控制原理 MATLAB 实验报告

作者：薄天乐（学号 202308630603，电信6班）

完整实验报告（含全部结果图）：

- `自动控制原理实验报告_薄天乐.docx` — Word 文档
- `自动控制原理实验报告_薄天乐.pdf` — PDF 预览

## 内容

- 实验一　系统的数学模型（传递函数串/并联、反馈、零极点、pzmap）
- 实验二　控制系统的时域分析（一阶/二阶阶跃响应、脉冲响应）
- 实验三　系统稳定性判断、频域分析及根轨迹（roots/劳斯判据、Bode、Nyquist、根轨迹）

## 复现

本机无 MATLAB，使用 Python 的 `control` + `matplotlib` 等价复现了全部 MATLAB 命令的数值结果与曲线。

```bash
pip install matplotlib scipy control python-docx
python scripts/gen_figs.py
python scripts/gen_figs2.py
python scripts/gen_figs3.py
python scripts/build_docx.py
```

- `scripts/` — 生成图表与文档的脚本
- `figs/` — 生成的结果图（PNG）
