from flask import Blueprint, render_template, request, jsonify
from common.utility import data_process
import time
import os

other = Blueprint('other', __name__)


@other.route('/data')
def data_analysis():
    '''
    从前端传进来csv文件的路径，返回可视化图需要的参数
    :return:
    '''
    return render_template('doubandata.html')


@other.route('/data-upload')
def fileUpload():
    file_data = request.files.get('file_data')
    if not file_data:
        return "请上传文件"

    df = data_process(file_data)
