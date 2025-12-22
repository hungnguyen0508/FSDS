import pandas as pd 
import random
from datetime import datetime, timedelta 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# set random seed and number of rows in each table
random.seed(42)
num_users = 100 
num_accounts = 150
num_transactions = 3000
num_loans = 80
num_payments = 200


# Function to create 5 tables 
def table_create():
    # create user tables
    users = []
    for i in range(1, num_users + 1): 
        users.append({
            "user_id": i, 
            "full_name": f"User {i}",
            "date_of_birth": f"{random.randint(1960,2000)}-{random.randint(1,12)}-{random.randint(1,31)}", 
            "gender": random.choice(["M","F"]),
            "employment_status": random.choice(["salaried","employed","unemployed","SALARIED","EMPLOYED","UNUMEPLOYED"]),
            "monthly_income" : np.random.choice([random.randint(8000000,30000000), None, random.randint(-7000000,-2100000)],p = [0.8,0.1,0.1]),
            "created_at": datetime.now()- timedelta(days = 365) - timedelta(days = random.randint(1,365))
            
        })
    df_users = pd.DataFrame(users)
    df_users.to_csv("df_user.csv", index = False)

    # accounts
    accounts = []
    for i in range(1, num_accounts + 1):
        user_id = random.choice([random.randint(1, num_users), 9999]) # orphan user
        accounts.append({
            "account_id": i,
            "user_id": user_id,  
            "account_type": random.choice(["checking", "savings", "CHECKING"]),
            "balance": np.random.choice([
                random.randint(0, 10000000),
                random.randint(-2100000,-1000000)],
                p = [0.9, 0.1]  # invalid balance
            ), 
            "opened_at": f"{datetime.now()- timedelta(days = 365) + timedelta(days = random.randint(1,50))} days from user created"
        })
    df_accounts = pd.DataFrame(accounts)
    df_accounts.to_csv("df_accounts.csv", index = False)

    # loans
    loans = []
    for i in range(1, num_loans + 1):
        loans.append({
            "loan_id": i,
            "user_id": random.choice([random.randint(1, num_users), 7777]),  # orphan
            "loan_amount": random.choice([
                random.randint(5000000, 100000000),
                -20000000  # invalid
            ]),
            "interest_rate": random.choice([10.5, 12.0, -3.0]),  # invalid rate
            "loan_term_months": random.choice([12, 24, 36, None]),
            "start_date": datetime.now() - timedelta(days=random.randint(300, 365)),
            "loan_status": random.choice(
                ["active", "closed", "default", "actve"]  # typo
            )
        })
    df_loans = pd.DataFrame(loans)
    df_loans.to_csv("df_loans.csv", index = False)
    # transactions table 
    transactions = []
    for i in range(1, num_transactions + 1):
        t_type = random.choice(["debit", "credit", "debt"])  # invalid enum
        amount = random.randint(10000, 5_000000)

        # Wrong sign logic
        if t_type == "debit":
            amount = random.choice([amount, -amount])
        elif t_type == "credit":
            amount = random.choice([-amount, amount])

        transactions.append({
            "transaction_id": random.choice([i, i]),  # duplicate IDs
            "account_id": random.randint(1, num_accounts),
            "user_id": random.choice([random.randint(1, num_users), 8888]),  # orphan
            "amount": amount,
            "transaction_type": t_type,
            "category": random.choice(
                ["groceries", "salary", "rent", "transfer", None]
            ),
            "transaction_time": datetime.now() - timedelta(days = 365)+ timedelta(days = random.randint(51,365))
        })

    df_transactions = pd.DataFrame(transactions)
    df_transactions.to_csv("transactions.csv", index=False)
    payments = []
    for i in range(1, num_payments + 1):
        start_offset = random.randint(50, 250)  # payment before loan start
        payments.append({
            "payment_id": i,
            "loan_id": random.choice([random.randint(1, num_loans), 6666]),  # orphan
            "payment_date": datetime.now() - timedelta(days=start_offset),
            "amount_paid": random.choice([
                random.randint(500000, 5000000),
                -1000000  # invalid
            ]),
            "payment_status": random.choice(
                ["on_time", "late", "ONTIME"]  # bad enum
            )
        })

    df_payments = pd.DataFrame(payments)
    df_payments.to_csv("loan_payments.csv", index=False)

if __name__ == "__main__": 
    table_create()