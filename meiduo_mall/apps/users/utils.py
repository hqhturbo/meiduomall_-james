"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :utils.py
# @Date     :2021/11/10 17:12
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meiduo_mall import settings
import logging

logger = logging.getLogger('django')

def generic_email_verify_token(user_id):
    '''生成邮件验证'''
    # 创建实例
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=60 * 30)
    # 加密数据
    data = s.dumps({'user_id':user_id})
    # 返回数据
    return data.decode()

def check_verify_token(token):
    '''解析邮件验证token'''
    # 创建实例
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=60 * 30)
    # 解密数据--可能有异常
    try:
        result = s.loads(token)
    except Exception as e:
        logger.error(f'解析邮件验证token出错.{e}')
        return None
    # 获取数据
    # result = {'user_id':user_id}
    return result.get('user_id')