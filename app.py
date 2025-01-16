from flask import Flask, request, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

# Check if the Excel file exists, if not create it with a sample admin user
def initialize_user_file():
    user_file = 'users.xlsx'
    if not os.path.exists(user_file):
        df = pd.DataFrame({
            'Admin': ['admin'],
            'Password': ['admin123']
        })
        df.to_excel(user_file, index=False)

initialize_user_file()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    admin = request.form['admin']
    password = request.form['password']

    # Load user credentials from Excel
    user_file = 'users.xlsx'
    df = pd.read_excel(user_file)

    # Validate credentials
    user = df[(df['Admin'] == admin) & (df['Password'] == password)]

    if not user.empty:
        return render_template('home.html')
    else:
        return render_template('error.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return "No files uploaded", 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Placeholder for transformation logic
    # df1, df2 = transform_data(df1, df2)

    output_file1 = 'output_file1.xlsx'
    output_file2 = 'output_file2.xlsx'

    df1.to_excel(output_file1, index=False)
    df2.to_excel(output_file2, index=False)

    return render_template('download.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
