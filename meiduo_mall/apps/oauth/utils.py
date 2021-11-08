"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :utils.py
# @Date     :2021/11/5 22:19
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""
from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

def generate_access_token(openid):
    '''
    签名openid
    :param openid:
    :return:
    '''
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    data = {'openid':openid}
    token = serializer.dumps(data)
    return token.decode()

def check_access_token(access_token):
    """
    提取openid
    :param access_token:
    :return:
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        return data.get('openid')