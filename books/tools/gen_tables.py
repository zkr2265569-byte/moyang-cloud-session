# 生成附录 A：统计分布临界值表（scipy 精确计算）。输出 common/critvals.tex
from scipy import stats
import math
out = []
w = out.append
w(r'\section{查表总指南}')
w(r'\subsection{检验统计量、原假设下的分布与对应的表}')
w(r'''\begin{center}\small
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{4.2cm}>{\raggedright\arraybackslash}p{3.6cm}L}
\toprule
检验统计量 & 原假设下的（渐近）分布 & 查哪张表、注意什么\\
\midrule
$t$ 统计量（正态误差、同方差、小样本） & $t_{n-K}$ & 表 \ref{tab:t}；$K$ 含截距\\
$t$ 统计量（大样本 / 稳健标准误） & $N(0,1)$ & 表 \ref{tab:phi}、表 \ref{tab:zcrit}\\
$t$ 统计量（聚类稳健，$G$ 个类） & 近似 $t_{G-1}$ & 表 \ref{tab:t}，自由度用 $G-1$\\
$F$ 统计量（$q$ 个线性约束） & $F_{q,\,n-K}$ & 表 \ref{tab:f05}、表 \ref{tab:f01}\\
Wald、LR、LM 统计量 & $\chi^2_q$ & 表 \ref{tab:chi}；$q$=约束个数\\
Hausman 检验 & $\chi^2_{q}$ & $q$=被比较系数的个数（时变回归元个数）\\
Sargan / Hansen $J$ 检验 & $\chi^2_{L-K}$ & $L-K$=过度识别约束个数\\
Arellano--Bond $AR(1)$/$AR(2)$ & $N(0,1)$ & 应拒绝 AR(1)、不拒绝 AR(2)\\
第一阶段 $F$（弱工具） & 非标准 & 表 \ref{tab:sy}（Stock--Yogo），经验法则 $F>10$\\
Pesaran CD 检验 & $N(0,1)$ & 双侧，$|CD|>1.96$ 即在 5\% 水平拒绝“无截面相关”\\
\bottomrule
\end{tabularx}\end{center}''')
w(r'\subsection{三种等价的决策方式}')
w(r'''\begin{itemize}
\item \key{拒绝域}：统计量落在临界值之外即拒绝。双侧 $t$：$|t|>c_{1-\alpha/2}$；$\chi^2$、$F$ 检验都是右侧检验：统计量 $>c_{1-\alpha}$。
\item \key{$p$ 值}：$p<\alpha$ 即拒绝。双侧正态 $p=2[1-\Phi(|z|)]$。
\item \key{置信区间}：$\hat\theta\pm c\cdot se(\hat\theta)$ 不含 $\theta_0$ 即在水平 $\alpha$ 下拒绝 $H_0:\theta=\theta_0$。
\end{itemize}''')
w(r'\subsection{自由度不在表中时}')
w(r'取较小的相邻自由度（临界值更大，结论更保守）；或按 $1/\mathrm{df}$ 线性插值。自由度很大时：$t_{\mathrm{df}}\approx N(0,1)$，$qF_{q,m}\approx\chi^2_q$，$\chi^2_{\mathrm{df}}$ 的上 $\alpha$ 分位数 $\approx \mathrm{df}+z_{1-\alpha}\sqrt{2\,\mathrm{df}}$（Wilson--Hilferty 更准：$\mathrm{df}\,[1-\tfrac{2}{9\mathrm{df}}+z_{1-\alpha}\sqrt{\tfrac{2}{9\mathrm{df}}}]^3$）。')
w(r'\subsection{查表例题}')
w(r'''\begin{itemize}
\item $n=45,K=5$，$t=2.10$，双侧 5\%：df$=40$，$c=2.021$，$|t|>c$，拒绝。
\item Wald 检验 3 个约束，$W=8.2$：$\chi^2_{3,0.95}=7.815<8.2$，5\% 水平拒绝；$\chi^2_{3,0.99}=11.345>8.2$，1\% 水平不拒绝。
\item $J$ 检验 $L=5$ 个工具、$K=3$ 个参数，$J=4.1$：df$=2$，$\chi^2_{2,0.95}=5.991>4.1$，不拒绝“工具全部外生”。
\item $F$ 检验 $q=3$，$n-K=40$：$F_{3,40;0.95}=2.84$。$F=3.1>2.84$，拒绝。
\end{itemize}''')

# A.2 normal
w(r'\section{标准正态分布}')
w(r'\subsection{标准正态分布函数表 \texorpdfstring{$\Phi(z)=P(Z\le z)$}{Phi(z)}}')
w(r'查法：$z$ 的整数位与第一位小数看行，第二位小数看列。例：$\Phi(1.96)$ 在“1.9”行、“0.06”列，为 0.9750。负值用对称性 $\Phi(-z)=1-\Phi(z)$；右尾概率 $P(Z>z)=1-\Phi(z)$；双侧 $p$ 值 $=2[1-\Phi(|z|)]$。')
w(r'\begin{center}\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.02}')
w(r'\captionof{table}{标准正态分布函数 $\Phi(z)$}\label{tab:phi}')
w(r'\begin{tabular}{c|cccccccccc}\toprule')
w(r'$z$ & ' + ' & '.join(f'{j/100:.2f}' for j in range(10)) + r'\\\midrule')
for i in range(35):
    z0 = i / 10
    w(f'{z0:.1f} & ' + ' & '.join(f'{stats.norm.cdf(z0 + j/100):.4f}' for j in range(10)) + r'\\')
w(r'\bottomrule\end{tabular}\end{center}')
w(r'\subsection{常用正态临界值}')
w(r'\begin{center}\small\captionof{table}{标准正态临界值 $z_{1-\alpha}$}\label{tab:zcrit}')
w(r'\begin{tabular}{lcccccc}\toprule')
alphas = [0.10, 0.05, 0.025, 0.01, 0.005, 0.001]
w(r'单侧水平 $\alpha$ & ' + ' & '.join(f'{a:g}' for a in alphas) + r'\\')
w(r'双侧水平 & ' + ' & '.join(f'{2*a:g}' for a in alphas) + r'\\\midrule')
w(r'临界值 $z_{1-\alpha}$ & ' + ' & '.join(f'{stats.norm.ppf(1-a):.3f}' for a in alphas) + r'\\\bottomrule')
w(r'\end{tabular}\end{center}')
w(r'记忆：90\%、95\%、99\% 双侧置信区间分别用 1.645、1.960、2.576。')

# A.3 t
w(r'\section{\texorpdfstring{$t$}{t} 分布临界值}')
w(r'查法：表中数 $c$ 满足 $P(t_{\mathrm{df}}>c)=\alpha$（单侧）。双侧水平 $\alpha$ 看“单侧 $\alpha/2$”列。例：df$=20$、双侧 5\% $\Rightarrow$ 单侧 0.025 列，$c=2.086$。OLS 中 df$=n-K$；聚类时 df$=G-1$。')
w(r'\begin{center}\small\setlength{\tabcolsep}{7pt}\renewcommand{\arraystretch}{1.0}\captionof{table}{$t$ 分布上侧临界值 $t_{\mathrm{df},1-\alpha}$}\label{tab:t}')
ta = [0.10, 0.05, 0.025, 0.01, 0.005, 0.001]
w(r'\begin{tabular}{r|cccccc}\toprule')
w(r'单侧 $\alpha$ & ' + ' & '.join(f'{a:g}' for a in ta) + r'\\')
w(r'双侧 $\alpha$ & ' + ' & '.join(f'{2*a:g}' for a in ta) + r'\\\midrule')
dfs = list(range(1, 31)) + [35, 40, 45, 50, 60, 80, 100, 120, 200, 500]
for d in dfs:
    w(f'{d} & ' + ' & '.join(f'{stats.t.ppf(1-a, d):.3f}' for a in ta) + r'\\')
w(r'$\infty$ & ' + ' & '.join(f'{stats.norm.ppf(1-a):.3f}' for a in ta) + r'\\\bottomrule')
w(r'\end{tabular}\end{center}')

# A.4 chi2
w(r'\section{\texorpdfstring{$\chi^2$}{chi2} 分布上侧临界值}')
w(r'查法：$c$ 满足 $P(\chi^2_{\mathrm{df}}>c)=\alpha$。Wald、LR、LM、Hausman、$J$ 检验都是右侧检验。例：$q=3$ 的 Wald 检验 5\% 临界值 7.815；$L-K=2$ 的 $J$ 检验 5\% 临界值 5.991。')
w(r'\begin{center}\small\setlength{\tabcolsep}{6pt}\renewcommand{\arraystretch}{1.0}\captionof{table}{$\chi^2$ 分布上侧临界值 $\chi^2_{\mathrm{df},1-\alpha}$}\label{tab:chi}')
ca = [0.90, 0.10, 0.05, 0.025, 0.01, 0.005, 0.001]
w(r'\begin{tabular}{r|ccccccc}\toprule')
w(r'df $\backslash$ $\alpha$ & ' + ' & '.join(f'{a:g}' for a in ca) + r'\\\midrule')
cdfs = list(range(1, 31)) + [35, 40, 45, 50, 60, 70, 80, 90, 100]
for d in cdfs:
    w(f'{d} & ' + ' & '.join(f'{stats.chi2.ppf(1-a, d):.3f}' for a in ca) + r'\\')
w(r'\bottomrule\end{tabular}\end{center}')
w(r'注：$\alpha=0.90$ 列是下侧 10\% 分位数（用于双侧方差检验等）。')

# A.5 F
w(r'\section{\texorpdfstring{$F$}{F} 分布上侧临界值}')
w(r'查法：$F(q,m)$ 中 $q$ 为分子自由度（约束个数，看列），$m$ 为分母自由度（$n-K$，看行）；$c$ 满足 $P(F_{q,m}>c)=\alpha$。例：$q=3$、$m=40$，5\% 临界值 2.84。$m=\infty$ 行等于 $\chi^2_{q,1-\alpha}/q$（如 $7.815/3=2.60$），即 $qF_{q,m}\dto\chi^2_q$。$q=1$ 时 $F_{1,m}=t_m^2$：$F_{1,20;0.95}=4.35=2.086^2$。')
qs = list(range(1, 11)) + [12, 15, 20, 30, 60]
ms = list(range(1, 31)) + [40, 60, 120]
for a, lab, cap in [(0.05, 'tab:f05', '5\\%'), (0.01, 'tab:f01', '1\\%'), (0.10, 'tab:f10', '10\\%')]:
    w(r'\subsection{\texorpdfstring{$F$}{F} 分布 ' + cap + r' 上侧临界值}')
    w(r'\begin{center}\scriptsize\setlength{\tabcolsep}{2.6pt}\renewcommand{\arraystretch}{1.0}\captionof{table}{$F$ 分布 ' + cap + r' 上侧临界值（列：分子 $q$；行：分母 $m$）}\label{' + lab + '}')
    w(r'\begin{tabular}{r|' + 'c' * (len(qs) + 1) + r'}\toprule')
    w(r'$m\backslash q$ & ' + ' & '.join(str(q) for q in qs) + r' & $\infty$\\\midrule')
    def fmt(x):
        return f'{x:.0f}' if x >= 1000 else (f'{x:.1f}' if x >= 100 else f'{x:.2f}')
    for m in ms:
        row = [fmt(stats.f.ppf(1-a, q, m)) for q in qs] + [fmt(1.0/stats.chi2.ppf(a, m)*m) if True else '']
        w(f'{m} & ' + ' & '.join(row) + r'\\')
    w(r'$\infty$ & ' + ' & '.join(fmt(stats.chi2.ppf(1-a, q)/q) for q in qs) + r' & 1.00\\\bottomrule')
    w(r'\end{tabular}\end{center}')

# A.6 Stock-Yogo
sy = [(1,16.4,9.0,6.7,5.5,16.4,9.0,6.7,5.5),(2,19.9,11.6,8.7,7.2,8.7,5.3,4.4,3.9),(3,22.3,12.8,9.5,7.8,6.5,4.4,3.7,3.3),
      (4,24.6,14.0,10.3,8.3,5.4,3.9,3.3,3.0),(5,26.9,15.1,11.0,8.8,4.8,3.6,3.0,2.8),(6,29.2,16.2,11.7,9.4,4.4,3.3,2.9,2.6),
      (7,31.5,17.4,12.5,9.9,4.2,3.2,2.7,2.5),(8,33.8,18.5,13.2,10.5,4.0,3.0,2.6,2.4),(9,36.2,19.7,14.0,11.1,3.8,2.9,2.5,2.3),
      (10,38.5,20.9,14.8,11.6,3.7,2.8,2.5,2.2),(15,50.4,26.8,18.7,'12.2$^{*}$',3.3,2.5,2.2,2.0),(20,62.3,32.8,22.7,17.6,3.2,2.3,2.1,1.9),
      (25,74.2,38.8,26.7,20.6,3.8,2.2,2.0,1.8),(30,86.2,44.8,30.7,23.6,3.9,2.2,1.9,1.7)]
w(r'\section{弱工具：Stock--Yogo 临界值}')
w(r'用法：先数排除工具个数 $L_2$（行），再选估计方法（2SLS 或 LIML）与可容忍的“名义 5\% 的 $t$ 检验实际水平上限”$r$（列）。第一阶段 $F$ 大于表中值，就拒绝“工具弱到使实际水平超过 $r$”。例：单个工具、$r=15\%$ 时临界值 9.0——这正是 Staiger--Stock“$F>10$”经验法则的来源。表值为 Stock \& Yogo (2005) 的模拟结果（Hansen 表 12.4）。')
w(r'\begin{center}\small\setlength{\tabcolsep}{5pt}\captionof{table}{弱工具检验的 5\% 临界值（1 个内生回归元）}\label{tab:sy}')
w(r'\begin{tabular}{r|cccc|cccc}\toprule')
w(r'& \multicolumn{4}{c|}{2SLS：最大实际水平 $r$} & \multicolumn{4}{c}{LIML：最大实际水平 $r$}\\')
w(r'$L_2$ & 0.10 & 0.15 & 0.20 & 0.25 & 0.10 & 0.15 & 0.20 & 0.25\\\midrule')
for r in sy:
    w(' & '.join(str(x) for x in r) + r'\\')
w(r'\bottomrule\end{tabular}\end{center}')
w(r'{\small $^{*}$ Hansen 表 12.4 印作 12.2；按相邻各行每 5 个工具约增加 3.0 的规律，应约为 14.6。}')
w(r'要点：2SLS 的临界值随工具个数迅速上升，LIML 的则下降——工具多时 LIML 对弱工具更稳健。Stata 中 \texttt{ivregress 2sls} 后 \texttt{estat firststage} 报告 Cragg--Donald 统计量与这些临界值。')
open('/home/user/moyang-cloud-session/books/common/critvals.tex', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('ok', len(out))
