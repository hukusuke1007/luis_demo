#!/bin/sh
# 整形
python3 export_schema.py -> output.json

# utf-8へ変換
# nkf -w --overwrite output.json

echo 'OK'
