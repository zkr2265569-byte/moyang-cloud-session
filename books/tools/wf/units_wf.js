export const meta = {
  name: 'studyguide-units',
  description: 'Rewrite study-guide units from the old guide, review-fix each against the source, then condense into quick-reference units',
  phases: [
    { title: 'Write', detail: 'one agent per unit writes LaTeX from old-guide text + page images' },
    { title: 'Review', detail: 'independent agent checks completeness/correctness against source and fixes in place' },
    { title: 'Condense', detail: 'econometrics units condensed into the exam quick-reference' },
    { title: 'Glossary', detail: 'condensed glossary for the quick-reference' },
  ],
}

const B = '/home/user/moyang-cloud-session/books'
const SP = '/tmp/claude-0/-home-user-moyang-cloud-session/8dab6098-16d2-5d7f-a812-0bf7c53de774/scratchpad'
const WG = `${B}/tools/WRITING_GUIDE.md`
const QG = `${B}/tools/QR_GUIDE.md`
const CHK = `bash ${B}/tools/check_unit.sh`
const SLIDES = `机器学习课件文本：${SP}/txt/ml_ch1.txt（机器学习概述）、${SP}/txt/ml_ch2.txt（线性模型）、${SP}/txt/ml_ch3.txt（前馈神经网络）；数据挖掘课件文本：${SP}/txt/dm_fin.txt（Python 金融大数据挖掘）、${SP}/txt/dm_text.txt（Python 文本分析）。课件 PDF 原件在 ${SP}/src 下（可用 pdftoppm 渲染页面查看）。`

const WRITE_SCHEMA = { type: 'object', properties: {
  files: { type: 'array', items: { type: 'string' } }, compiled: { type: 'boolean' }, pages: { type: 'number' },
  sections: { type: 'array', items: { type: 'string' } }, n_examples: { type: 'integer' }, n_practice: { type: 'integer' },
  notes: { type: 'string' } }, required: ['files', 'compiled', 'pages', 'sections', 'notes'] }
const REVIEW_SCHEMA = { type: 'object', properties: {
  compiled: { type: 'boolean' }, pages: { type: 'number' },
  added: { type: 'array', items: { type: 'string' } }, fixed: { type: 'array', items: { type: 'string' } },
  remaining: { type: 'array', items: { type: 'string' } } }, required: ['compiled', 'pages', 'added', 'fixed', 'remaining'] }
const QR_SCHEMA = { type: 'object', properties: {
  file: { type: 'string' }, compiled: { type: 'boolean' }, pages: { type: 'number' },
  sections: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } }, required: ['file', 'compiled', 'pages', 'sections', 'notes'] }

const units = args.units

function sib(u) {
  if (!u.siblings || !u.siblings.length) return '（本章只有这一个单元）'
  return u.siblings.map(s => `${s.id}：${s.sec_titles.join('；')}`).join(' ／ ')
}
function chkArgs(u, file, mode) {
  return `${CHK} ${file} ${u.chapter || 1} ${mode}` + (u.first ? '' : ` "${u.chapter_title}"`)
}

// ---------------- 教材单元：撰写 ----------------
function writePrompt(u) {
  if (u.id === 'UAPP1') return `你负责《高级计量经济学》复习教材（新版）的附录 B、C、D。先完整阅读写作规范 ${WG} 并严格遵守（尤其第 1 节“必须删除的内容”）。
旧版原文：${u.source}（旧版印刷页 710–749；每页前有页面图片路径，表格与公式以图片为准）。其中旧版附录 A（710–717）与附录 B 核心公式速查（718–731）**不用写**（附录 A 已另行生成，附录 B 公式速查已取消）。你要写：
1. 旧版附录 C「Stata / R 命令速查」→ 新文件 ${B}/econ_guide/units/appB_stata.tex，以 \\chapter{Stata / R 命令速查} 开头；
2. 旧版附录 D「英文答题句式与模板」→ 新文件 ${B}/econ_guide/units/appC_english.tex，以 \\chapter{英文答题句式与模板} 开头；
3. 旧版附录 E「全书记号对照」→ 新文件 ${B}/econ_guide/units/appD_notation.tex，以 \\chapter{全书记号对照} 开头；删去旧版 E.7“讲次—主题—本书章节对照”整节。
要求：保留全部命令、句式、模板、记号条目（删除授课来源相关内容和指向模拟卷/习题全解的内容）；命令写在 lstlisting 或 \\texttt 中，确保 Stata/R 语法正确（如有过时或错误写法直接改正）；记号对照中的章号按新版全书结构（规范第 2 节；新版无第 18–28 章）。示范骨架若引用 2025 真题，保留。
分别编译检查：${CHK} <文件> 1 guide（三个文件各查一次），直到 COMPILE OK 且 BANNED-WORD CHECK: OK。最后用 StructuredOutput 返回（files 列出三个文件）。`
  if (u.id === 'UGa' || u.id === 'UGb') {
    const ab = u.id === 'UGa'
    return `你负责《高级计量经济学》复习教材（新版）附录 E「中英术语对照表」的${ab ? '前半部分（英文首字母 A–L）' : '后半部分（英文首字母 M–Z）'}。先阅读写作规范 ${WG} 第 1、6、7、8 节并遵守。
旧版原文：${u.source}（旧版术语表的若干页，页前有页面图片路径；表中公式以图片为准）。注意首末页可能包含不属于你负责字母范围的条目，忽略它们。
输出文件：${B}/econ_guide/units/${ab ? 'appE_glossary_a.tex' : 'appE_glossary_b.tex'}。
${ab ? '文件以 \\chapter{中英术语对照表} 开头，紧跟两三行用法说明（按英文字母排序；“简释”给出一句话含义；正文中的页码请查书末英文术语索引）。' : '不要写 \\chapter（接在 A–L 部分之后）。'}
格式：每个首字母一组，组标题写 \\section*{X}\\addcontentsline{toc}{section}{X}；组内用 longtable，三列：English（p{4.6cm}）| 中文（p{3.2cm}）| 简释（自动换行），表头用 booktabs。
要求：保留旧版你负责范围内的全部术语；同一术语的重复条目合并为一条（简释取更完整者）；简释中的公式改用 LaTeX 数学（如 $\\alpha_i$、$E(z_i x_i')$）；删除“Hansen 11.11”“作业”“习题”“板书”“讲次”一类来源标注；简释准确、简洁。
编译检查：${CHK} <文件> 1 guide${ab ? '' : ' "中英术语对照表"'}，直到 COMPILE OK 且 BANNED-WORD CHECK: OK。用 StructuredOutput 返回。`
  }
  return `你是《高级计量经济学》博士资格考试复习教材（新版）的撰写者，负责单元 ${u.id}。
第一步：完整阅读写作规范 ${WG}，严格遵守其中每一条（尤其第 1 节“必须删除的内容”、第 3 节标题要求、第 4 节推导写法）。

【本单元】
- 属于第 ${u.chapter} 章「${u.chapter_title}」。${u.first ? '这是本章第一个单元：文件以 \\chapter{' + u.chapter_title + '} 开头，紧跟“本章导读”。' : '这是本章的后续单元：不要写 \\chapter，直接从 \\section 开始。'}${u.last && u.chapter !== 17 ? '这是本章最后一个单元：以 \\section{本章小结} 收尾（规范第 3 节）。' : ''}
- 你负责旧版这些节：${u.sec_titles.join('；')}。旧版印刷页 ${u.old_pages[0]}–${u.old_pages[1]}（首末页可能夹带不属于你的节，忽略那部分）。
- 本章其他单元负责（不要重复写它们的内容，可用一句话衔接）：${sib(u)}
- 旧版原文：${u.source}。文件开头列出了旧版目录中属于本单元的全部条目——这是**必须覆盖的知识点清单**。每页正文前标注了该页图片路径。
- 文本中的公式是乱的（上下标、分式、求和号被打散），**凡含公式的页面都要用 Read 查看页面图片，公式以图片为准**。旧版中“老师板书要点”盒内的内容也是知识点，必须融入正文（但不得提及“老师/板书”）。
- 输出文件：${u.guide_out}

【工作步骤】
1. 读规范；通读本单元原文与全部相关页面图片；列出知识点清单，设计新的节/小节/小小节结构（由浅入深、逻辑连贯、标题细致具体）。
2. 撰写：分多次写入输出文件（先 Write 开头，再用 Bash cat >> 追加）。推导一步一行、每行 \\why{理由}；例题完整求解；保留旧版正文中的练习（含完整答案）。
3. 编译检查：${chkArgs(u, u.guide_out, 'guide')}，反复修正直到 COMPILE OK、BANNED-WORD CHECK: OK、尽量没有超过 10pt 的 Overfull。
4. 自查：对照知识点清单逐条确认已覆盖；抽查渲染页面（pdftoppm + Read）确认公式与版面正确。
完成后用 StructuredOutput 返回：files=[输出文件]、compiled、pages、sections（新版各 \\section 标题）、n_examples、n_practice、notes（如有拿不准之处写在这里）。`
}

// ---------------- 教材单元：审校 ----------------
function reviewPrompt(u, w) {
  const files = (w && w.files && w.files.length) ? w.files.join('、') : u.guide_out
  return `你是《高级计量经济学》复习教材（新版）的独立审校者，负责单元 ${u.id}。别人已写好新版文件：${files}。
先阅读写作规范 ${WG}。旧版原文：${u.source}（开头是必须覆盖的知识点清单；每页前有页面图片路径——公式以图片为准，文本中的公式是乱的）。
你的任务是**直接修改新版文件**，使之达到出版质量：
1. 完整性：逐页对照旧版（文本 + 图片），确认旧版中每个知识点、公式、推导步骤、结论、例子、练习、注意事项、对比表都在新版中（规范要求删除的除外：授课来源字样、模拟卷/习题全解/公式速查的指引等）。逐条核对知识点清单。缺的按规范写法补上，放在逻辑上合适的位置。
2. 正确性：逐个核查新版中每个公式和每一步推导（正负号、转置、求逆的位置、下标、维度、期望与概率极限、分布与自由度、成立条件），以及每个文字结论；有错就改。拿不准时 grep Hansen 文本 ${SP}/txt/hansen.txt 核实。
3. 清楚：推导是否每步有 \\why 理由、有无跳步；符号是否先定义后使用；标题是否具体细致（目录能当索引）；有无啰嗦、重复、含糊的句子；例题解答是否完整。
4. 规范：banned 字样清零（老师、板书、讲次、课堂、课外、待核、习题全解、模拟卷、AI 等）；编译通过。
编译检查命令：${u.id === 'UAPP1' ? CHK + ' <文件> 1 guide（三个文件各查一次）' : (u.id === 'UGb' ? CHK + ' <文件> 1 guide "中英术语对照表"' : chkArgs(u, u.guide_out, 'guide'))}。改完后必须再编译确认通过。
用 StructuredOutput 返回：compiled、pages、added（补上的知识点）、fixed（改正的错误）、remaining（仍需注意的问题，没有则空）。`
}

// ---------------- 速查册单元（高级计量，由教材单元压缩） ----------------
function condensePrompt(u) {
  if (u.id === 'UAPP1') return `你负责《高级计量经济学》考场速查册的附录「英文答题模板与 Stata 命令速查」。先阅读速查册规范 ${QG} 并遵守。
来源：已定稿的教材附录 ${B}/econ_guide/units/appC_english.tex（英文答题句式与模板）与 ${B}/econ_guide/units/appB_stata.tex（Stata/R 命令）。
输出：${B}/econ_qr/units/qr_appB.tex，以 \\chapter{英文答题模板与 Stata 命令速查} 开头；约 4 页（英文句式约 2.5 页：作答结构模板、各类题型的高频句式；Stata/R 约 1.5 页：最常用命令一览表）。
编译检查：${CHK} ${B}/econ_qr/units/qr_appB.tex 1 qr。用 StructuredOutput 返回。`
  return `你是《高级计量经济学》考场速查册的撰写者，负责单元 ${u.id}。先完整阅读速查册规范 ${QG} 并严格遵守。
来源：已定稿、已审校的教材单元 ${u.guide_out}（以它为准，无需再看旧版）。
输出：${u.qr_out}；篇幅目标约 ${u.qr_pages} 页（±25%）。
- 属于第 ${u.chapter} 章「${u.chapter_title}」。${u.first ? '本章第一个单元：以 \\chapter{' + u.chapter_title + '} 开头。' : '后续单元：不要写 \\chapter。'}
- 教材单元中的每个 \\section 在速查册中都要有同序、同名（可略缩短）的 \\section，不多不少（两书节号一致）。\\section 以下自由安排，标题要具体可检索。
- ${u.chapter === 17 ? '本单元是 2025 年真题精讲：保留每一小问的完整推导（每步 \\why）、结论与英文标准答案（english 盒），以及常见错误；压缩文字说明。' : '只写定义、条件、公式、结论、对比表、关键推导骨架、易错点、少量英文一句话；不写例题与练习。'}
编译检查：${chkArgs(u, u.qr_out, 'qr')}，直到 COMPILE OK、BANNED-WORD CHECK: OK；检查页数是否在目标范围内，渲染一两页确认版面紧凑易读。
用 StructuredOutput 返回：file、compiled、pages、sections、notes。`
}

// ---------------- 速查册单元（数据挖掘与机器学习，由旧版直接压缩） ----------------
function dmmlWritePrompt(u) {
  const app = u.chapter === 0
  return `你是《数据挖掘与机器学习》博士资格考试**考场速查册**的撰写者，负责单元 ${u.id}。先完整阅读速查册规范 ${QG} 并严格遵守。
【本单元】
- ${app ? '本单元是附录「' + u.chapter_title.replace(/^附录 [A-C]　/, '') + '」：文件以 \\chapter{' + u.chapter_title.replace(/^附录 [A-C]　/, '') + '} 开头（排在 \\appendix 之后，自动编为附录）。' : '属于第 ' + u.chapter + ' 章「' + u.chapter_title + '」。' + (u.first ? '本章第一个单元：以 \\chapter{' + u.chapter_title + '} 开头。' : '后续单元：不要写 \\chapter。')}
- ${app ? '来源为旧版对应附录。' : '负责旧版这些节：' + u.sec_titles.join('；') + '。本章其他单元负责：' + sib(u) + '（不要重复）。'}
- 旧版原文：${u.source}（旧版印刷页 ${u.old_pages[0]}–${u.old_pages[1]}；开头是旧版目录中属于本单元的条目 = 必须覆盖的知识点清单；每页前有页面图片路径。文本中公式是乱的，公式页要用 Read 看图片，以图片为准）。
- 核对课件是否有遗漏：${SLIDES}
- 输出：${u.qr_out}；篇幅目标约 ${u.qr_pages} 页（±25%）。
【要求】
- 速查册**不含任何习题、例题和模拟题**（手算类知识点给出公式与计算步骤要点即可，可附一行极简数值示意）。
- 旧版每个知识点都要有对应内容（哪怕一行）；公式、算法步骤、超参数含义、代码模板必须准确（Python 代码按当前库版本写法，如 Selenium 4 的 find_element(By.XPATH, ...)）。
- 不得出现老师、教师、课件、板书、课堂、待核、AI、模拟卷、习题全解等字样；旧版“课件原写法/课件错误”之类说明只保留正确写法；“课外补充”改称“拓展”（\\tagext）。
- 标题具体可检索（目录当索引用）；多用表格与紧凑列表。
编译检查：${CHK} ${u.qr_out} ${u.chapter || 1} qr${u.first || app ? '' : ' "' + u.chapter_title + '"'}，直到 COMPILE OK、BANNED-WORD CHECK: OK，页数在目标范围内。
用 StructuredOutput 返回：file、compiled、pages、sections、notes。`
}
function dmmlReviewPrompt(u) {
  return `你是《数据挖掘与机器学习》考场速查册的独立审校者，负责单元 ${u.id}。别人已写好：${u.qr_out}。先阅读速查册规范 ${QG}。
旧版原文：${u.source}（开头是必须覆盖的知识点清单；每页前有页面图片路径，公式以图片为准）。课件文本：${SLIDES}
请**直接修改文件**：
1. 完整性：逐条核对知识点清单与旧版正文，凡是旧版有而速查册没有的知识点（定义、公式、算法步骤、性质、对比、代码函数/参数、易错点）都补上（简洁地）；习题、例题、模拟题不要补。
2. 正确性：核查每个公式（符号、下标、求和范围、梯度与更新式的正负号、归一化常数）、每个算法步骤、每段代码（语法、库函数名与参数是否符合当前版本），有错就改。
3. 速查性：标题是否具体可检索；排版是否紧凑；有无啰嗦重复；篇幅目标约 ${u.qr_pages} 页（±25%）。
4. 规范：banned 字样清零；编译通过：${CHK} ${u.qr_out} ${u.chapter || 1} qr${u.first || u.chapter === 0 ? '' : ' "' + u.chapter_title + '"'}。
用 StructuredOutput 返回：compiled、pages、added、fixed、remaining。`
}

const results = await pipeline(units,
  u => u.book === 'dmml'
    ? agent(dmmlWritePrompt(u), { label: `qrwrite:${u.id}`, phase: 'Write', schema: QR_SCHEMA })
    : agent(writePrompt(u), { label: `write:${u.id}`, phase: 'Write', schema: WRITE_SCHEMA }),
  (w, u) => (u.book === 'dmml'
    ? agent(dmmlReviewPrompt(u), { label: `qrreview:${u.id}`, phase: 'Review', schema: REVIEW_SCHEMA })
    : agent(reviewPrompt(u, w), { label: `review:${u.id}`, phase: 'Review', schema: REVIEW_SCHEMA })).then(r => ({ id: u.id, write: w, review: r })),
  (wr, u) => (u.book === 'econ' && u.id !== 'UGa' && u.id !== 'UGb')
    ? agent(condensePrompt(u), { label: `condense:${u.id}`, phase: 'Condense', schema: QR_SCHEMA }).then(q => ({ ...wr, qr: q }))
    : wr,
)

let gloss = null
if (args.glossary_qr) {
  phase('Glossary')
  gloss = await agent(`你负责《高级计量经济学》考场速查册的附录「中英术语速查」。先阅读速查册规范 ${QG}。
来源：已定稿的教材附录术语表 ${B}/econ_guide/units/appE_glossary_a.tex 与 ${B}/econ_guide/units/appE_glossary_b.tex。
输出：${B}/econ_qr/units/qr_glossary.tex，以 \\chapter{中英术语速查} 开头；约 4 页：挑选考试最可能出现的约 300–400 个英文术语，按字母排序，紧凑两栏（可用 multicols{2} 内的简单列表或 longtable），每条“English — 中文（必要时 5–10 字简释）”。
编译检查：${CHK} ${B}/econ_qr/units/qr_glossary.tex 1 qr。用 StructuredOutput 返回。`, { label: 'condense:glossary', phase: 'Glossary', schema: QR_SCHEMA })
}
return { results, gloss }
