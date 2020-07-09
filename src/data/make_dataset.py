import re
import json

STATEMENT_RE = r'\n+ ?\t*'
SENTENCE_RE = r'(?<![0-9])[.!?]\s+|[.!?]?\s*\n+'
CLAUSE_RE = r'\d+\.\s+.*'
SUB_CLAUSE_RE = r'\d+\.\d+\s+.*'
SUB_SUB_CLAUSE_RE = r'\d+\.\d+\.\d+\s+.*'

contract_text = open('../../data/contracts/DPA Data Processing Addendum - 2019 - Final.txt', 'r').read()

# extract statements
statement_list = re.split(STATEMENT_RE, contract_text)

contract = {}
clauses = []
clause = {}
sub_clause = {}
sub_sub_clause = {}
idx = 0
sentence_id = 1

while idx < len(statement_list):
    statement = statement_list[idx]
    if re.match(CLAUSE_RE, statement):
        if sub_sub_clause:
            sub_clause['sub_clauses'].append(sub_sub_clause)
            sub_sub_clause = {}
        if sub_clause:
            clause['sub_clauses'].append(sub_clause)
            sub_clause = {}
        if clause:
            clauses.append(clause)
        clause = {}
        clause['title'] = statement
        clause['sentences'] = []
        clause['sub_clauses'] = []
    elif re.match(SUB_CLAUSE_RE, statement):
        if sub_sub_clause:
            sub_clause['sub_clauses'].append(sub_sub_clause)
            sub_sub_clause = {}
        if sub_clause:
            clause['sub_clauses'].append(sub_clause)
        sub_clause = {}
        sub_clause['title'] = statement
        sub_clause['sentences'] = []
        sub_clause['sub_clauses'] = []
    elif re.match(SUB_SUB_CLAUSE_RE, statement):
        if sub_sub_clause:
            sub_clause['sub_clauses'].append(sub_sub_clause)
        sub_sub_clause = {}
        sub_sub_clause['title'] = statement
        sub_sub_clause['sentences'] = []
        sub_sub_clause['sub_clauses'] = []
    else:
        for sentence in re.split(SENTENCE_RE, statement):
            if not sentence:
                continue
            elif sub_sub_clause:
                sub_sub_clause['sentences'].append({
                    'id': sentence_id,
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
            elif sub_clause:
                sub_clause['sentences'].append({
                    'id': sentence_id,
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
            # ignore statements outside of clauses for now
            elif not clause:
                continue
            else:
                clause['sentences'].append({
                    'id': sentence_id,
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