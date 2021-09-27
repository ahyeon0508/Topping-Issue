from flask import Flask, request, render_template

app=Flask(__name__)

@app.route("/")
def hello_world():
	return "Hello World!"

@app.route("/index")
def indexhtml():
    return render_template("index template")

if __name__ == '__main__':
    app.run()