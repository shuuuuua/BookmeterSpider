#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime as dt

import urllib2
import json

BASE_URL = 'https://bookmeter.com'

class User:
    id = None
    name = None
    image_url = None
    user_home_url = None

    num_read = 0
    num_reading = 0
    num_stacked = 0
    num_wish = 0

    num_followees = 0
    num_follewers = 0

    """
    aaa
    """

    def __init__(self, id):
        self.id = str(id)

        self.user_home_url = BASE_URL + '/users/' + self.id + '/'
        f = urllib2.urlopen(self.user_home_url)
        html = f.read()
        bs = BeautifulSoup(html, "html.parser")

        self.name = bs.find('div', class_='userdata-side__name').text
        self.image_url = bs.find('figure', class_='userdata-side__avatar').find('img').attrs['src']

        userdata_navs = bs.find('ul', class_='userdata-nav').find_all('li')
        self.num_read = int(userdata_navs[0].find('span', class_='userdata-nav__count').text.replace(u'冊',''))
        self.num_readng = int(userdata_navs[1].find('span', class_='userdata-nav__count').text.replace(u'冊',''))
        self.num_stacked = int(userdata_navs[2].find('span', class_='userdata-nav__count').text.replace(u'冊',''))
        self.num_wish = int(userdata_navs[3].find('span', class_='userdata-nav__count').text.replace(u'冊',''))

        favorites = bs.find_all('div', class_='bm-block-side userdata')
        for favorite in favorites:
            if favorite.find('span', class_='bm-block-side__title__text').text == u'お気に入り':
                self.num_followees = int(favorite.find('span', class_='bm-block-side__title__num').text.replace(u'人',''))
            elif favorite.find('span', class_='bm-block-side__title__text').text == u'お気に入られ':
                self.num_followers = int(favorite.find('span', class_='bm-block-side__title__num').text.replace(u'人',''))

    def get_followees(self, is_all=True):
        url = self.user_home_url + 'followees'

        if is_all:
            followees = self._get_friends(url, self.num_followees)
        else:
            followees = self._get_friends(url, 20)

        return followees

    def get_followers(self, is_all=True):
        url = self.user_home_url + 'followers'

        if is_all:
            followers = self._get_friends(url, self.num_followers)
        else:
            followers = self._get_friends(url, 20)

        return followers

    def _get_friends(self, url, num):
        friends = []

        for i in range((num-1)/20 + 1):
            f = urllib2.urlopen(url + '?page=' + str(i+1))
            html = f.read()
            bs = BeautifulSoup(html, "html.parser")

            items = bs.find('ul', class_='relationships__list').find_all('li', class_='list__item')
            for item in items:
                user_id = item.find('div', class_='item__username').find('a').attrs['href'].replace('/users/','')
                friends.append(User(user_id))

        return friends

    def get_read_books(self, is_all=True):
        url = self.user_home_url + 'books/read'

        if is_all:
            books = self._get_books(url, self.num_read)
        else:
            books = self._get_books(url, 20)

        return books

    def get_reading_books(self, is_all=True):
        url = self.user_home_url + 'books/reading'

        if is_all:
            books = self._get_books(url, self.num_reading)
        else:
            books = self._get_books(url, 20)

        return books

    def get_stacked_books(self, is_all=True):
        url = self.user_home_url + 'books/stacked'

        if is_all:
            books = self._get_books(url, self.num_stacked)
        else:
            books = self._get_books(url, 20)

        return books

    def get_wish_books(self, is_all=True):
        url = self.user_home_url + 'books/wish'

        if is_all:
            books = self._get_books(url, self.num_wish)
        else:
            books = self._get_books(url, 20)

        return books

    def _get_books(self, url, num):
        books = []

        for i in range((num - 1)/20 + 1):
            f = urllib2.urlopen(url + '?page=' + str(i+1))
            html = f.read()
            bs = BeautifulSoup(html, "html.parser")

            items = bs.find('div', class_='books book-list book-list--grid').find_all('li', class_='group__book')
            for item in items:
                book_id = int(item.find('div', class_='detail__title').find('a').attrs['href'].replace('/books/',''))
                book = Book(book_id)
                book.read_at = item.find('div', class_='detail__date').text.replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
                book.user_id = self.id
                books.append(book)

        return books


class Book:
    id = None
    user_id = None
    title = None
    book_home_url = None
    read_at = None
    authors = []
    num_page = None
    num_pickup = None
    image_url = None
    amazon_url = None
    review = None

    def __init__(self, id):
        self.id = str(id)

        self.book_home_url = BASE_URL + '/books/' + self.id + '/'
        f = urllib2.urlopen(self.book_home_url)
        html = f.read()
        bs = BeautifulSoup(html, "html.parser")

        self.title = bs.find('header', class_='show__header').find('h1', class_='inner__title').text
        items = bs.find('header', class_='show__header').find('ul', class_='header__authors').find_all('li')
        for item in items:
            self.authors.append(item.find('a').text)

        self.image_url = bs.find('section', class_='sidebar__group') \
                           .find('div', class_='group__image').find('img').attrs['src']
        self.amazon_url = bs.find('section', class_='sidebar__group') \
                            .find('div', class_='detail__amazon').find('a').attrs['href']
        items = bs.find('section', class_='sidebar__group') \
                  .find_all('dd', class_='bm-details-side__item')

        self.num_pickup = int(items[0].find('span', class_='span bm-details-side__pickup').text)
        self.num_page = int(items[1].find('span').text)
