

from flask import Flask,flash,jsonify
from flask import request,redirect,url_for
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurant/<int:restaurant_id>',methods=['GET','POST'])
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/json')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify([i.serialize for i in menuItems] )


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json')
def restaurantMenuSpecificJSON(restaurant_id,menu_id):
    menuItem = session.query(MenuItem).filter(MenuItem.id==menu_id,MenuItem.restaurant_id
    ==restaurant_id).one()
    return jsonify(menuItem.serialize)


@app.route('/restaurant/<int:restaurant_id>/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method =='POST':
        newItem = MenuItem(name=request.form.get('name'),restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newMenu.html',restaurant_id=restaurant_id)
    



@app.route('/restaurant/edit/<int:restaurant_id>/<int:menu_id>',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        if request.form['newName']:
            editedItem.name = request.form['newName']
        session.add(editedItem)
        session.commit()
        flash(" menu item edited")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenu.html',restaurant_id=restaurant_id,menu_id=
        menu_id,item=editedItem)
    

@app.route('/restaurant/delete/<int:restaurant_id>/<int:menu_id>',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        if deletedItem:
            session.delete(deletedItem)
            session.commit()
            flash(" menu item edited")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenu.html',restaurant_id=restaurant_id,menu_id=menu_id,
        item=deletedItem)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)


