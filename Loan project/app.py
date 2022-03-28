from flask import Flask, request, render_template
from loandb import User, Loans, session, get_user_id
from loanClasses import loan_creator, saved_loans

app = Flask(__name__)

user_chooser = False  

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        username = request.form['username']
        global user_chooser
        try:
            add_user = User(name = username)
            session.add(add_user)
            session.commit()
            user_chooser = username
        except:
            session.rollback()
            user_chooser = username   
        return render_template("menu.html", username=username)
    else:
        return render_template('home.html')


@app.route('/loan', methods=['POST', 'GET'])
def new_loan():    
    if request.method == "POST":
        amount = request.form['loan_amount']
        interest = request.form['interest_rate']
        term = request.form['term']
        name = request.form['name']
        new_loan = loan_creator(int(amount), int(interest), int(term), name)
        new_loan.save_monthly_payments()
        saved_loans.append(new_loan)
        table = new_loan.get_loan_table()
        chart = new_loan.draw_plots()
        l_name, l_amount, l_interest, l_term = new_loan.get_info()
        user_id = get_user_id(user_chooser)
        add_loan = Loans(name=l_name, amount=l_amount, interest=l_interest, term=l_term, user_id=user_id)
        session.add(add_loan)
        session.commit()
        return render_template('selected_loan.html',
                               loan_name=l_name,
                               loan_amount = l_amount,
                               loan_interest = l_interest,
                               loan_term = l_term,
                               table=[table.to_html(classes='data')],
                               titles=table.columns.values,
                               chart=chart)
    button_value = 'Calculate'
    return render_template('new_loan.html', button_value=button_value)


@app.route('/loan_list')
def loan_list():    
    return render_template('loan_list.html', loans=saved_loans)


@app.route('/selected_loan')
def selected_loan():
    for loan in saved_loans:
        if loan == '{{i}}':
            return render_template('selected_loan.html', selected_loan=loan)


@app.route('/update_loan', methods=['POST', 'GET'])
def update_loan():    
    if request.method == "POST":
        amount = request.form['loan_amount']
        interest = request.form['interest_rate']
        term = request.form['term']
        name = request.form['name']
        new_loan = loan_creator(int(amount), int(interest), int(term), name)
        new_loan.save_monthly_payments()
        saved_loans.append(new_loan)
        table = new_loan.get_loan_table()
        chart = new_loan.draw_plots()
        return render_template('selected_loan.html', selected_loan=new_loan, table=[table.to_html(classes='data')], titles=table.columns.values, chart=chart)
    button_value = 'Update'
    return render_template('new_loan.html', button_value=button_value)

        
if __name__ == "__main__":
    app.run(debug=True) 
    