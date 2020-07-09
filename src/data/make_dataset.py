import re
import json

STATEMENT_RE = re.compile(r'\n+ ?\t*')
SENTENCE_RE = re.compile(r'(?<=(?<![0-9])[.!?])\s+|(?<=[.!?])?\s*\n+')
CLAUSE_RE = re.compile(r'\d+\.\s+.*')
SUB_CLAUSE_RE = re.compile(r'\d+\.\d+\s+.*')
SUB_SUB_CLAUSE_RE = re.compile(r'\d+\.\d+\.\d+\s+.*')

contract_text = open('../../data/contracts/DPA Data Processing Addendum - 2019 - Final.txt', 'r').read()

# extract statements
statement_list = STATEMENT_RE.split(contract_text)

contract = {}
clauses = []
clause = {}
sub_clause = {}
sub_sub_clause = {}
idx = 0
sentence_id = 1

while idx < len(statement_list):
    statement = statement_list[idx]
    if CLAUSE_RE.match(statement):
        if sub_sub_clause:
            sub_clause['sub_clauses'].append(sub_sub_clause)
            sub_sub_clause = {}
        if sub_clause:
            clause['sub_clauses'].append(sub_clause)
            sub_clause = {}
        if clause:
            clauses.append(clause)

        title_list = statement.split('\t')
        clause = {
            'title_number': title_list[0],
            'title_text': title_list[1].strip(),
            'sentences': [],
            'sub_clauses': []
        }
    elif SUB_CLAUSE_RE.match(statement):
        if sub_sub_clause:
            sub_clause['sub_clauses'].append(sub_sub_clause)
            sub_sub_clause = {}
        if sub_clause:
            clause['sub_clauses'].append(sub_clause)

        title_list = statement.split('\t')
        sub_clause = {
            'title_number': title_list[0],
            'title_text': title_list[1].strip(),
            'sentences': [],
            'sub_clauses': []
        }
    elif SUB_SUB_CLAUSE_RE.match(statement):
        if sub_sub_clause:
            sub_clause['sub_clauses'].append(sub_sub_clause)

        title_list = statement.split('\t')
        sub_sub_clause = {
            'title_number': title_list[0],
            'title_text': title_list[1].strip(),
            'sentences': [],
            'sub_clauses': []
        }
    else:
        for sentence in SENTENCE_RE.split(statement):
            if not sentence:
                continue
            elif sub_sub_clause:
                sub_sub_clause['sentences'].append({
                    'id': sentence_id,
                    'text': sentence,
                    'type': 'regular',
                    'modality': None,
                    'symboleo_elements': {
                        'trigger': None,
                        'debtor': None,
                        'creditor': None,
                        'antecedent': None,
                        'consequent': None,
                        'asset': None
                    }
                })
            elif sub_clause:
                sub_clause['sentences'].append({
                    'id': sentence_id,
                    'text': sentence,
                    'type': 'regular',
                    'modality': None,
                    'symboleo_elements': {
                        'trigger': None,
                        'debtor': None,
                        'creditor': None,
                        'antecedent': None,
                        'consequent': None,
                        'asset': None
                    }
                })
            # ignore statements outside of clauses for now
            elif not clause:
                continue
            else:
                clause['sentences'].append({
                    'id': sentence_id,
                    'text': sentence,
                    'type': 'regular',
                    'modality': None,
                    'symboleo_elements': {
                        'trigger': None,
                        'debtor': None,
                        'creditor': None,
                        'antecedent': None,
                        'consequent': None,
                        'asset': None
                    }
                })
            sentence_id += 1
    idx += 1

if sub_sub_clause:
    sub_clause['sub_clauses'].append(sub_sub_clause)
if sub_clause:
    clause['sub_clauses'].append(sub_clause)
if clause:
    clauses.append(clause)

contract['clauses'] = clauses
open('../../data/processed/dpa_labeled_draft.json', 'w').write(json.dumps(contract))