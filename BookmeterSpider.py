from bs4 import BeautifulSoup

import requests
import json

class BookmeterSpider:
  LOGIN_PAGE_URL = 'https://bookmeter.com/login'

  session = None
  """
  aaa
  """

  def __init__(self, user_id, password):
    self.session = requests.Session()
    payload = {
      'session[email_address]': user_id,
      'session[password]': password
    }

    r = self.session.get(self.LOGIN_PAGE_URL)
    bs_login_page = BeautifulSoup(r.text)
    auth_token = bs_login_page.find(attrs={'name': 'authenticity_token'}).get('value')
    payload['authenticity_token'] = auth_token

    r = self.session.post(self.LOGIN_PAGE_URL, data=payload)
    bs_home_page = BeautifulSoup(r.text)
    user_content = bs_home_page.find(attrs={'name':'current_user'}).get('content')

    j = json.loads(user_content)
    print j['user']['id']

  def get_reading_books(self):
    pass

  def get_read_books(self):
    pass

  def get_want_books(self):
    pass

  def get_stacked_books(self):
    pass
