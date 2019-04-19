from flask import Flask, redirect

app = Flask(__name__)
new_url = 'http://dorm.kinsaurralde.com'

@app.route('/')
def root():
	return redirect(new_url, code=302)

if __name__== '__main__':
	app.run(host='0.0.0.0', port=5000)
