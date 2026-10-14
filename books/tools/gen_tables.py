# 生成附录 A：统计分布临界值表（scipy 精确计算）。输出 common/critvals.tex
from scipy import stats
import math
out = []
w = out.append
# A.1 查表总指南：速查册（qr）用精简版，复习教材用完整版（含统计量一览、三种决策方式、插值与大自由度近似、例题）
w(r'\ifqr')
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

w(r'\else')
w(r'''本附录给出考场上需要的常用临界值：标准正态分布函数 $\Phi(z)$、正态临界值，$t$ 分布、$\chi^2$ 分布与 $F$ 分布（10\%、5\%、1\%）的上侧临界值，以及弱工具的 Stock--Yogo 临界值。前几张表的每一个数都用 Python \texttt{scipy.stats}（\texttt{norm.cdf}、\texttt{t.ppf}、\texttt{chi2.ppf}、\texttt{f.ppf}）精确计算后四舍五入；自由度为 $\infty$ 的行由极限分布直接算出（$t_\infty=N(0,1)$，$F(q,\infty)=\chi^2_q/q$，$F(\infty,m)=m/\chi^2_m$ 的相应分位数）。Stock--Yogo 表照录 Hansen 表 12.4。本节先说明“什么统计量查哪张表”，再给出几道查表例题。

\section{查表总指南}

\subsection{检验统计量、原假设下的分布与对应的表：一览}

下表列出全书出现的检验统计量。“正文”一栏为该检验在本书中所在的章。

{\small\renewcommand{\arraystretch}{1.12}\begin{longtable}{@{}>{\raggedright\arraybackslash}p{4.2cm}>{\raggedright\arraybackslash}p{2.8cm}>{\raggedright\arraybackslash}p{4.0cm}>{\raggedright\arraybackslash}p{1.8cm}>{\raggedright\arraybackslash}p{1.5cm}@{}}
\toprule
\textbf{统计量} & \textbf{$H_0$ 下（渐近）分布} & \textbf{拒绝 $H_0$（水平 $\alpha$）} & \textbf{查表} & \textbf{正文}\\
\midrule
\endfirsthead
\toprule
\textbf{统计量} & \textbf{$H_0$ 下（渐近）分布} & \textbf{拒绝 $H_0$（水平 $\alpha$）} & \textbf{查表} & \textbf{正文}\\
\midrule
\endhead
\bottomrule
\endlastfoot
$t=(\hat\theta-\theta_0)/\mathrm{se}(\hat\theta)$，大样本（同方差、HC 或 HAC 标准误） & $N(0,1)$ & 双侧 $|t|>z_{1-\alpha/2}$；右侧 $t>z_{1-\alpha}$ & 表 \ref{tab:zcrit}、\ref{tab:phi} & 第 6 章\\
\addlinespace[1pt]
同上，正态同方差误差（精确分布） & $t_{n-K}$ & $|t|>t_{n-K,1-\alpha/2}$ & 表 \ref{tab:t} & 第 4、6 章\\
\addlinespace[1pt]
聚类稳健 $t$（Stata 默认做法） & $t_{G-1}$（$G$ 为簇数） & $|t|>t_{G-1,1-\alpha/2}$ & 表 \ref{tab:t} & 第 5 章\\
\addlinespace[1pt]
Wald 统计量 $W$（$q$ 个约束，含 GMM 的 Wald） & $\chi^2_q$ & $W>\chi^2_{q,1-\alpha}$ & 表 \ref{tab:chi} & 第 6、8 章\\
\addlinespace[1pt]
两步 $F$ / 矩阵形式 $F$（正态同方差） & $F(q,n-K)$ & $F>F_{q,n-K;1-\alpha}$ & 表 \ref{tab:f05}、\ref{tab:f01} & 第 6 章\\
\addlinespace[1pt]
LR、LM（$nR^2$ 形式）、GMM 距离统计量 $D$ & $\chi^2_q$ & 同 Wald & 表 \ref{tab:chi} & 第 6、8 章\\
\addlinespace[1pt]
第一阶段 $F$（弱工具） & 不用常规临界值 & $F>10$（保守标准 30），或大于 Stock--Yogo 临界值 & 表 \ref{tab:sy} & 第 9 章\\
\addlinespace[1pt]
控制函数 $t$（内生性检验） & $N(0,1)$ & $|t|>1.96$（5\%） & 表 \ref{tab:zcrit} & 第 9 章\\
\addlinespace[1pt]
Hausman：IV vs OLS / FE vs RE & $\chi^2_{k_2}$ / $\chi^2_K$ & $H>\chi^2_{\mathrm{df},1-\alpha}$ & 表 \ref{tab:chi} & 第 9、11 章\\
\addlinespace[1pt]
Hansen $J$ / Sargan（过度识别） & $\chi^2_{L-K}$ & $J>\chi^2_{L-K,1-\alpha}$ & 表 \ref{tab:chi} & 第 9、12 章\\
\addlinespace[1pt]
$C$ 统计量（子集过度识别） & $\chi^2_{L_b}$ & $C>\chi^2_{L_b,1-\alpha}$ & 表 \ref{tab:chi} & 第 9 章\\
\addlinespace[1pt]
Arellano--Bond AR($j$) 检验 $m_j$ & $N(0,1)$ & AR(1) 应拒绝，AR(2) 不应拒绝 & 表 \ref{tab:zcrit} & 第 12 章\\
\addlinespace[1pt]
截面相关：单对 $\sqrt T\hat\rho_{ij}$ / $T\hat\rho_{ij}^2$ & $N(0,1)$ / $\chi^2_1$ & $|\sqrt T\hat\rho_{ij}|>1.96$（5\%） & 表 \ref{tab:zcrit} & 第 14 章\\
\addlinespace[1pt]
截面相关：Breusch--Pagan $LM=T\sum_{i<j}\hat\rho_{ij}^2$ & $\chi^2_{N(N-1)/2}$ & 自由度大，用下文的大自由度近似 & 表 \ref{tab:chi} & 第 14 章\\
\addlinespace[1pt]
截面相关：$CD^*$（右侧）、Pesaran $CD$（双侧） & $N(0,1)$ & $CD^*>1.645$；$|CD|>1.96$（5\%） & 表 \ref{tab:zcrit} & 第 14 章\\
\addlinespace[1pt]
事件研究前导系数联合检验（$m$ 个前导项） & $\chi^2_m$（或 $F=W/m$） & $W>\chi^2_{m,1-\alpha}$ & 表 \ref{tab:chi} & 第 15 章\\
\addlinespace[1pt]
SCM 安慰剂（置换）检验 & 无参数分布 & $p=$ 处理单位效应的秩 $/N$ & 不查表 & 第 16 章\\
\end{longtable}}

表中 $k_2$ 为内生回归元个数，$K$ 在 FE vs RE 的 Hausman 检验中指被比较的时变回归元个数；$L$ 为工具个数，$L_b$ 为子集检验中被检验的那部分工具个数。$\chi^2$、$F$、$J$、Hausman 检验都是\key{右侧}检验。

\subsection{三种等价的决策方式：拒绝域、\texorpdfstring{$p$}{p} 值、置信区间}

\begin{enumerate}
  \item \key{拒绝域法}：统计量落在“比临界值更极端”的一侧就拒绝 $H_0$。双侧 $t$ 检验用 $z_{1-\alpha/2}$（5\% 为 1.96）；$\chi^2$、$F$ 检验都是右侧检验，只看上侧临界值。
  \item \key{$p$ 值法}：$p<\alpha$ 就拒绝。表中只能“夹出”$p$ 值的范围，例如 $\chi^2_{3,0.95}=7.815<W=9.1<\chi^2_{3,0.975}=9.348$，就写 $0.025<p<0.05$。双侧正态检验的 $p=2[1-\Phi(|t|)]$ 可由表 \ref{tab:phi} 精确算出。
  \item \key{置信区间法}：$\hat\theta\pm c\cdot\mathrm{se}(\hat\theta)$ 不包含 $\theta_0$ $\iff$ 双侧检验在相应水平拒绝 $H_0:\theta=\theta_0$（$c$ 取 $z_{1-\alpha/2}$ 或 $t_{\mathrm{df},1-\alpha/2}$）。
\end{enumerate}

\subsection{自由度不在表中时：取保守值、按 \texorpdfstring{$1/\mathrm{df}$}{1/df} 插值或用大自由度近似}

\subsubsection{保守做法：取较小的相邻自由度}
对 $t$ 分布与 $F$ 分布的分母自由度而言，自由度越小，临界值越大，检验越保守。例：$t_{45}$ 用 $t_{40}$ 的 2.021（精确值 2.014）。

\subsubsection{按 \texorpdfstring{$1/\mathrm{df}$}{1/df} 线性插值}
临界值对 $1/\mathrm{df}$ 近似线性。例：
\begin{align*}
t_{45,0.975}&\approx t_{40,0.975}+\bigl(t_{50,0.975}-t_{40,0.975}\bigr)\cdot\frac{1/45-1/40}{1/50-1/40} \why{对 $1/\mathrm{df}$ 线性插值}\\
&=2.021+(2.009-2.021)\times 0.556 \why{查表 \ref{tab:t}}\\
&=2.014. \why{与精确值相同}
\end{align*}

\subsubsection{大样本：\texorpdfstring{$t\approx N(0,1)$}{t ~ N(0,1)}，\texorpdfstring{$qF\approx\chi^2_q$}{qF ~ chi2}}
$\mathrm{df}\ge 120$ 时 $t\approx N(0,1)$；$F(q,m)$ 在 $m\to\infty$ 时趋于 $\chi^2_q/q$（$F$ 表中 $m=\infty$ 的行），这就是“$qF\approx W\sim\chi^2_q$”。

\subsubsection{大自由度 \texorpdfstring{$\chi^2$}{chi2}（\texorpdfstring{$\mathrm{df}>100$}{df>100}）：Wilson--Hilferty 近似与正态近似}
截面相关的 LM 检验（$\mathrm{df}=N(N-1)/2$）、工具很多的 Hansen $J$ 检验（$\mathrm{df}=L-K$）常超出 $\chi^2$ 表。记 $z=z_{1-\alpha}$（取自表 \ref{tab:zcrit}），两个近似为
\[
\text{Wilson--Hilferty：}\quad \chi^2_{k,1-\alpha}\approx k\Bigl(1-\frac{2}{9k}+z\sqrt{\frac{2}{9k}}\Bigr)^3;\qquad
\text{正态近似：}\quad \chi^2_{k,1-\alpha}\approx k+z\sqrt{2k}.
\]
正态近似的依据是 $\E\chi^2_k=k$、$\Var\chi^2_k=2k$（第 1 章）与中心极限定理。Wilson--Hilferty 近似极准：$k=100$、5\% 时给出 124.340（精确值 124.342）；$k=190$ 时给出 223.159（精确值 223.160）。正态近似偏小：$k=100$ 时只有 123.26。

\subsection{查表例题}

\begin{exmp}[Wald 检验，\texorpdfstring{$q=3$}{q=3}]
检验 $H_0:\beta_1=\beta_2=\beta_3=0$，用聚类稳健方差算得 $W=9.1$。在 5\% 与 1\% 水平下是否拒绝？Stata 报告的 $F$ 值是多少，如何判断？
\solution
$H_0$ 下 $W\dto\chi^2_3$。查表 \ref{tab:chi} 中 $\mathrm{df}=3$ 一行：$\chi^2_{3,0.95}=7.815$，$\chi^2_{3,0.99}=11.345$。由 $7.815<9.1<11.345$：5\% 水平拒绝，1\% 水平不拒绝。又 $9.1<\chi^2_{3,0.975}=9.348$，所以 $0.025<p<0.05$；精确 $p=0.028$。

Stata 的 \texttt{test} 报告 $F=W/q=9.1/3=3.03$，应与 $F(3,\infty)$ 的 5\% 临界值 $7.815/3=2.60$ 比较：$3.03>2.60$，结论相同。
\end{exmp}

\begin{exmp}[小样本 \texorpdfstring{$t$}{t} 与聚类 \texorpdfstring{$t$}{t}]
(1) 正态同方差回归，$n=23$，$K=3$（含截距），$t=2.30$。双侧 5\% 检验是否拒绝？右侧单侧 5\% 临界值是多少？(2) 若按 30 个省聚类，双侧 5\% 临界值是多少？
\solution
(1) $\mathrm{df}=n-K=20$，双侧 5\% 临界值 $t_{20,0.975}=2.086$；$2.30>2.086$，拒绝。右侧单侧 5\% 临界值 $t_{20,0.95}=1.725$。

(2) Stata 对聚类 $t$ 用 $t_{G-1}=t_{29}$，双侧 5\% 临界值 2.045，比 1.96 大。
\end{exmp}

\begin{exmp}[\texorpdfstring{$F$}{F} 检验与正态 \texorpdfstring{$p$}{p} 值]
(1) 无约束模型 $n=44$、$K=4$，检验 $q=3$ 个排除约束，得 $F=3.5$。5\% 水平是否拒绝？(2) 大样本 $t=2.17$，双侧 $p$ 值是多少？
\solution
(1) 分母自由度 $n-K=40$，查表 \ref{tab:f05}：$F_{3,40;0.95}=2.84$。$3.5>2.84$，5\% 水平拒绝。

(2) 查表 \ref{tab:phi}：$\Phi(2.17)=0.9850$，所以双侧 $p=2[1-\Phi(2.17)]=2(1-0.9850)=0.030$。
\end{exmp}

\begin{exmp}[大自由度 \texorpdfstring{$\chi^2$}{chi2}：动态面板的 Hansen \texorpdfstring{$J$}{J}]
Arellano--Bond 差分 GMM，数据为 $y_{i0},\dots,y_{iT}$，$T=20$，只估计一个参数 $\rho$（$K=1$），使用全部滞后水平值作工具。求 $J$ 检验的 5\% 临界值。
\solution
第 $t$ 个差分方程（$t=2,\dots,T$）的工具为 $y_{i0},\dots,y_{i,t-2}$，共 $t-1$ 个，所以
\begin{align*}
L&=\sum_{t=2}^{T}(t-1) \why{逐个方程数工具}\\
&=\frac{T(T-1)}{2}=190. \why{$T=20$}
\end{align*}
$J\dto\chi^2_{L-K}=\chi^2_{189}$，超出 $\chi^2$ 表。用 Wilson--Hilferty 近似（$z=1.645$）：
\begin{align*}
\chi^2_{189,0.95}&\approx 189\Bigl(1-\frac{2}{9\times189}+1.645\sqrt{\frac{2}{9\times189}}\Bigr)^3 \why{Wilson--Hilferty}\\
&=189\times(1-0.00118+0.05640)^3=189\times1.05523^3 \why{逐项计算}\\
&\approx 222.07, \why{精确值 222.08}
\end{align*}
工具这么多时 $J$ 检验功效很低，$p$ 值常虚高（第 12 章），应限制工具个数（\texttt{collapse}、\texttt{laglimits()}）并报告工具数。
\end{exmp}''')
w(r'\fi')

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
w(r'\subsection{第一阶段 \texorpdfstring{$F$}{F} 的弱工具临界值（一个内生变量，5\% 检验）}')
w(r'用法（见第 9 章 Stock--Yogo 临界值一节）：先数排除工具个数 $L_2$（行），再选估计方法（2SLS 或 LIML）与可容忍的“名义 5\% 的 $t$ 检验实际水平上限”$r$（列）。第一阶段 $F$ 大于表中值，就拒绝“工具弱到使实际水平超过 $r$”。例：单个工具、$r=15\%$ 时临界值 9.0（Hansen 用 $\tau^2=1.7$ 算得 8.7，Stock--Yogo 用 $\tau^2=1.82$ 得 9.0）——Staiger--Stock“$F>10$”的经验法则正是由这类计算得出的。表值不是用 scipy 计算的，而是 Stock \& Yogo (2005) 的模拟结果，照录 Hansen 表 12.4。')
w(r'\begin{center}\small\setlength{\tabcolsep}{5pt}\captionof{table}{弱工具检验的 5\% 临界值（1 个内生回归元）}\label{tab:sy}')
w(r'\begin{tabular}{r|cccc|cccc}\toprule')
w(r'& \multicolumn{4}{c|}{2SLS：最大实际水平 $r$} & \multicolumn{4}{c}{LIML：最大实际水平 $r$}\\')
w(r'$L_2$ & 0.10 & 0.15 & 0.20 & 0.25 & 0.10 & 0.15 & 0.20 & 0.25\\\midrule')
for r in sy:
    w(' & '.join(str(x) for x in r) + r'\\')
w(r'\bottomrule\end{tabular}\end{center}')
w(r'{\small $^{*}$ 照录 Hansen 表 12.4。此格与相邻两行（$L_2=10$ 时 11.6，$L_2=20$ 时 17.6）相比明显偏小，疑为原表排印错误；按相邻各行每增加 5 个工具约增加 3.0 的规律推算约为 14.6，判断时用 14.6 较为稳妥。}')
w('')
w(r'要点：2SLS 的临界值随工具个数迅速上升，LIML 的则下降——工具多时 LIML 对弱工具更稳健。Stata 中 \texttt{ivregress 2sls}（或 \texttt{liml}）\key{不加}稳健方差选项时，其后的 \texttt{estat firststage} 才报告 Cragg--Donald 统计量与这些临界值。')
open('/home/user/moyang-cloud-session/books/common/critvals.tex', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('ok', len(out))
