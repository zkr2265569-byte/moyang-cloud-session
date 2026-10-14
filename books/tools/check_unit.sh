#!/bin/bash
# 用法: check_unit.sh <unit.tex 绝对路径> <章号> [qr] [章标题(若单元本身不含\chapter)]
# 编译单个单元，报告错误、未定义引用、Overfull 警告与页数。
set -u
F="$1"; CH="$2"; MODE="${3:-guide}"; TITLE="${4:-}"
ROOT=/home/user/moyang-cloud-session/books
B=$(mktemp -d /tmp/claude-0/unitbuild.XXXXXX)
export TEXINPUTS="$ROOT/common//:$ROOT/tools//:$(dirname "$F")//:"
PRE="\\def\\unitfile{$F}\\def\\unitchap{$CH}"
[ "$MODE" = "qr" ] && PRE="$PRE\\def\\qrmode{1}"
[ -n "$TITLE" ] && PRE="$PRE\\def\\unitchaptitle{$TITLE}"
cd "$B"
timeout 600 xelatex -interaction=nonstopmode -halt-on-error -jobname=unit "$PRE\\input{unit_wrapper.tex}" > build.out 2>&1
RC=$?
if [ $RC -eq 0 ]; then timeout 600 xelatex -interaction=nonstopmode -halt-on-error -jobname=unit "$PRE\\input{unit_wrapper.tex}" > build.out 2>&1; RC=$?; fi
if [ $RC -ne 0 ]; then
  echo "== COMPILE FAILED (rc=$RC). First error context:"
  grep -n -A6 -m3 "^!" unit.log | head -40
  echo "-- last lines of log:"; tail -15 unit.log
else
  P=$(pdfinfo unit.pdf 2>/dev/null | awk '/^Pages/{print $2}')
  echo "== COMPILE OK. pages=$P  pdf=$B/unit.pdf"
  echo "-- Overfull hbox > 10pt (前10条):"; grep -E "Overfull \\\\hbox \(([1-9][0-9]+|[0-9]{3,})\.[0-9]+pt" unit.log | head -10
  echo "-- Undefined refs/cmds:"; grep -E "undefined|Undefined" unit.log | sort -u | head -10
fi
python3 -I "$ROOT/tools/banned.py" "$F"
