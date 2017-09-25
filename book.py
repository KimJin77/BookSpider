#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Kim on 2017/9/25

class Book():
    '''豆瓣书本类'''

    '''
    初始化
    
    :type pic 封面图片
    :type name 书名
    :type author 作者/译者
    :type press 出版社
    :type time 出版时间
    :type price 价格
    :type rating 分数
    :type rating_num 评价人数
    '''
    def __init__(self, pic, name, author, press, time, price, rating, rating_num):
        self.pic = pic
        self.name = name
        if len(author) == 1:
            self.author = author[0]
        else:
            self.author = author[0] + '/' + author[1]
        self.press = press
        self.time = time
        self.price = price
        self.rating = rating
        self.rating_num = rating_num