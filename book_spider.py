#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Kim on 2017/9/25

import requests
import random
import re

from book import Book
from bs4 import BeautifulSoup as bs
from urllib.parse import quote # url编码
from openpyxl import Workbook

header = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'},
          {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3'},
          {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'}]

def douban_book_spider(book_tag, page=2):
    '''豆瓣读书爬虫，根据标签进行爬取'''

    book_list = []

    # while True:
    for current_page in range(page):
        try:
            url = 'https://book.douban.com/tag/'+ quote(book_tag) + '?start=' + str(current_page * 20) # 豆瓣书单每页显示20本书
            response = requests.get(url, headers=random.choice(header))
        except requests.exceptions.RequestException as e:
            print(e)
            # continue

        soup = bs(response.text, 'html.parser')
        books = soup.find_all('li', class_='subject-item')
        if books == None:
            return None
        for book in books:
            book_info = book.find('div', class_='info')

            pic = book.find('img', width='90').get('src').strip()  # 书本的封面
            name = book_info.select('h2 a:nth-of-type(1)')[0].get('title').strip() # 书名

            desc = book_info.find('div', class_='pub').text.split('/')
            *author, press, pub_time, price = desc
            author = [a.strip() for a in author]
            rating = book_info.find('span', class_='rating_nums').text
            rating_num = book_info.find('span', class_='pl').text.strip()
            rating_num = re.sub(r'\D', '', rating_num)

            book = Book(pic, name, author, press, pub_time, price, rating, rating_num)
            book_list.append(book)
    return book_list

def write_to_excel_file(book_tag, book_dict):
    '''将查找到的书本写入excel文件'''

    if book_dict == None or len(book_dict) == 0:
        print('没有找到相对应标签的书籍')
        return

    wb = Workbook()
    for tag in book_tag:
        ws = wb.create_sheet(title=tag)
        ws.append(['书名', '作者/译者', '出版社', '出版时间', '价格', '评分/评分人数', '封面'])
        list = book_dict[tag]
        if list == None or len(list) == 0:
            continue
        for book in list:
            ws.append([book.name, book.author, book.press, book.time, book.price, book.rating + '/' + book.rating_num,
                       book.pic])
    wb.save('book_list.xlsx')

def get_books(book_tags):
    results = {}
    for tag in book_tags:
        book_list = douban_book_spider(tag)
        results[tag] = book_list
    return results

if __name__ == '__main__':
    tag = ['小说', '音乐', '历史']
    write_to_excel_file(tag, get_books(tag))

