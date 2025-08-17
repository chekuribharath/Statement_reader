from flask import Flask, render_template, render_template_string, request

import json
from collections import defaultdict
from datetime import datetime
import os

app = Flask(__name__)


# Use absolute path for JSON file
JSON_PATH = os.path.join(os.path.dirname(__file__), 'spending_trends', 'json_files', 'JsonFile.json')

def load_transactions():
    with open(JSON_PATH) as f:
        data = json.load(f)
    return data['transaction_details']

def summarize_trends(transactions):
    monthly_debits = defaultdict(float)
    monthly_credits = defaultdict(float)
    for t in transactions:
        date = datetime.strptime(t['tran_date'], '%d-%m-%Y')
        month = date.strftime('%Y-%m')
        debit = float(t['debit']) if t['debit'] else 0.0
        credit = float(t['credit']) if t['credit'] else 0.0
        monthly_debits[month] += debit
        monthly_credits[month] += credit
    return monthly_debits, monthly_credits

def get_unique_particulars(transactions):
    return sorted(set(t['particulars'] for t in transactions))


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return None

@app.route('/')
def index():
    transactions = load_transactions()
    transaction_type = request.args.get('transaction_type', '')
    # Filter transactions for particulars list based on transaction type
    if transaction_type == 'credit':
        particulars_source = [t for t in transactions if not t['debit'] or t['debit'] == '' or t['debit'] is None]
    elif transaction_type == 'debit':
        particulars_source = [t for t in transactions if t['debit'] and t['debit'] != '' and t['debit'] is not None]
    else:
        particulars_source = transactions
    particulars_list = get_unique_particulars(particulars_source)

    selected_particular = request.args.get('particulars', '')
    from_date_str = request.args.get('from_date', '')
    to_date_str = request.args.get('to_date', '')
    from_date = parse_date(from_date_str)
    to_date = parse_date(to_date_str)

    filtered = transactions
    if transaction_type == 'credit':
        filtered = [t for t in filtered if not t['debit'] or t['debit'] == '' or t['debit'] is None]
    elif transaction_type == 'debit':
        filtered = [t for t in filtered if t['debit'] and t['debit'] != '' and t['debit'] is not None]
    if selected_particular:
        filtered = [t for t in filtered if t['particulars'] == selected_particular]
    if from_date or to_date:
        temp = []
        for t in filtered:
            t_date = datetime.strptime(t['tran_date'], '%d-%m-%Y')
            if from_date and t_date < from_date:
                continue
            if to_date and t_date > to_date:
                continue
            temp.append(t)
        filtered = temp

    debits, credits = summarize_trends(filtered)
    months = sorted(set(list(debits.keys()) + list(credits.keys())))
    debit_values = [debits[m] for m in months]
    credit_values = [credits[m] for m in months]
    return render_template(
        'index.html',
        months=months,
        debits=debit_values,
        credits=credit_values,
        particulars_list=particulars_list,
        selected_particular=selected_particular,
        transaction_type=transaction_type,
        from_date_str=from_date_str,
        to_date_str=to_date_str
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
