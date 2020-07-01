import re
import json

contract = open('../../data/contracts/DPA Data Processing Addendum - 2019 - Final.txt', 'r').read()
sentence_list = re.split(r'(?<![0-9])[.!?]\s+|[.!?]?\s*\n+', contract)

sentences = []
for i, sentence in enumerate(sentence_list):
    if sentence == '':
        continue
    sentences.append({
        'id': i,
        'text': sentence,
        'type': 'regular',
        'symboleo_elements': {
            'trigger': None,
            'debtor': None,
            'creditor': None,
            'antecedent': None,
            'consequent': None,
            'asset': None
        }
    })

open('../../data/processed/dpa_labeled_draft.json', 'w').write(json.dumps(sentences))

