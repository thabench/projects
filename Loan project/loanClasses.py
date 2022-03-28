from loandb import get_loans
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

saved_loans = [] #will be changerd to db

class Loan():
    def __init__(self, amount, interest, period):
        self.__amount = amount
        self.__interest = interest
        self.__period = period
        self.__name = None
        
    def __repr__(self):
        return f'|Loan named {self.__name}|   Amount: {self.__amount}|   Interest rate: {self.__interest}|   Term in months: {self.__period}'
        
    
    def get_info(self):
        return self.__name, self.__amount, self.__interest, self.__period
   
    
    def set_name(self, new_name):
        self.__name = new_name
        return self.__name
    
    
    def save_monthly_payments(self):
        amount = self.__amount
        month = 1
        file_name = (f'loan_{self.__name}_A{self.__amount}_P{self.__interest}.csv')
        with open(file_name, 'w', encoding="UTF-8", newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['Month', 'Stable Monthly Payment', 'Loan Balance', 'Monthly Interest', 'Monthly Payment'])
            while amount > 0:
                stable_payment = round(self.__amount / self.__period, 2)
                if amount < stable_payment:
                    stable_payment = amount
                    monthly_interest = round((loan_balance + stable_payment) * (self.__interest/100) / 12, 2)
                    payment = round(monthly_interest + amount, 2)
                    csv_writer.writerow([month, stable_payment, loan_balance, monthly_interest, payment])
                    break    
                loan_balance = round(amount - stable_payment, 2)
                monthly_interest = round((loan_balance + stable_payment) * (self.__interest/100) / 12, 2)
                payment = round(stable_payment + monthly_interest, 2)
                csv_writer.writerow([month, stable_payment, loan_balance, monthly_interest, payment])
                month +=1
                amount = loan_balance
                
    
    def get_loan_table(self):
        loan_file = (f'loan_{self.__name}_A{self.__amount}_P{self.__interest}.csv')
        table = pd.read_csv(loan_file, header=0)
        loan_data = table.values
        return table
        
    
    def draw_plots(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax = sns.set(style='darkgrid')
        data = self.get_loan_table()
        sns.pairplot(data, kind='reg',
            x_vars=['Stable Monthly Payment','Loan Balance', 'Monthly Interest', 'Monthly Payment'],
            y_vars=['Month'])
        canvas=FigureCanvas(fig)
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return fig
        
        
        
            

def loan_creator(amount, interest, term, name = None):    
    loan = Loan(amount, interest, term)
    loan.set_name(name)
    return loan

# loan_creator(1000, 10, 10, "Tomas").save_monthly_payments()


# print(loan1.get_info())


# print(type(loan_creator(1000, 10, 10, "Vardas").get_loan_table()))

# print(loan_creator(1000, 10, 10, "Vardas").draw_plots())       
