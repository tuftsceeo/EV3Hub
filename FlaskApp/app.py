from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/ev3')
def ev3():
	return render_template('ev3.html')

@app.route('/more')
def more():
	return render_template('more.html')

if __name__ == '__main__':
	app.run(debug=True)
