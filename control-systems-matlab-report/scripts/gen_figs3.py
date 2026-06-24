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

def render_text(lines, fname, fontsize=13):
    fig = plt.figure(figsize=(6, 0.5 + 0.36 * len(lines)))
    fig.text(0.05, 0.5, "\n".join(lines), ha="left", va="center",
             fontsize=fontsize, fontproperties=fm.FontProperties(fname=font_path))
    save(fname)

res = {}

# ============ 实验三 ============
# 表3-1 稳定性: roots([1,3,2,5,1])
den = [1.0,3,2,5,1]
r = np.roots(den)
res["e3_roots"] = [complex(round(x.real,4), round(x.imag,4)) for x in r]
lines = ["ans ="]
for x in r:
    if abs(x.imag) < 1e-9:
        lines.append(f"  {x.real:.4f}")
    else:
        sgn = "+" if x.imag>=0 else "-"
        lines.append(f"  {x.real:.4f} {sgn} {abs(x.imag):.4f}i")
render_text(lines, "e3_t31_roots.png")

# Routh table
def routh(den):
    den = [float(x) for x in den]
    n = len(den)
    cols = (n+1)//2
    R = np.zeros((n, cols))
    R[0,:len(den[0::2])] = den[0::2]
    R[1,:len(den[1::2])] = den[1::2]
    for i in range(2,n):
        for j in range(cols-1):
            a = R[i-1,0]
            if abs(a) < 1e-12:
                a = 1e-10
            R[i,j] = (R[i-1,0]*R[i-2,j+1]-R[i-2,0]*R[i-1,j+1])/a
    return R
R = routh(den)
res["routh"] = R.round(4).tolist()
rl = ["完整的劳斯表为："]
for row in R:
    rl.append("  " + "   ".join(f"{v:8.4f}" for v in row))
rl.append("")
rl.append("劳斯表第一列为： " + ", ".join(f"{v:.4f}" for v in R[:,0]))
sign_changes = int(np.sum(np.diff(np.sign(R[:,0]))!=0))
rl.append(f"系统不稳定，第一列发生了 {sign_changes} 次符号变化，存在正实部根。")
render_text(rl, "e3_t31_routh.png", fontsize=12)
res["sign_changes"] = sign_changes

# 表3-2 Bode
sysa = ct.tf([25],[1,4,25])
plt.figure(figsize=(6,4.5))
ct.bode_plot(sysa, dB=True, Hz=False, deg=True)
plt.suptitle("Bode Diagram of G(s)=25/(s^2+4s+25)")
save("e3_t32_bode_a.png")

numb = 9*np.array([1,0.2,1]); denb = np.convolve([1,0],[1,1.2,9])
sysb = ct.tf(numb, denb)
plt.figure(figsize=(6,4.5))
ct.bode_plot(sysb, dB=True, Hz=False, deg=True)
plt.suptitle("Bode Diagram of G(s)=9(s^2+0.2s+1)/s(s^2+1.2s+9)")
save("e3_t32_bode_b.png")

# 表3-3 Nyquist
sysc = ct.tf([1],[1,0.8,1])
plt.figure(figsize=(5.5,4.5))
ct.nyquist_plot(sysc)
plt.gcf().suptitle("")
plt.grid(True); plt.gca().set_title("Nyquist Plot of G(s)=1/(s^2+0.8s+1)")
save("e3_t33_nyq_a.png")

plt.figure(figsize=(5.5,4.5))
ct.nyquist_plot(sysb)
plt.gcf().suptitle("")
plt.grid(True); plt.gca().set_title("Nyquist Plot of G(s)=9(s^2+0.2s+1)/s(s^2+1.2s+9)")
save("e3_t33_nyq_b.png")

# 表3-4 Root locus (manual, clean axes)
num_rl=np.array([1.0,1]); den_rl=np.array([1.0,4,2,9])
op = np.roots(den_rl)   # open-loop poles
oz = np.roots(num_rl)   # open-loop zeros

def plot_rlocus(Ks, fname, title):
    plt.figure(figsize=(5.5,4.5))
    for K in Ks:
        # closed-loop char eq: den + K*num = 0 (align lengths)
        L = max(len(den_rl), len(num_rl))
        d = np.concatenate([np.zeros(L-len(den_rl)), den_rl])
        n = np.concatenate([np.zeros(L-len(num_rl)), num_rl])
        r = np.roots(d + K*n)
        plt.plot(r.real, r.imag, '.', color='C0', markersize=2)
    plt.plot(op.real, op.imag, 'x', color='b', markersize=10, label='开环极点')
    plt.plot(oz.real, oz.imag, 'o', mfc='none', mec='r', markersize=9, label='开环零点')
    plt.axhline(0, color='k', lw=0.5); plt.axvline(0, color='k', lw=0.5)
    plt.grid(True); plt.xlabel("Real Axis"); plt.ylabel("Imaginary Axis")
    plt.title(title); plt.legend(loc='upper left')
    save(fname)

plot_rlocus(np.linspace(0,200,4000), "e3_t34_rlocus.png", "Root Locus")
plot_rlocus(np.arange(1,10.01,0.5), "e3_t34_rlocus_k.png", "Root Locus with K from 1 to 10")

print("=== Experiment 3 done ===")
for k,v in res.items():
    print(k,"=",v)
