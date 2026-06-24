# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import control as ct

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)
font_path = r"C:/Windows/Fonts/msyh.ttc"
fm.fontManager.addfont(font_path)
cjk = fm.FontProperties(fname=font_path).get_name()
plt.rcParams["font.sans-serif"] = [cjk, "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 130
plt.rcParams["savefig.bbox"] = "tight"

def save(name):
    p = os.path.join(OUT, name); plt.savefig(p); plt.close(); print("saved", p)

# ============ 实验二 时域分析 ============
# 表2-1 a: 手动绘制 y=10*(1-exp(-2t))
t = np.arange(0, 5.0001, 0.5)
y = 10*(1-np.exp(-2*t))
plt.figure(figsize=(5.5,4))
plt.plot(t, y, 'r')
plt.axis([0,5,0,10.1]); plt.yticks(range(0,11))
plt.title("y(t) = 1 - exp(-2t)"); plt.xlabel("t"); plt.ylabel("y(t)"); plt.grid(True)
save("e2_t21_manual.png")

# 表2-1 b: step 10/(0.5s+1)
sys_b = ct.tf([10],[0.5,1])
tb, yb = ct.step_response(sys_b)
plt.figure(figsize=(5.5,4))
plt.plot(tb, yb, 'b'); plt.grid(True)
plt.title("Step Response of 10/(0.5s+1)"); plt.xlabel("Time (s)"); plt.ylabel("Amplitude")
save("e2_t21_step.png")

# 表2-1 c: comparison
s1 = ct.tf([10],[0.5,1]); s2 = ct.tf([10],[1,1])
t1,y1 = ct.step_response(s1); t2,y2 = ct.step_response(s2)
plt.figure(figsize=(5.5,4))
plt.plot(t1,y1,label='0.5s+1'); plt.plot(t2,y2,label='s+1')
plt.legend(); plt.grid(True); plt.title("Comparison")
plt.xlabel("Time (s)"); plt.ylabel("Amplitude")
save("e2_t21_compare.png")

# 表2-2 二阶系统
t22 = np.linspace(0,80,1000); wn=0.4
zetas = list(np.arange(0,0.81,0.2)) + [1,1.5,2]
plt.figure(figsize=(6,4.5)); 
for zeta in zetas:
    sys = ct.tf([wn**2],[1,2*zeta*wn,wn**2])
    to,yo = ct.step_response(sys, t22)
    plt.plot(to,yo,label=f"\u03b6 = {zeta:g}")
plt.title("二阶系统响应曲线"); plt.xlabel("时间 (s)"); plt.ylabel("响应幅值")
plt.legend(); plt.grid(True); plt.axis([0,80,0,2])
save("e2_t22_second.png")

# 表2-3 impulse 1/(s^2+0.2s+1)
sys23 = ct.tf([1],[1,0.2,1])
t3,y3 = ct.impulse_response(sys23)
plt.figure(figsize=(5.5,4))
plt.plot(t3,y3,'b'); plt.grid(True)
plt.title("Unit-impulse Response of G(s)=1/(s^2+0.2s+1)")
plt.xlabel("Time (s)"); plt.ylabel("Amplitude")
save("e2_t23_impulse.png")

print("=== Experiment 2 done ===")
