
import functools

from flask import (
    session, redirect, url_for
)


def auth(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not session.get('username'):
            return redirect('/sigin/login')
        return func(*args, **kwargs)
    return inner
