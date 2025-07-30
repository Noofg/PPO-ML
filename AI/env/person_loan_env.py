import gym
from gym import spaces
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

class PersonalLoanEnv(gym.Env):
    def __init__(self, csv_path):
        super(PersonalLoanEnv, self).__init__()

        # Load và xử lý dữ liệu
        self.df = pd.read_csv(csv_path)
        self.original_df = self.df.copy()

        # Các cột định danh và số
        self.categorical_cols = [
            'EmploymentStatus', 'EducationLevel', 'MaritalStatus',
            'HomeOwnershipStatus', 'LoanPurpose', 'UtilityBillsPaymentHistory'
        ]
        self.numerical_cols = [
            'Age', 'AnnualIncome', 'CreditScore', 'Experience', 'LoanAmount',
            'LoanDuration', 'NumberOfDependents', 'MonthlyDebtPayments',
            'CreditCardUtilizationRate', 'NumberOfOpenCreditLines',
            'NumberOfCreditInquiries', 'DebtToIncomeRatio', 'LengthOfCreditHistory',
            'SavingsAccountBalance', 'CheckingAccountBalance', 'TotalAssets',
            'TotalLiabilities', 'MonthlyIncome', 'JobTenure', 'NetWorth',
            'BaseInterestRate', 'InterestRate', 'MonthlyLoanPayment',
            'TotalDebtToIncomeRatio', 'RiskScore'
        ]
        self.target_col = 'LoanApproved'

        # Encode dữ liệu
        for col in self.categorical_cols:
            self.df[col] = LabelEncoder().fit_transform(self.df[col].astype(str))

        self.features = self.numerical_cols + self.categorical_cols
        self.scaler = StandardScaler()
        self.df[self.features] = self.scaler.fit_transform(self.df[self.features])

        self.data = self.df[self.features].values
        self.labels = self.df[self.target_col].values

        self.current_index = 0
        self.total_steps = len(self.df)

        # Định nghĩa không gian
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(len(self.features),), dtype=np.float32)
        self.action_space = spaces.Discrete(2)  # 0: từ chối, 1: chấp nhận

    def reset(self):
        self.current_index = 0
        return self.data[self.current_index]

    def step(self, action):
        done = False
        info = {}

        actual = self.labels[self.current_index]

        # Tính reward: đúng thì +1, sai thì -1
        reward = 1 if action == actual else -1

        self.current_index += 1
        if self.current_index >= self.total_steps:
            done = True
            obs = np.zeros_like(self.data[0])
        else:
            obs = self.data[self.current_index]

        return obs, reward, done, info
if __name__ == "__main__":
    try:
        env = PersonalLoanEnv('data/dataset.csv')
        print("Khởi tạo môi trường thành công!")
        obs = env.reset()
        print("Observation:", obs)
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print("Step result:", obs, reward, done, info)
    except Exception as e:
        print("Lỗi:", e)