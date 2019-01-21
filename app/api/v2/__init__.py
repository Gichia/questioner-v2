"""Initialize blueprint fro version2 of api"""
from flask import Blueprint

ver2 = Blueprint('ver2', __name__, url_prefix="/api/v2")