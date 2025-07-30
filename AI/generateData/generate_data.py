import pandas as pd
import numpy as np
import os

os.makedirs('data', exist_ok=True)

def generate_data(start_date='2015-01-01', end_date='2021-12-31'):
    date_range = pd.date_range(start=start_date, end=end_date)
    days = len(date_range)
    
    data = []
    for day in range(days):
        date = date_range[day]
        # Thu nhập ngẫu nhiên hàng ngày
        income = np.random.uniform(5, 20)  # Thu nhập hàng ngày thay vì chỉ ngày 1
        essential_need = np.random.uniform(5, 15)
        entertainment_need = np.random.uniform(1, 5)
        unexpected_expense = np.random.choice([0, np.random.uniform(0, 20)], p=[0.8, 0.2])
        # Nợ thay đổi ngẫu nhiên qua thời gian
        debt_balance = np.random.uniform(0, 200) if day == 0 else max(0, data[-1][5] - np.random.uniform(0, 10))  # Giảm nợ ngẫu nhiên
        investment_opportunity = np.random.uniform(0, 1)  # Giá trị liên tục thay vì nhị phân
        inflation_rate = np.random.uniform(0.01, 0.03)  # Biến động hàng ngày
        interest_rate = np.random.uniform(0.005, 0.015)  # Biến động hàng ngày
        data.append([
            date, income, essential_need, entertainment_need,
            unexpected_expense, debt_balance, investment_opportunity,
            inflation_rate, interest_rate
        ])
    
    df = pd.DataFrame(data, columns=[
        'date', 'income', 'essential_need', 'entertainment_need',
        'unexpected_expense', 'debt_balance', 'investment_opportunity',
        'inflation_rate', 'interest_rate'
    ])
    df.to_csv('data/synthetic_finance.csv', index=False)
    print("Generated richer synthetic_finance.csv from 2015 to 2021")

if __name__ == '__main__':
    generate_data()