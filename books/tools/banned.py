# 检查单元文件中不应出现的字样（板书、老师、讲次标签、已删除部分的引用等）。
import re, sys
pat = [r'板书', r'老师', r'教师', r'任课', r'课堂', r'讲次', r'第\s*[0-9一二三四五六七八九十]+\s*讲', r'\bF2[45]\b', r'F2[45]-L', r'\[F2',
       r'本讲', r'上课', r'课上', r'笔记原', r'转写', r'习题全解', r'模拟卷', r'作业\s*Hansen', r'Hansen\s*习题', r'待核', r's0[0-9]', r'AI\s*(参考)?答案', r'课外补充', r'课件']
txt = open(sys.argv[1], encoding='utf-8').read()
bad = []
for i, line in enumerate(txt.splitlines(), 1):
    s = line.split('%')[0] if not line.lstrip().startswith('\\lst') else line
    for p in pat:
        if re.search(p, s):
            bad.append(f'  line {i}: [{p}] {line.strip()[:120]}')
            break
print('== BANNED-WORD CHECK: ' + ('OK' if not bad else f'{len(bad)} hit(s)'))
print('\n'.join(bad[:40]))
