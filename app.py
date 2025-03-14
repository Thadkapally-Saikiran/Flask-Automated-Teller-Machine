from flask import Flask, render_template, request, redirect, url_for, session, flash  # Import necessary Flask components for web handling, template rendering, requests, redirection, session management, and flash messaging
import mysql.connector  # Import MySQL connector to interact with the MySQL database
import os  # Import OS module for interacting with the operating system (e.g., environment variables)
from decimal import Decimal  # Import Decimal for precise arithmetic with decimal numbers (important for monetary calculations)
from datetime import datetime  # Import datetime to work with date and time values

# Create a Flask web application instance
app = Flask(__name__)  # Initialize the Flask application
app.secret_key = "atmsecuritykey"  # Set a secret key for session management (used for securely signing the session cookie)

# Configure MySQL Connection
# Establish a connection to the MySQL database with credentials
# Note: Never expose credentials like password in real applications, use environment variables instead.
db = mysql.connector.connect(  # Create a connection object to the MySQL database
    host="localhost",  # Specify the host where the database server is located (localhost in this case)
    user="root",  # Specify the database username
    password="SaiKiran@2001",  # Specify the database password (should be kept secure)
    database="user_db"  # Specify the database name that stores the user data
)
cursor = db.cursor(dictionary=True)  # Create a cursor object to execute SQL queries; using dictionary=True to get results as dictionaries

# Helper function: get messages based on selected language
def get_messages():
    language = session.get("language", "1")  # Retrieve the current language from the session; default to "1" (English) if not set
    if language == "2":  # Check if the selected language is "2" (Hindi)
        msgs = {
           "welcome": "ATM में आपका स्वागत है",  # Hindi welcome message
           "enter_account": "अपना खाता नंबर दर्ज करें: ",  # Prompt to enter account number in Hindi
           "enter_pin": "अपना PIN दर्ज करें: ",  # Prompt to enter PIN in Hindi
           "login_success": "लॉगिन सफल",  # Message for successful login in Hindi
           "incorrect": "गलत खाता नंबर या PIN",  # Message for incorrect account number or PIN in Hindi
           "select_menu": "ATM मेन्यू",  # Label for ATM menu in Hindi
           "choice": "अपना विकल्प चुनें (1-5): ",  # Prompt for choosing a menu option in Hindi
           "balance": "वर्तमान शेष राशि: ₹",  # Label for showing current balance in Hindi
           "enter_deposit": "जमा राशि दर्ज करें: ",  # Prompt to enter deposit amount in Hindi
           "deposit_success": "सफलतापूर्वक जमा किया गया। नया शेष: ₹",  # Message for successful deposit in Hindi
           "enter_withdraw": "निकासी राशि दर्ज करें: ",  # Prompt to enter withdrawal amount in Hindi
           "withdraw_success": "सफलतापूर्वक निकासी किया गया। नया शेष: ₹",  # Message for successful withdrawal in Hindi
           "insufficient": "पर्याप्त शेष राशि नहीं है",  # Message for insufficient funds in Hindi
           "enter_pin_confirm": "लेन-देन की पुष्टि के लिए अपना PIN दर्ज करें: ",  # Prompt to confirm PIN for transaction in Hindi
           "invalid_pin": "अमान्य PIN. लेन-देन रद्द किया गया.",  # Message when PIN is invalid in Hindi
           "transaction_history": "लेन-देन इतिहास:",  # Label for transaction history in Hindi
           "no_transactions": "अभी तक कोई लेन-देन नहीं",  # Message when no transactions exist in Hindi
           "thank_you": "ATM का उपयोग करने के लिए धन्यवाद। आपका दिन शुभ हो!",  # Thank you message in Hindi
           "invalid_choice": "अमान्य विकल्प. कृपया मान्य विकल्प चुनें।",  # Message for invalid menu choice in Hindi
           "invalid_amount": "कृपया एक मान्य राशि दर्ज करें",  # Message for invalid amount input in Hindi
           "positive_amount": "कृपया एक सकारात्मक राशि दर्ज करें"  # Message for ensuring a positive amount in Hindi
        }
    else:  # Otherwise, default to English messages
        msgs = {
           "welcome": "Welcome to the ATM",  # English welcome message
           "enter_account": "Enter your account number: ",  # Prompt to enter account number in English
           "enter_pin": "Enter your PIN: ",  # Prompt to enter PIN in English
           "login_success": "Login Successful",  # Message for successful login in English
           "incorrect": "Incorrect account number or PIN",  # Message for incorrect credentials in English
           "select_menu": "ATM MENU",  # Label for ATM menu in English
           "choice": "Enter your choice (1-5): ",  # Prompt for choosing a menu option in English
           "balance": "Current Balance: ₹",  # Label for current balance in English
           "enter_deposit": "Enter amount to deposit: ",  # Prompt to enter deposit amount in English
           "deposit_success": "Deposit successful. New balance: ₹",  # Message for successful deposit in English
           "enter_withdraw": "Enter amount to withdraw: ",  # Prompt to enter withdrawal amount in English
           "withdraw_success": "Withdrawal successful. New balance: ₹",  # Message for successful withdrawal in English
           "insufficient": "Insufficient funds",  # Message for insufficient funds in English
           "enter_pin_confirm": "Enter your PIN to confirm the transaction: ",  # Prompt to confirm PIN for transaction in English
           "invalid_pin": "Invalid PIN. Transaction cancelled.",  # Message for invalid PIN in English
           "transaction_history": "Transaction History:",  # Label for transaction history in English
           "no_transactions": "No transactions yet",  # Message when no transactions exist in English
           "thank_you": "Thank you for using the ATM. Have a great day!",  # Thank you message in English
           "invalid_choice": "Invalid choice. Please select a valid option.",  # Message for invalid menu choice in English
           "invalid_amount": "Please enter a valid number",  # Message for invalid amount input in English
           "positive_amount": "Please enter a positive amount"  # Message for ensuring a positive amount in English
        }
    return msgs  # Return the messages dictionary based on the selected language

# -------------------- Route: Language Selection --------------------
@app.route("/", methods=["GET", "POST"])  # Define the root URL route; accepts GET and POST methods for language selection
def language_selection():
    if request.method == "POST":  # If the form is submitted via POST method
        language = request.form.get("language")  # Retrieve the selected language value from the submitted form
        session["language"] = language  # Store the selected language in the session
        return redirect(url_for("login"))  # Redirect the user to the login page after language selection
    return render_template("language_selection.html")  # Render the language selection HTML template for GET requests

# -------------------- Route: Login --------------------
@app.route("/login", methods=["GET", "POST"])  # Define the login route; accepts GET and POST methods
def login():
    msgs = get_messages()  # Retrieve localized messages based on the selected language
    if request.method == "POST":  # If the login form is submitted via POST
        account_number = request.form.get("account_number")  # Retrieve the account number entered by the user
        pin = request.form.get("pin")  # Retrieve the PIN entered by the user
        query = "SELECT * FROM atm_users WHERE account_number = %s"  # SQL query to fetch user details based on account number
        cursor.execute(query, (account_number,))  # Execute the SQL query with the provided account number
        user = cursor.fetchone()  # Fetch the first matching user record from the database
        if user and user["pin"] == pin:  # Check if the user exists and the provided PIN matches the stored PIN
            session["user"] = user["account_number"]  # Save the account number in session to maintain login state
            flash(msgs["login_success"], "success")  # Flash a success message (localized)
            return redirect(url_for("dashboard"))  # Redirect the user to the dashboard after successful login
        else:
            flash(msgs["incorrect"], "error")  # Flash an error message if login credentials are incorrect
            return redirect(url_for("login"))  # Redirect back to the login page for another attempt
    return render_template("login.html", msgs=msgs)  # Render the login HTML template, passing in the localized messages for GET requests

# -------------------- Route: Dashboard (ATM Menu) --------------------
@app.route("/dashboard")  # Define the dashboard route
def dashboard():
    if "user" not in session:  # Check if the user is not logged in (i.e., session does not contain a user)
        return redirect(url_for("login"))  # Redirect to the login page if not authenticated
    msgs = get_messages()  # Retrieve localized messages based on the session's language
    return render_template("dashboard.html", msgs=msgs)  # Render the dashboard HTML template, passing in the messages

# -------------------- Route: Check Balance --------------------
@app.route("/checkbalance")  # Define the route for checking account balance
def checkbalance():
    if "user" not in session:  # Verify if the user is logged in
        return redirect(url_for("login"))  # Redirect to login if the session is missing the user
    msgs = get_messages()  # Get localized messages
    account_number = session["user"]  # Retrieve the account number of the logged-in user from session
    query = "SELECT balance FROM atm_users WHERE account_number = %s"  # SQL query to get the user's balance
    cursor.execute(query, (account_number,))  # Execute the query with the account number
    user = cursor.fetchone()  # Fetch the user's data from the query result
    balance = user["balance"] if user else 0  # Extract the balance from the user record, defaulting to 0 if no user is found
    flash(msgs["balance"] + format(balance, ".2f"), "info")  # Flash an informational message displaying the formatted balance
    return redirect(url_for("dashboard"))  # Redirect back to the dashboard page

# -------------------- Route: Deposit (GET and POST) --------------------
@app.route("/deposit", methods=["GET", "POST"])  # Define the route for depositing money; supports GET (to display form) and POST (to process deposit)
def deposit():
    if "user" not in session:  # Check if the user is logged in
        return redirect(url_for("login"))  # Redirect to login if not authenticated
    msgs = get_messages()  # Retrieve localized messages
    if request.method == "POST":  # If the deposit form is submitted via POST
        deposit_amount = request.form.get("deposit_amount")  # Get the deposit amount from the form
        pin_confirm = request.form.get("pin_confirm")  # Get the PIN confirmation from the form
        account_number = session["user"]  # Retrieve the user's account number from session
        query = "SELECT * FROM atm_users WHERE account_number = %s"  # SQL query to fetch the user's details
        cursor.execute(query, (account_number,))  # Execute the query with the user's account number
        user = cursor.fetchone()  # Fetch the user's record from the database
        if user and user["pin"] == pin_confirm:  # Verify that the user exists and the PIN confirmation matches the stored PIN
            try:
                deposit_amount = Decimal(deposit_amount)  # Convert the deposit amount to a Decimal for precise arithmetic
                if deposit_amount > 0:  # Check that the deposit amount is positive
                    new_balance = user["balance"] + deposit_amount  # Calculate the new balance after deposit
                    update_query = "UPDATE atm_users SET balance = %s WHERE account_number = %s"  # SQL query to update the balance
                    cursor.execute(update_query, (new_balance, account_number))  # Execute the update with the new balance and account number
                    db.commit()  # Commit the balance update to the database
                    # Insert transaction record
                    txn_query = "INSERT INTO transactions (account_number, description, timestamp) VALUES (%s, %s, %s)"  # SQL query to log the transaction
                    description = f"Deposited ₹{deposit_amount:.2f}"  # Create a description for the transaction
                    timestamp = datetime.now()  # Capture the current date and time for the transaction
                    cursor.execute(txn_query, (account_number, description, timestamp))  # Execute the insert query to record the transaction
                    db.commit()  # Commit the transaction record insertion
                    flash(msgs["deposit_success"] + format(new_balance, ".2f"), "success")  # Flash a success message with the new balance
                else:
                    flash(msgs["positive_amount"], "error")  # Flash an error message if the deposit amount is not positive
            except ValueError:
                flash(msgs["invalid_amount"], "error")  # Flash an error message if the deposit amount conversion fails (invalid input)
        else:
            flash(msgs["invalid_pin"], "error")  # Flash an error message if the PIN confirmation is incorrect
        return redirect(url_for("dashboard"))  # Redirect back to the dashboard after processing the deposit
    return render_template("deposit.html", msgs=msgs)  # Render the deposit HTML template with localized messages for GET requests

# -------------------- Route: Withdraw (GET and POST) --------------------
@app.route("/withdraw", methods=["GET", "POST"])  # Define the route for withdrawing money; supports GET to display the form and POST to process the withdrawal
def withdraw():
    if "user" not in session:  # Check if the user is logged in
        return redirect(url_for("login"))  # Redirect to the login page if not authenticated
    msgs = get_messages()  # Retrieve localized messages
    if request.method == "POST":  # If the withdrawal form is submitted via POST
        withdraw_amount = request.form.get("withdraw_amount")  # Retrieve the withdrawal amount from the form
        pin_confirm = request.form.get("pin_confirm")  # Retrieve the PIN confirmation from the form
        account_number = session["user"]  # Get the user's account number from session
        query = "SELECT * FROM atm_users WHERE account_number = %s"  # SQL query to fetch user details
        cursor.execute(query, (account_number,))  # Execute the query using the account number
        user = cursor.fetchone()  # Fetch the user's record from the database
        if user and user["pin"] == pin_confirm:  # Verify that the user exists and the provided PIN confirmation is correct
            try:
                withdraw_amount = Decimal(withdraw_amount)  # Convert the withdrawal amount to a Decimal for precise arithmetic
                if withdraw_amount <= 0:  # Check if the withdrawal amount is non-positive
                    flash(msgs["positive_amount"], "error")  # Flash an error message for non-positive withdrawal amount
                elif withdraw_amount > user["balance"]:  # Check if the withdrawal amount exceeds the current balance
                    flash(msgs["insufficient"], "error")  # Flash an error message for insufficient funds
                else:
                    new_balance = user["balance"] - withdraw_amount  # Calculate the new balance after withdrawal
                    update_query = "UPDATE atm_users SET balance = %s WHERE account_number = %s"  # SQL query to update the user's balance
                    cursor.execute(update_query, (new_balance, account_number))  # Execute the update query with the new balance
                    db.commit()  # Commit the balance update to the database
                    # Insert transaction record
                    txn_query = "INSERT INTO transactions (account_number, description, timestamp) VALUES (%s, %s, %s)"  # SQL query to log the withdrawal transaction
                    description = f"Withdrawn ₹{withdraw_amount:.2f}"  # Create a description for the withdrawal transaction
                    timestamp = datetime.now()  # Capture the current timestamp for the transaction
                    cursor.execute(txn_query, (account_number, description, timestamp))  # Execute the insert query to record the transaction
                    db.commit()  # Commit the transaction record insertion
                    flash(msgs["withdraw_success"] + format(new_balance, ".2f"), "success")  # Flash a success message with the new balance
            except ValueError:
                flash(msgs["invalid_amount"], "error")  # Flash an error message if the withdrawal amount conversion fails (invalid input)
        else:
            flash(msgs["invalid_pin"], "error")  # Flash an error message if PIN confirmation fails
        return redirect(url_for("dashboard"))  # Redirect back to the dashboard after processing the withdrawal
    return render_template("withdraw.html", msgs=msgs)  # Render the withdrawal HTML template with localized messages for GET requests

# -------------------- Route: View Transaction History (GET and POST) --------------------
@app.route("/viewhistory", methods=["GET", "POST"])  # Define the route for viewing transaction history; supports GET (to show PIN confirmation form) and POST (to display transactions)
def viewhistory():
    if "user" not in session:  # Check if the user is not logged in
        return redirect(url_for("login"))  # Redirect to the login page if not authenticated
    msgs = get_messages()  # Retrieve localized messages
    account_number = session["user"]  # Get the account number of the logged-in user from session
    if request.method == "POST":  # If the form is submitted via POST (to confirm PIN)
        pin_confirm = request.form.get("pin_confirm")  # Retrieve the PIN confirmation from the form
        query = "SELECT * FROM atm_users WHERE account_number = %s"  # SQL query to fetch the user's details
        cursor.execute(query, (account_number,))  # Execute the query using the account number
        user = cursor.fetchone()  # Fetch the user's record from the database
        if user and user["pin"] == pin_confirm:  # Verify the user's existence and correct PIN confirmation
            txn_query = "SELECT description, timestamp FROM transactions WHERE account_number = %s ORDER BY timestamp DESC"  # SQL query to retrieve transaction history in descending order by timestamp
            cursor.execute(txn_query, (account_number,))  # Execute the query with the account number
            transactions = cursor.fetchall()  # Fetch all transaction records for the user
            return render_template("view_history.html", msgs=msgs, transactions=transactions)  # Render the transaction history template with the retrieved transactions
        else:
            flash(msgs["invalid_pin"], "error")  # Flash an error message if the PIN is invalid
            return redirect(url_for("dashboard"))  # Redirect to the dashboard if PIN confirmation fails
    # GET method: show form for PIN confirmation
    return render_template("view_history.html", msgs=msgs, transactions=None)  # Render the view history template with no transactions to prompt for PIN confirmation

# -------------------- Route: Logout --------------------
@app.route("/logout")  # Define the route for logging out
def logout():
    session.clear()  # Clear the session to log the user out
    flash("Logged out successfully.", "info")  # Flash an informational message indicating successful logout
    return redirect(url_for("login"))  # Redirect the user back to the login page

if __name__ == "__main__":  # Check if this script is run directly (and not imported as a module)
    app.run(debug=True)  # Run the Flask development server in debug mode (provides detailed error messages)
