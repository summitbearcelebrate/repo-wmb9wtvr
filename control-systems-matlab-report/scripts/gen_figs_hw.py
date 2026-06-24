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
fp = fm.FontProperties(fname=font_path)
plt.rcParams["font.sans-serif"] = [cjk, "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 130
plt.rcParams["savefig.bbox"] = "tight"


def save(name):
    p = os.path.join(OUT, name)
    plt.savefig(p)
    plt.close()
    print("saved", p)


def fmtnum(x):
    if abs(x.imag) < 1e-9:
        return f"{x.real:.4f}"
    sign = "+" if x.imag >= 0 else "-"
    return f"{x.real:.4f} {sign} {abs(x.imag):.4f}i"


def poly_to_latex(coeffs, var="s"):
    coeffs = np.atleast_1d(coeffs)
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        p = n - i
        if abs(c) < 1e-9:
            continue
        c_round = round(float(c), 4)
        if p == 0:
            terms.append(f"{c_round:g}")
        else:
            if abs(c_round - 1) < 1e-9:
                coef = ""
            elif abs(c_round + 1) < 1e-9:
                coef = "-"
            else:
                coef = f"{c_round:g}"
            terms.append(f"{coef}{var}^{{{p}}}" if p > 1 else f"{coef}{var}")
    if not terms:
        return "0"
    expr = terms[0]
    for t in terms[1:]:
        expr += (" - " + t[1:]) if t.startswith("-") else (" + " + t)
    return expr


def render_tf(num, den, fname):
    tex = rf"$G(s)=\dfrac{{{poly_to_latex(num)}}}{{{poly_to_latex(den)}}}$"
    fig = plt.figure(figsize=(4.6, 1.3))
    fig.text(0.5, 0.5, tex, ha="center", va="center", fontsize=15)
    save(fname)


def render_text(lines, fname, fontsize=14):
    fig = plt.figure(figsize=(5.2, 0.5 + 0.38 * len(lines)))
    fig.text(0.06, 0.95, "\n".join(lines), ha="left", va="top",
             fontsize=fontsize, fontproperties=fp)
    plt.axis("off")
    save(fname)


# ===== 实验一 报告 Q2: roots 3,5,2 -> characteristic polynomial =====
p = np.poly([3, 5, 2])
render_text(["p = poly([3 5 2])", "p =",
             "   " + "   ".join(f"{v:g}" for v in p),
             "即特征方程为：s^3 - 10s^2 + 31s - 30 = 0"], "e1_hw2.png")

# ===== 实验一 报告 Q3: nested feedback block diagram =====
s = ct.tf('s')
G1 = 10 / (s + 1)
G2 = 2 / (s * (s + 1))
H1 = (s + 2) / (s + 3)          # inner positive feedback
H2 = 5 * s / (s**2 + 6 * s + 8)  # outer negative feedback
M = ct.feedback(G2, H1, sign=+1)
T = ct.minreal(G1 * M, verbose=False)
T = ct.minreal(ct.feedback(T, H2, sign=-1), verbose=False)
num = np.asarray(T.num[0][0], dtype=float)
den = np.asarray(T.den[0][0], dtype=float)
render_tf(num, den, "e1_hw3_tf.png")

z = ct.zeros(T)
p_ = ct.poles(T)
zlines = ["zeros (零点):"] + ["  " + fmtnum(complex(v)) for v in z]
plines = ["poles (极点):"] + ["  " + fmtnum(complex(v)) for v in p_]
render_text(zlines + [""] + plines, "e1_hw3_zp.png", fontsize=13)

plt.figure(figsize=(4.2, 3.4))
plt.scatter(np.real(p_), np.imag(p_), marker='x', s=80, color='b', label='极点')
plt.scatter(np.real(z), np.imag(z), marker='o', s=70, facecolors='none',
            edgecolors='r', label='零点')
plt.axhline(0, color='k', lw=0.5)
plt.axvline(0, color='k', lw=0.5)
plt.grid(True)
plt.xlabel('Real Axis')
plt.ylabel('Imaginary Axis')
plt.title('极点—零点图')
plt.legend()
save("e1_hw3_pzmap.png")

# ===== 实验二 报告 Q3: typical 2nd order system =====
def step2(wn, zeta, t):
    sys = ct.tf([wn**2], [1, 2 * zeta * wn, wn**2])
    tt, yy = ct.step_response(sys, t)
    return tt, yy

# Q3(1) wn fixed = 1, zeta = 0,0.25,0.5,1.0,2.0
t = np.linspace(0, 20, 1500)
plt.figure(figsize=(5.2, 3.4))
for zeta in [0, 0.25, 0.5, 1.0, 2.0]:
    tt, yy = step2(1.0, zeta, t)
    plt.plot(tt, yy, label=fr"$\zeta$={zeta}")
plt.grid(True)
plt.xlabel('时间 t (s)')
plt.ylabel('y(t)')
plt.title(r'$\omega_n=1$ 时不同 $\zeta$ 的单位阶跃响应')
plt.legend()
save("e2_hw3_zeta.png")

# Q3(2) zeta = 0.25, wn = 1,2,4,6
t2 = np.linspace(0, 20, 1500)
plt.figure(figsize=(5.2, 3.4))
for wn in [1, 2, 4, 6]:
    tt, yy = step2(wn, 0.25, t2)
    plt.plot(tt, yy, label=fr"$\omega_n$={wn}")
plt.grid(True)
plt.xlabel('时间 t (s)')
plt.ylabel('y(t)')
plt.title(r'$\zeta=0.25$ 时不同 $\omega_n$ 的单位阶跃响应')
plt.legend()
save("e2_hw3_wn.png")

# ===== 实验二 报告 Q2: G(s)=(s^2+3s+7)/(s^4+4s^3+6s^2+4s+1) step response =====
num_e2q2 = [1, 3, 7]
den_e2q2 = [1, 4, 6, 4, 1]
sys_e2q2 = ct.tf(num_e2q2, den_e2q2)
tt, yy = ct.step_response(sys_e2q2, np.linspace(0, 30, 2000))
plt.figure(figsize=(5.2, 3.3))
plt.plot(tt, yy, 'b')
plt.grid(True)
plt.xlabel('时间 t (s)')
plt.ylabel('y(t)')
plt.title(r'Step Response of $G(s)=\dfrac{s^2+3s+7}{s^4+4s^3+6s^2+4s+1}$')
save("e2_hw2_step.png")

# ===== 实验三 报告 Q2(a): Bode + margin =====
# G(s)=500(0.0167s+1)/[s(0.05s+1)(0.0025s+1)(0.001s+1)]
num_e3q2 = 500 * np.array([0.0167, 1.0])
den_e3q2 = np.convolve(np.convolve([0.05, 1], [0.0025, 1]),
                       np.convolve([0.001, 1], [1, 0]))
sys_e3q2 = ct.tf(num_e3q2, den_e3q2)
plt.figure(figsize=(5.4, 4.0))
ct.bode_plot(sys_e3q2, dB=True, Hz=False, deg=True)
plt.gcf().suptitle('Bode Diagram (实验三报告 2a)')
save("e3_hw2_bode.png")

gm, pm, wcg, wcp = ct.margin(sys_e3q2)
gm_db = 20 * np.log10(gm) if np.isfinite(gm) else np.inf
render_text([
    "[Gm,Pm,Wcg,Wcp] = margin(sys)",
    "",
    f"幅值裕度 Gm = {gm:.4g}  ({gm_db:.4g} dB)" if np.isfinite(gm) else "幅值裕度 Gm = Inf",
    f"相角裕度 Pm = {pm:.4g}  度",
    f"Wcg (相位穿越频率) = {wcg:.4g} rad/s" if np.isfinite(wcg) else "Wcg = Inf",
    f"Wcp (增益穿越频率) = {wcp:.4g} rad/s",
    "",
    "结论：Pm>0 且 Gm>0(dB)，系统稳定。" if (pm > 0 and (not np.isfinite(gm) or gm_db > 0))
    else "结论：据 Gm/Pm 符号判断系统稳定裕度。",
], "e3_hw2_margin.png", fontsize=12)

# ===== 实验三 报告 Q3: rlocus + K=1 closed-loop step =====
# open-loop G(s)=K(s^2+5s+6)/(s^2+8s+32)
num_e3q3 = [1, 5, 6]
den_e3q3 = [1, 8, 32]
# root locus (manual sweep)
Ks = np.concatenate([np.linspace(0, 5, 400), np.linspace(5, 200, 600)])
plt.figure(figsize=(5.0, 3.8))
roots_all = []
for K in Ks:
    ch = np.array(den_e3q3, float) + K * np.array(num_e3q3, float)
    roots_all.append(np.roots(ch))
roots_all = np.array(roots_all)
for col in range(roots_all.shape[1]):
    plt.plot(np.real(roots_all[:, col]), np.imag(roots_all[:, col]), 'b.', ms=1.5)
op = np.roots(den_e3q3)
oz = np.roots(num_e3q3)
plt.scatter(np.real(op), np.imag(op), marker='x', s=80, color='b', label='开环极点')
plt.scatter(np.real(oz), np.imag(oz), marker='o', s=70, facecolors='none',
            edgecolors='r', label='开环零点')
plt.axhline(0, color='k', lw=0.5); plt.axvline(0, color='k', lw=0.5)
plt.grid(True); plt.xlabel('Real Axis'); plt.ylabel('Imaginary Axis')
plt.title('Root Locus'); plt.legend()
save("e3_hw3_rlocus.png")

# K=1 closed-loop step
G = ct.tf(num_e3q3, den_e3q3)
T1 = ct.feedback(1 * G, 1)
T1 = ct.minreal(T1, verbose=False)
tt, yy = ct.step_response(T1, np.linspace(0, 6, 1500))
plt.figure(figsize=(5.2, 3.3))
plt.plot(tt, yy, 'b')
plt.grid(True); plt.xlabel('时间 t (s)'); plt.ylabel('y(t)')
plt.title('K=1 闭环系统单位阶跃响应')
save("e3_hw3_step_k1.png")
nT = np.asarray(T1.num[0][0], float); dT = np.asarray(T1.den[0][0], float)
print("K=1 closed-loop num", np.round(nT, 4), "den", np.round(dT, 4))
print("margin: Gm", gm, "Pm", pm, "Wcg", wcg, "Wcp", wcp)

print("HW figures done")
