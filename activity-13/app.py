from flask import Flask,render_template,request,redirect,session,send_file
from pymongo import MongoClient
import pickle
from fpdf import FPDF
import os

with open("ai.pkl","rb") as f:
    ai=pickle.load(f)
mongouri="mongodb+srv://22f01a0546:zNR0tlpj9u9AqBkf@cluster1.s4np6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client=MongoClient(mongouri)
print("DB Connected")

app=Flask(__name__) 
app.secret_key="ViK@S0"
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signupForm',methods=["POST"])
def signupForm():
    username=request.form["username"]
    password=request.form["password"]
    data={"username":username,
          "password":password
          }
    db=client["sacet"]
    collection=db["cse"]
    k=collection.find_one(data)
    print(k)

    if k is not None:
        print("account exist")
        return render_template("signup.html",err="account exist")
    else:
        collection.insert_one(data)
    return render_template("signup.html",msg="account created")
@app.route('/loginForm',methods=["POST"])
def loginForm():
    username=request.form["username"]
    password=request.form["password"]
    data={"username":username,
          "password":password
          }
    db=client["sacet"]
    collection=db["cse"]
    k=collection.find_one(data)
    print(k)
    if k is None:
        return render_template("login.html",err="Invalid Login")
    else:
        session["username"]=username
        return redirect("/dashboard")
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/predictAI', methods=['POST'])
def generate_resume():
    # Get form data
    name = request.form['n']
    email = request.form['p']
    mobile = request.form['k']
    linkedin = request.form['t']
    github = request.form['h']
    skills = request.form['ph']
    experiences = request.form['rainfall']

    # Generate PDF Resume
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Resume", ln=True, align='C')
    
    pdf.ln(10)  # Line break
    pdf.set_font('Arial', '', 12)

    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.cell(200, 10, f"Mobile: {mobile}", ln=True)
    pdf.cell(200, 10, f"LinkedIn: {linkedin}", ln=True)
    pdf.cell(200, 10, f"GitHub: {github}", ln=True)
    pdf.cell(200, 10, f"Skills: {skills}", ln=True)
    pdf.cell(200, 10, f"Experience: {experiences}", ln=True)

    # Save PDF
    resume_filename = f"{name}_resume.pdf"
    pdf.output(resume_filename)

    # Send the file back to the user for download
    return send_file(resume_filename, as_attachment=True)

if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=9000,
        debug=True
    )



    