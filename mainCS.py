from flask import Flask, request, render_template
import pickle
import pandas as pd

file1 = open('model.pkl', 'rb')
rf = pickle.load(file1)
file1.close()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def predict():
    prediction=''
    if request.method == 'POST':
        my_dict = request.form
        Month = int(my_dict['Month'])
        Month=Month-1
        Annual_Income = float(my_dict['Annual_Income'])
        Interest_Rate = int(my_dict['Interest_Rate'])
        Num_of_Loan = int(my_dict['Num_of_Loan'])
        Type_of_Loan = int(my_dict['Type_of_Loan'])
        Delay_from_due_date = int(my_dict['Delay_from_due_date'])
        Num_of_Delayed_Payment = int(my_dict['Num_of_Delayed_Payment'])
        Changed_Credit_Limit = float(my_dict['Changed_Credit_Limit'])
        Credit_Mix = my_dict['Credit_Mix']
        if Credit_Mix.lower() == 'standard':
            Credit_Mix = 0
        elif Credit_Mix.lower() == 'good':
            Credit_Mix = 1
        else:
            Credit_Mix = 2
        Outstanding_Debt = float(my_dict['Outstanding_Debt'])
        Credit_Utilization_Ratio = float(my_dict['Credit_Utilization_Ratio'])
        Credit_History_Age_inMonths = int(my_dict['Credit_History_Age_inMonths'])
        Total_EMI_per_month = float(my_dict['Total_EMI_per_month'])
        Amount_invested_monthly = float(my_dict['Amount_invested_monthly'])
        Monthly_Balance = float(my_dict['Monthly_Balance'])
        
        # Create DataFrame from input features
        input_data = pd.DataFrame({
            'Month': [Month],
            'Annual_Income': [Annual_Income],
            'Interest_Rate': [Interest_Rate],
            'Num_of_Loan': [Num_of_Loan],
            'Type_of_Loan': [Type_of_Loan],
            'Delay_from_due_date': [Delay_from_due_date],
            'Num_of_Delayed_Payment': [Num_of_Delayed_Payment],
            'Changed_Credit_Limit': [Changed_Credit_Limit],
            'Credit_Mix': [Credit_Mix],
            'Outstanding_Debt': [Outstanding_Debt],
            'Credit_Utilization_Ratio': [Credit_Utilization_Ratio],
            'Credit_History_Age_inMonths': [Credit_History_Age_inMonths],
            'Total_EMI_per_month': [Total_EMI_per_month],
            'Amount_invested_monthly': [Amount_invested_monthly],
            'Monthly_Balance': [Monthly_Balance]
        })
        
        prediction = rf.predict(input_data)[0]
        prediction=int(prediction)
        if(prediction==0):
            prediction='Good Credit Score'
        if(prediction==1):
            prediction='Standard Credit Score'
        if(prediction==2):
            prediction='Poor Credit Score'
        print(prediction)
    
        return render_template('result.html', prediction=prediction)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
