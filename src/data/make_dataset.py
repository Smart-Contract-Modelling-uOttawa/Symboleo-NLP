import re
import json

STATEMENT_RE = re.compile(r'\n+ ?\t*')
SENTENCE_RE = re.compile(r'(?<=(?<![0-9])(?<!e\.g)(?<!i\.e)[.!?])\s+|(?<=[.!?])?\s*\n+')
ALL_CLAUSE_RE = re.compile(r'\d+\.(\d+\.?)*\s+.*')
ENUMERATION_RE = re.compile(r'\(x*v*i*v*x*\)\s+')

contract_text = open('../../data/contracts/DPA Data Processing Addendum - 2019 - Final.txt', 'r').read()

statement_list = STATEMENT_RE.split(contract_text)

contract = {}
clauses = []
clause_stack = []
sentence_id = 1

for statement in statement_list:
    if ALL_CLAUSE_RE.match(statement):
        title_number, title_text = statement.split('\t')
        clause_level = len(re.findall(r'\d+', title_number))

        # remove all clauses from the stack that are the same or lower level
        while len(clause_stack) > 0 and len(re.findall(r'\d+', clause_stack[-1]['title_number'])) >= clause_level:
            # top level clauses are added to clauses list
            if len(re.findall(r'\d+', clause_stack[-1]['title_number'])) == 1:
                clauses.append(clause_stack[-1])
            clause_stack.pop()

        clause = {
            'title_number': title_number,
            'title_text': title_text.strip(),
            'sentences': [],
            'sub_clauses': []
        }

        if len(clause_stack) > 0:
            clause_stack[-1]['sub_clauses'].append(clause)

        clause_stack.append(clause)

    elif len(clause_stack) > 0:
        for sentence in SENTENCE_RE.split(statement):
            if not sentence:
                continue

            sentence_obj = {
                'id': sentence_id,
                'text': sentence,
                'type': 'regular',
                'modality': None,
                'symboleo_elements': [
                    {
                        'trigger': None,
                        'debtor': None,
                        'creditor': None,
                        'antecedent': None,
                        'consequent': None,
                        'asset': None
                    }
                ],
                'enumeration': []
            }

            if ENUMERATION_RE.match(sentence):
                clause_stack[-1]['sentences'][-1]['enumeration'].append(sentence_obj)
            else:
                clause_stack[-1]['sentences'].append(sentence_obj)

            sentence_id += 1

if len(clause_stack) > 0:
    clauses.append(clause_stack[0])

contract['clauses'] = clauses
open('../../data/processed/dpa_labeled_draft.json', 'w').write(json.dumps(contract))
