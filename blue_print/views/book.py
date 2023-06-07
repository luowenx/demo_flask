from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)
from datetime import datetime
from .. import db
from .auth import auth
from dbutils.pooled_db import PooledDB

bp = Blueprint('book', __name__)


def query_db(query, args=(), one=False):
    cur = db.get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@bp.route('/add', methods=['GET', 'POST'])
@auth
def add():
    if request.method == 'GET':
        return render_template('addbook.html')
    try:
        book_name = request.form.get('book_name')
        author_name = request.form.get('author_name')
        intro = request.form.get('intro')
        # created = request.form.get('created')
        datetime_str = request.form.get('created')
        datetime_obj = datetime.fromisoformat(datetime_str)
        created = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        author_id = 1988

        # 1、写sql 语句
        query = 'INSERT INTO book (author_id, author_name, created, name, intro) VALUES(?, ?, ?, ?, ?)'
        # 2、获取数据库连接
        conection = db.get_db()
        # 3、获取游标，执行sql
        args = [author_id, author_name, created, book_name, intro]
        cursor = conection.execute(query, args)
        # 对数据库有改动，commit提交，不然不生效
        conection = conection.commit()
        # result = query_db(query,[author_id, author_name, created, book_name, intro], one=False)
        # 关闭连接
        cursor.close()
        msg = "您成功添加一本书。"
        assert cursor.rowcount == 1, "添加失败，添加过程出错了。"
    except Exception as e:
        msg = "添加失败，添加过程出错了：" + str(e)
        return render_template('result.html', msg=msg)
    else:
        return render_template('result.html', msg=msg)


@bp.route('/book', methods=['GET', 'POST', 'DELETE', 'PUT'])
@auth
def book():
    if request.method == 'GET':
        id = request.args.get('id')
        query = "SELECT * FROM book WHERE id = ?"
        book = query_db(query, [id], one=True)
        print(book['created'])
        result = {k: book[k] for k in book.keys()}
        return result
    elif request.method == 'DELETE':
        id = request.args.get('id')
        query = "DELETE FROM book WHERE id = ?"
        try:
            conection = db.get_db()
            args = [id]
            cursor = conection.execute(query, args)
            conection.commit()
            cursor.close()
            msg = '您成功删除了一条数据。'
            assert cursor.rowcount == 1, '删除失败'
        except Exception as e:
            msg = "添加失败，添加过程出错了：" + str(e)
            return render_template('result.html', msg=msg)
        else:
            return render_template('result.html', msg=msg)
    return '1'


@bp.route('/editing/<int:id>', methods=['GET', 'POST'])
@auth
def editing(id):
    if request.method == 'GET':
        query = "SELECT * FROM book WHERE id = ?"
        book = query_db(query, [id], one=True)
        book = {k: book[k] for k in book.keys()}
        print(book)
        return render_template('editing.html', book=book)

    try:
        book_name = request.form.get('book_name')
        author_name = request.form.get('author_name')
        intro = request.form.get('intro')
        datetime_str = request.form.get('created')
        datetime_obj = datetime.fromisoformat(datetime_str)
        created = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

        query = 'UPDATE book SET author_name = ?, created = ?, name = ?, intro = ? WHERE id = ?'
        # 2、获取数据库连接
        conection = db.get_db()
        # 3、获取游标，执行sql
        args = [author_name, created, book_name, intro, id]
        cursor = conection.execute(query, args)
        # 对数据库有改动，commit提交，不然不生效
        conection = conection.commit()
        # 关闭连接
        cursor.close()

        msg = "成功编辑了一本书"
        assert cursor.rowcount == 1, "保存失败，添加过程出错了。"
    except Exception as e:
        msg = "保存失败，保存过程出错了：" + str(e)
        return render_template('result.html', msg=msg)
    else:
        return render_template('result.html', msg=msg)
