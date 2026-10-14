#!/bin/bash
# 用法: build.sh econ_guide|econ_qr|dmml_qr   —— 编译整本书（3 遍 xelatex + makeindex），输出 build/<book>/main.pdf
set -u
BOOK=$1
ROOT=/home/user/moyang-cloud-session/books
OUT=$ROOT/build/$BOOK
mkdir -p $OUT
export TEXINPUTS="$ROOT/common//:$ROOT/$BOOK//:"
cd $ROOT/$BOOK
for i in 1 2; do xelatex -interaction=nonstopmode -halt-on-error -output-directory=$OUT main.tex > $OUT/pass$i.out 2>&1 || { echo "FAIL pass $i"; grep -n -A5 -m3 "^!" $OUT/main.log; exit 1; }; done
if [ -f $OUT/main.idx ]; then (cd $OUT && makeindex -s $ROOT/common/bookindex.ist main.idx > makeindex.out 2>&1); fi
xelatex -interaction=nonstopmode -halt-on-error -output-directory=$OUT main.tex > $OUT/pass3.out 2>&1 || { echo "FAIL pass 3"; grep -n -A5 -m3 "^!" $OUT/main.log; exit 1; }
echo "OK pages=$(pdfinfo $OUT/main.pdf | awk '/^Pages/{print $2}')"
grep -c "Overfull" $OUT/main.log | sed 's/^/overfull boxes: /'
grep -E "Reference .* undefined|multiply defined" $OUT/main.log | sort -u | head -20
