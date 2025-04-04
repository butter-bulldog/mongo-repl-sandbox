#
# 2.4ダンプ内のmetadata.jsonを修正するスクリプト
# 下記を修正しないと4.0にリストアできない
# ・optionsを削除する
# ・indexesのkeyの値がTrueになっているものを1に変換する
#
from glob import glob
import json

for filename in sorted(glob('../tmp/dump/*/*.metadata.json')):
    with open(filename, 'r') as f:
        data = json.loads(f.read())
        if 'options' in data:
            del data['options']
        if 'indexes' in data:
            for index in data['indexes']:
              if 'key' in index:
                index['key'] = {k: (1 if v is True else v) for k, v in index['key'].items()}
    with open(filename, 'w') as f:
        json.dump(data, f)