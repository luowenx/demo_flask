from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)
import sqlite3 as sql


bp = Blueprint('book', __name__)

@bp.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('addbook.html')
    
    # try:
    #     book_name = request.form.get('book_name')
    #     author_name = request.form.get('author_name')
    #     intro = request.form.get('intro')
    #     created = request.form.get('created')

    #     with sql.connect() as con:
    # except:
    #     con.rollback()
    #              msg = "error in insert operation"

    # finally:
        