from flask import Flask, render_template, request, flash
import os

#Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '46d1ce3b317f4d2ce1d08512694d27b6'


#Home Page of Web App
@app.route("/", methods=["POST","GET"])
@app.route("/home", methods=["POST","GET"])
def home():
    return render_template('home.html')


#route for manually entering sequences
@app.route("/enter_sequence", methods=["POST","GET"])
def enter_sequence():
    flash("Please enter sequence:")
    return render_template("enter_sequence.html")


#route for uploading sequences as plain text file
@app.route("/upload_file", methods=["POST","GET"])
def upload_file():
    return render_template("upload_file.html")


#Display output of manually entered sequence
@app.route("/enter_sequence_output", methods=["POST","GET"])
def enter_sequence_output():
    flash("Input sequence:\n"+str(request.form['sequence_input']))
    output = revComp(str(request.form['sequence_input']))
    if output == "error":
        flash("Error: input sequence contains non-DNA characters")
    else:
        flash("Reverse complement sequence:\n"+output)
    flash("Enter another sequence:")
    return render_template("enter_sequence.html")


#Display output of file-uploaded sequence
@app.route("/upload_file_output", methods=["POST","GET"])
def upload_file_output():
    file = request.files["file"]
    if file.filename[-4:]!='.txt':
        flash("Error: No files or wrong file type uploaded")
        return render_template("upload_file.html")
    else:

        input=file.read().decode('utf-8')
        flash("Input sequence:\n"+input)
        output = revComp(input)
        if output == "error":
            flash("Error: Input sequence contains non-DNA characters")
        else:
            flash("Reverse complement sequence:\n"+output)
        return render_template("upload_file.html")


#Algorithm for calculating reverse complement of DNA sequence
def revComp(str):
    out = ''
    for i in str:
        if i == 'A':
            out='T'+out
        elif i == 'a':
            out='t'+out
        elif i == 'T':
            out='A'+out
        elif i == 't':
            out='a'+out
        elif i == 'C':
            out='G'+out
        elif i == 'c':
            out='g'+out
        elif i == 'G':
            out='C'+out
        elif i == 'g':
            out='c'+out
        elif i == ' ': #allow spaces
            pass
        else:
            return 'error'
    return out


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
