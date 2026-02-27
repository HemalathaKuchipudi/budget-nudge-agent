def calculate_monthly_limit(salary, expenses, emi):
    disposable = salary - expenses - emi
    return max(int(disposable * 0.4), 0)