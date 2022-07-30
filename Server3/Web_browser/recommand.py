from app import app
from flask import Flask, flash, request, redirect, url_for, render_template, session
import requests
import threading

from datetime import datetime
import pymysql

from tkinter import *
import random


def user_info_gen(userid):
	return {
	    "userid": userid,
	    "latitude": 37.56667000000000,
	    "longitude":  126.97806000000000,
		"timestamp": datetime.now().timestamp()
  	}

class User:
	def __init__(self, user):
		self.user = user

class Recipes:
	def __init__(self, prep_recipes, lack_recipes):
		self.prep_recipes = prep_recipes
		self.lack_recipes = lack_recipes

def recipe_token(res):
    recipe_dic={}
    for rep_recipe in res["rep_df"]:
        recipe_dic[rep_recipe["_source.recipe_nm"]] = rep_recipe
    prep_recipes = list(map(lambda x : recipe_dic[x], res["frec_prep_recipe"]))
    lack_recipes = list(map(lambda x : recipe_dic[x], res["frec_lack_recipe"]))
    return prep_recipes, lack_recipes

@app.route('/recipe_req/', methods=['POST'])
def request_recipe():
	userid = request.form['userid']
	filename = request.form['filename']
	ingredients = request.form['ingredients']
	essential_ingredients = request.form['essential_ingredients']
	basic_ingredients = request.form['basic_ingredients']
	allergy = request.form['allergy']
	user_ingredients_data = {"ingredients":ingredients.split(sep="\r\n"), 
	                         "essential_ingredients":essential_ingredients.split(sep="\r\n"),
	                         "basic_ingredients":basic_ingredients.split(sep="\r\n"),
	                         "allergy":allergy.split(sep="\r\n"),
	                         }
	user_gen_info = user_info_gen(userid)
	global user_info
	user_info=User(user_gen_info)
	request_data = dict(user_info.user, **user_ingredients_data)
	res = requests.post("http://localhost:5003/recipe_req/", json=request_data).json()
 
	prep_recipes, lack_recipes = recipe_token(res)
	global recipes
	recipes = Recipes(prep_recipes, lack_recipes)

	flash('추천 레시피')
	return render_template('recipe.html', prep_recipes=prep_recipes, lack_recipes=lack_recipes)

conn = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")
cursor = conn.cursor()
@app.route('/send_tomysql/', methods = ['GET', 'POST'])
def send_tomysql():
    url = request.url
    recipe_url = url[url.find("?")+1:url.find("&")].replace('%2F', '/')
    recipe_code = url[url.find("&")+1:]
    sql = "INSERT INTO user_select_db(userid, recipe_code, timestamp, latitude, longitude) VALUES (%s, %s, %s, %s, %s)"
    userdata = [user_info.user["userid"], recipe_code, datetime.now(), user_info.user["latitude"], user_info.user["longitude"]]
    cursor.execute(sql, userdata)   
    conn.commit()   
    return redirect(recipe_url)

@app.route('/ex_req/<ex_recipe_code>', methods=['POST'])
def ex_req(ex_recipe_code):
    user_ingredients_data = {"ex_recipe_code":ex_recipe_code}
    request_data = dict(user_info.user, **user_ingredients_data)
    res_ex = requests.post("http://localhost:5004/ex_req/", json=request_data).json()
    flash(res_ex["massge"])
    return render_template('recipe.html', prep_recipes=recipes.prep_recipes, lack_recipes=recipes.lack_recipes, ex=True)

@app.route('/ex_res/', methods=['GET', 'POST'])
def webhook():
    def auto(match):
        ex_match = Tk()
        label = Label(ex_match, text = match)
        label.pack()
        ex_match.mainloop()
    if request.method == 'GET':
        match = request.args.to_dict()
    elif request.method == 'POST':
        if request.is_json is True: 
            match = request.get_json()
        else: 
            match = request.form.to_dict()
    thread = threading.Thread(target=auto, kwargs={'match': match})
    thread.start()
    return "Done"

