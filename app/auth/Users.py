__author__ = "Manuel Escriche <mev@tid.es>"

import base64, requests
from flask_login import UserMixin
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from kconfig import settings

class User(UserMixin):
    __data__ = dict()

    def __init__(self, uid, displayName, accessKey, jSession):
        self.id = uid
        self.displayName = displayName
        self.accessKey = accessKey
        self.jSession = jSession
        User.__data__[uid] = dict(uid=uid,
                                  displayName=displayName,
                                  accessKey=accessKey,
                                  jSession=jSession)
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.displayName)

    @staticmethod
    def get(userid):
        return User(**User.__data__[userid])

class LoginForm(Form):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    url = 'https://{}/rest/auth/latest/session'.format(settings.server['JIRA'].domain)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self._access_key = None
        self._displayName = None
        self._active = False
        self._jsession = None

    def validate(self):
        rv = Form.validate(self)
        if not rv: return False

        user = self.username.data
        _auth = '{}:{}'.format(self.username.data, self.password.data)
        #print(_auth)
        keyword = base64.b64encode(bytes(_auth,'utf-8'))
        #print(keyword)
        self._access_key = str(keyword)[2:-1]
        #print(self._access_key)
        headers = {'Content-Type': 'application/json', "Authorization": "Basic {}".format(self._access_key)}
        #print(LoginForm.url)
        #print(headers)
        req_session = requests.session()
        try:
            answer = req_session.get(LoginForm.url, headers=headers, verify=False)
        except:
            raise Exception
        #print(headers)
        #print('answer - status=', answer.status_code)
        if answer.status_code != 200:
            return False
        data = dict(answer.json())
        answer2 = req_session.get(data['self'])
        data2 = dict(answer2.json())

        self._jsession = req_session
        self._displayName = data2['displayName']
        self._active = data2['active']
        self.user = user
        return True

    def get_user(self):
        return User(self.user, self._displayName, self._access_key, self._jsession)

if __name__ == "__main__":
    pass