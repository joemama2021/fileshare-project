from flask import Flask, render_template, request
import io
from flask import send_file
import boto3


app = Flask(__name__)

##boto3 init
s3 = boto3.client('s3')
# A temporary list of users (to be replaced with a database)
users = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]


# Home route
@app.route('/')
def index():
    return render_template('index.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                
                
                ##setup session


                return "Login successful! Redirect to file management page."
        
        return "Invalid username or password. Please try again."

    return render_template('login.html')

#File upload
@app.route('/upload', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                s3.upload.fileobj(file, 'fileshare-project', file.filename)
                return "File Uploaded Successfully!"
            except Exception as e:
                return f"An error occured: {e}"
    return render_template('upload.html')


#FIle download
@app.route('/download/<filename>')
def download_file(filename):
    try:
        obj = s3.get_object(Bucket='fileshare-project', Key = filename)
        file_content = obj['Body'].read()
        return send_file(io.BytesIO(file_content), as_attachment=True, attachment_filename=filename)
    except Exception as e:
        return f"Error occured: {e}"  


#Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform user registration logic here
        # with proper error handling and security measures

        return "Registration successful! You can now login."
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
