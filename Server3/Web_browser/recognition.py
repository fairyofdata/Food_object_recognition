import os
from app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests

import pymysql
from pymysql.cursors import DictCursor

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
def upload_form():
	return render_template('home.html')
 
@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('오늘의 도마')
		return render_template('home.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
  
@app.route('/recognition/', methods=['POST'])
def send_image_to_yolo():
  filename = request.form['filename']
  response = requests.post("http://localhost:5002/yolov5x-recipe/", files={"image": open(app.config['UPLOAD_FOLDER'] + filename, 'rb').read()}).json()
  ingredients_en = list(set([x['name'] for x in response if x['name']]))
  print(ingredients_en)
  convert_ingredients_dict = {'carrot':'당근', 'egg':'달걀', 'potato':'감자', 'onion':'양파', 'squid':'오징어', 'chicken':'닭다리살'}
  ingredients = list(map(lambda x: convert_ingredients_dict[x], ingredients_en))
  flash('식재료 인식 완료')
  return render_template('home.html', filename=filename, ingredients=ingredients)

@app.route('/ingrecome', methods=['POST'])
def ingrecome():
  filename = request.form['filename']
  ingredients = request.form['ingredients']
  userid = request.form["userid"]
  conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8", cursorclass=DictCursor)
  cursor = conn.cursor()
  sql = f"SELECT * FROM user_db WHERE userid = '{userid}'"
  cursor.execute(sql)  
  user_ingredient_infos = cursor.fetchall()
  user_ingredient_info = user_ingredient_infos[0]
  basic_ingredients, allergy = user_ingredient_info['basic_ingredients'], user_ingredient_info['allergy']
  ingredients = list(ingredients[:-2].split(sep=", "))
  basic_ingredients = basic_ingredients.split(sep=", ")
  allergy = allergy.split(sep=", ")
  flash('저장된 식재료 불러오기')
  return render_template('home.html', filename=filename, ingredients=ingredients, basic_ingredients=basic_ingredients, allergy=allergy, userid=userid)

