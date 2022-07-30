from app import app
from flask import redirect, render_template, request, url_for

import recognition
import recommand

@app.route('/', methods=['GET','POST'])
def home():
	return render_template('home.html')

recognition
recommand

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5001, debug=True)
