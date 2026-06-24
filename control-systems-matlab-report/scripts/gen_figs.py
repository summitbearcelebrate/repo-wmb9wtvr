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

# Chinese font
font_path = r"C:/Windows/Fonts/msyh.ttc"
fm.fontManager.addfont(font_path)
cjk = fm.FontProperties(fname=font_path).get_name()
plt.rcParams["font.sans-serif"] = [cjk, "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 130
plt.rcParams["savefig.bbox"] = "tight"

results = {}

def conv(a, b):
    return np.convolve(a, b)

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

# ============ render a transfer function as a LaTeX image ============
def poly_to_latex(coeffs, var="s"):
    coeffs = np.atleast_1d(coeffs)
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        p = n - i
        if abs(c) < 1e-9:
            continue
        c_round = round(c, 4)
        # coefficient text
        if p == 0:
            terms.append(f"{c_round:g}")
        else:
            if abs(c_round - 1) < 1e-9:
                coef = ""
            elif abs(c_round + 1) < 1e-9:
                coef = "-"
            else:
                coef = f"{c_round:g}"
            if p == 1:
                terms.append(f"{coef}{var}")
            else:
                terms.append(f"{coef}{var}^{{{p}}}")
    if not terms:
        return "0"
    expr = terms[0]
    for t in terms[1:]:
        if t.startswith("-"):
            expr += " - " + t[1:]
        else:
            expr += " + " + t
    return expr

def render_tf(num, den, fname, title=None):
    ntex = poly_to_latex(num)
    dtex = poly_to_latex(den)
    tex = rf"$G(s)=\dfrac{{{ntex}}}{{{dtex}}}$"
    fig = plt.figure(figsize=(4.2, 1.2))
    fig.text(0.5, 0.5, tex, ha="center", va="center", fontsize=17)
    save(fname)

def render_text(lines, fname, fontsize=14):
    fig = plt.figure(figsize=(6, 0.5 + 0.4 * len(lines)))
    txt = "\n".join(lines)
    fig.text(0.05, 0.5, txt, ha="left", va="center", fontsize=fontsize, family="monospace")
    save(fname)

# ==================================================================
# 实验一  系统的数学模型
# ==================================================================
# 表1-1 A: 特征多项式与特征根
p = np.array([1.0, 3, 0, 4])
r = np.roots(p)
results["e1_roots_p"] = [fmtnum(x) for x in r]
pp = np.poly(r)
results["e1_poly_r"] = [round(v, 4) for v in pp.real]
render_text(["r =", *[f"  {fmtnum(x)}" for x in r]], "e1_t11_roots.png")
render_text(["p =", "  " + "   ".join(f"{v:.4f}" for v in pp.real)], "e1_t11_poly.png")

# 表1-1 B: 单位反馈系统
numg = [1.0]; deng = [500.0, 0, 0]
numc = [1.0, 1]; denc = [1.0, 2]
num1 = conv(numg, numc); den1 = conv(deng, denc)
render_tf(num1, den1, "e1_t11_series.png", "num1/den1 = series(numg,deng,numc,denc)")
# cloop negative unity feedback: num1/(den1+num1)
den_cl = np.array(den1, dtype=float).copy()
n1arr = np.array(num1, dtype=float)
# align lengths
L = max(len(den_cl), len(n1arr))
den_cl = np.concatenate([np.zeros(L-len(den_cl)), den_cl])
n1pad = np.concatenate([np.zeros(L-len(n1arr)), n1arr])
den_cl = den_cl + n1pad
render_tf(num1, den_cl, "e1_t11_cloop.png", "[num,den]=cloop(num1,den1)")
results["e1_t11_num1"] = list(np.array(num1).round(4))
results["e1_t11_den1"] = list(np.array(den1).round(4))
results["e1_t11_cloop_den"] = list(den_cl.round(4))

# 表1-2 零极点
num1b = [1.0, 3, 2]; den1b = [1.0, 3, 4, 12]
z = np.roots(num1b); pls = np.roots(den1b)
results["e1_t12_zeros"] = [fmtnum(x) for x in z]
results["e1_t12_poles"] = [fmtnum(x) for x in pls]
render_text(["z =", *[f"  {fmtnum(x)}" for x in z]], "e1_t12_zeros.png")
render_text(["p =", *[f"  {fmtnum(x)}" for x in pls]], "e1_t12_poles.png")
n1_=[1,1]; n2_=[1,2]; d1_=[1,2j]; d2_=[1,-2j]; d3_=[1,3]
num2 = conv(n1_, n2_)
den2 = conv(conv(d1_, d2_), d3_)
render_text(["num2 =", "  " + "   ".join(f"{v.real:.0f}" for v in np.array(num2))], "e1_t12_num2.png")
render_text(["den2 =", "  " + "   ".join(f"{v.real:.0f}" for v in np.array(den2))], "e1_t12_den2.png")
render_tf(np.real(num2), np.real(den2), "e1_t12_printsys2.png", "printsys(num2,den2)")
num = conv(num1b, np.real(den2)); den = conv(den1b, np.real(num2))
render_tf(num, den, "e1_t12_printsys.png", "printsys(num,den)")
# pzmap: zeros of num, poles of den (they coincide)
zz = np.roots(num); pz = np.roots(den)
plt.figure(figsize=(5,4))
plt.scatter(pz.real, pz.imag, marker="x", s=90, c="b", label="极点")
plt.scatter(zz.real, zz.imag, marker="o", s=70, facecolors="none", edgecolors="r", label="零点")
plt.axhline(0, color="k", lw=0.6); plt.axvline(0, color="k", lw=0.6)
plt.grid(True); plt.xlabel("Real Axis"); plt.ylabel("Imaginary Axis")
plt.title("极点一零点图"); plt.legend()
save("e1_t12_pzmap.png")

# 表1-3 反馈系统 feedback(numg,deng,numh,denh)
numh=[1.0,1]; denh=[1.0,2]
# closed = numg*denh / (deng*denh + numg*numh)
cl_num = conv(numg, denh)
cl_den_a = conv(deng, denh); cl_den_b = conv(numg, numh)
La = max(len(cl_den_a), len(cl_den_b))
A = np.concatenate([np.zeros(La-len(cl_den_a)), cl_den_a])
B = np.concatenate([np.zeros(La-len(cl_den_b)), cl_den_b])
cl_den = A + B
render_tf(cl_num, cl_den, "e1_t13_feedback.png", "[num,den]=feedback(numg,deng,numh,denh)")
results["e1_t13_num"] = list(np.array(cl_num).round(4))
results["e1_t13_den"] = list(cl_den.round(4))

print("=== Experiment 1 done ===")
for k,v in results.items():
    print(k, "=", v)
