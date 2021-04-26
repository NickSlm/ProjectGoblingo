# external imports
from flask import Flask, session, request, redirect, url_for
from flask import render_template,flash
from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask_table import Table, Col
import sqlite3
import requests
# internal imports
from db import server_names, find_realm_id, find_item_id, get_items, get_total_quantity,get_items_by_type, get_mount_list_info
from blizzardAPI import Blizzard


# constant variables
BLIZZARD_CLIENT_ID = "6eef8ac48dbc417197ed8a34c731e398"
BLIZZARD_CLIENT_SECRET = "mxzBzxKXxQZsYU3ogGjPhoodi9O6VVmQ"
ITEM_CLASS_DICT = {"Weapons":"Weapon", "Armor":"Armor", "Containers":"Container", "Gems":"Gem","Item Enhancements":"Item Enhancement",
"Consumables":"Consumable","Glyphs":"Glyph", "Trade Goods":"Tradeskill","Recipes":"Recipe","Battle Pets":"Battle Pets","Quest Items":"Quest",
"Miscellaneous":"Miscellaneous","WoW Token":"WoW Token"}

app =  Flask(__name__)
app.secret_key = 'test'

def get_offset(mount_list, offset=0, per_page=60):
    return mount_list[offset: offset + per_page]

@app.route('/', methods=['GET'])
def home():
    session['server_list'] = server_names()
    return render_template('home.html')


@app.route('/login')
def login():
    return redirect(f"https://eu.battle.net/oauth/authorize?"
                    f"client_id={BLIZZARD_CLIENT_ID}&"
                    f"scope=wow.profile&"
                    f"redirect_uri=http://127.0.0.1:5000/authorized&"
                    f"response_type=code")


@app.route('/authorized')
def authorized():
    code = request.args.get("code")
    res = requests.post("https://eu.battle.net/oauth/token", data={
        "client_id": BLIZZARD_CLIENT_ID,
        "client_secret": BLIZZARD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": "http://127.0.0.1:5000/authorized",
        "scope": "wow.profile",
        "code": code})
    response = res.json()
    session['access_token'] = response['access_token']
    get_user_info = requests.get(f"https://eu.battle.net/oauth/userinfo?access_token={session['access_token']}")
    user_info = get_user_info.json()
    session['battletag'] = user_info['battletag']
    session['account_id'] = user_info['id']
    return redirect(url_for('home'))


@app.route('/logout')
def logout(): 
    session.pop('access_token', None)
    session.pop('battletag', None)
    session.pop('account_id', None)
    return redirect(url_for('home'))


@app.route('/auction-house', methods=["POST", "GET"])
def auction_house():
    # realms list
    realm_list = server_names()
    # connection to realms auction data
    if request.method == 'POST' and "realm_name" in request.form:
        session['server'] = request.form.get('realm_name')
    # display auction item data
    if request.method == 'POST' and "item_name" in request.form:
        session['item_name'] = request.form['item_name']
        filter_list = request.form.getlist('my_checkbox')
        if not session['item_name'] and not filter_list:
            flash("Please insert an item")
        elif session['item_name'] and filter_list:
            pass
        elif session['item_name'] and not filter_list:
            connection = Blizzard(connected_realm=find_realm_id(session['server']))
            auction_data = connection.get_data(connected_realm=find_realm_id(session['server']))
            item_dict = get_items(session['item_name'], auction_data)
            if not item_dict:
                flash("No such item exists")
            item_total = get_total_quantity(item_dict)
            return render_template('auction.html',realm_list=realm_list,item_class=ITEM_CLASS_DICT, item_dict=item_dict, item_total=item_total)
        else:
            connection = Blizzard(connected_realm=find_realm_id(session['server']))
            auction_data = connection.get_data(connected_realm=find_realm_id(session['server']))
            item_dict = get_items_by_type(filter_list, auction_data)
            if not item_dict:
                flash("No such item exists")
            item_total = get_total_quantity(item_dict)
            return render_template('auction.html', realm_list=realm_list, item_class=ITEM_CLASS_DICT, item_dict=item_dict, item_total=item_total)
    return render_template('auction.html', realm_list=realm_list, item_class=ITEM_CLASS_DICT)


@app.route('/statistics', methods=["POST", "GET"])
def statistics():
    return render_template('statistics.html')


@app.route('/profile', methods=["POST", "GET"])
def profile():
    return render_template('profile.html')


@app.route('/profile/characters', methods=["POST", "GET"])
def profile_characters():
    test_dict = {}
    connection = Blizzard()
    data = connection.get_character_list(profile_token=session['access_token'])
    for server in data:     # TODO: DELETE
        test_dict.update({server: len(data[server])})
    return render_template('profile_characters.html', char_list=data, char_server= test_dict)


@app.route('/profile/mounts', methods=["POST", "GET"])
def profile_mounts():
    mount_data, total_mounts = get_mount_list_info(profile_token=session['access_token'])
    total = len(mount_data)
    return render_template('profile_mounts.html',mounts=mount_data, total_mounts=total_mounts, total=total)

@app.route('/profile/pets', methods=["POST", "GET"])
def profile_pets():
    return render_template('profile_pets.html')


if __name__ == '__main__':
    app.run()