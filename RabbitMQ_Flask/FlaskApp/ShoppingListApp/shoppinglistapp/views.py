from datetime import datetime

import sqlalchemy.exc
from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import current_user, login_required
from flask_restful import Api
from wtforms import FieldList, FormField

from ShoppingListApp.shoppinglistapp.models import ShoppingListModel, ItemModel
from ShoppingListApp.shoppinglistapp.forms import AddShoppingListForm, AddItemForm
from .serializers import ShortShoppingListSchema
from ShoppingListApp.shoppinglistapp.helpers import load_previous_data_to_add_shopping_list
from .resources import ModifyShoppingListResource, basket_market_object

site_views = Blueprint("site_views",
                       __name__,
                       template_folder='templates')

shopping_list_api = Api(site_views)
shopping_list_api.add_resource(ModifyShoppingListResource, "/modify_add_shopping_list")
shopping_list_serializer = ShortShoppingListSchema()


@site_views.route("/")
def home():
    paginator = []
    if current_user.is_authenticated:
        page_number = request.args.get('page', 1, type=int)
        paginator = ShoppingListModel.get_paginator(current_user.get_id(), page_number)
    return render_template("shoppinglistapp/home.html", title="Home Page", paginator=paginator)


@site_views.route("/add", methods=["POST", "GET"])
@login_required
def add_shopping_list():
    num_items = request.args.get('items', default=0, type=int)
    AddShoppingListForm.items = FieldList(FormField(AddItemForm), min_entries=num_items)

    form = AddShoppingListForm()
    form = load_previous_data_to_add_shopping_list(form)

    if form.validate_on_submit():
        list_obj = ShoppingListModel()
        list_obj.name = form.name.data
        list_obj.status = "created"
        list_obj.user_id = current_user.get_id()

        items = []
        for item in form.items:
            item_obj = ItemModel()
            item_obj.name = item.item_name.data
            item_obj.price = float(item.price.data)
            item_obj.shop = str(item.shop.data)
            items.append(item_obj)
        list_obj.items = items
        try:
            list_obj.save_to_db()
        except sqlalchemy.exc.IntegrityError:
            flash("In every shopping list items must have unique name", 'danger')
            return render_template("shoppinglistapp/add_shopping_list.html",
                                   title="Add Shopping List", form=AddShoppingListForm())
        else:
            print("serializer for shopping list => ", shopping_list_serializer.dump(list_obj))
            # TODO: send this 'shopping_list_serializer.dump(list_obj)' to the RabbitMQ

            flash("New shopping list is saved.", 'info')
            return redirect(url_for("site_views.home"))

    return render_template("shoppinglistapp/add_shopping_list.html", title="Add Shopping List", form=form)


@site_views.route("/details/<list_id>")
@login_required
def detail_shopping_list(list_id):
    the_list = ShoppingListModel.find_by_id(list_id)
    if the_list is None:
        abort(404)
    elif the_list.user != current_user:
        abort(403)

    the_list.created = datetime.strftime(the_list.created, "%Y-%m-%d %H:%M")
    if the_list.updated:
        the_list.updated = datetime.strftime(the_list.updated, "%Y-%m-%d %H:%M")
    return render_template("shoppinglistapp/detail_shopping_list.html",
                           title="Detail Shopping List",
                           the_list=the_list)


@site_views.route("/delete/<list_id>", methods=["POST"])
@login_required
def delete_shopping_list(list_id):
    the_list = ShoppingListModel.find_by_id(list_id)
    if the_list and the_list.user != current_user:
        abort(403)

    the_list.delete_from_db()

    # TODO: here I should start publishing serialized shopping list to RabbitMQ, with indication of delete
    # basket_market_object.reset()
    # basket_market_object.set_user_id(current_user.get_id())
    # basket_market_object.process()
    the_list.status = "deleted"
    # TODO: send this to RabbitMQ 'shopping_list_serializer.dump(the_list)'
    print("serializing deleted list => ", shopping_list_serializer.dump(the_list))

    flash(f"Deleted '{the_list.name}' successfully.", "info")
    return redirect(url_for("site_views.home"))


@site_views.route("/frequent-itemsets")
@login_required
def get_frequent_item_sets():
    if not current_user.is_authenticated:
        abort(401)
    basket_market_object.fit_model()
    freq_item_sets = basket_market_object.frequent_item_sets
    return render_template("shoppinglistapp/frequent_item_sets.html",
                           title="Frequently Bought Items",
                           freq_item_sets=freq_item_sets)


@site_views.route("/patterns")
@login_required
def get_rules():
    if not current_user.is_authenticated:
        abort(401)
    basket_market_object.fit_model()
    rules = basket_market_object.rules
    return render_template("shoppinglistapp/rules.html",
                           title="Shopping List Patterns",
                           rules=rules)
