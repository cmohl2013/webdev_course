import cgi
import webapp2
import re
from jinja2 import Environment, PackageLoader

abc = 'abcdefghijklmnopqrstuvwxyz'



def isValidInput(username, regex):
    USER_RE = re.compile(regex)
    if USER_RE.match(username):
        return True
    return False    

def isValidUsername(username):
    return isValidInput(username, "^[a-zA-Z0-9_-]{3,20}$")

def isValidPw(pw):
    return isValidInput(pw,  "^.{3,20}$")

def isValidEmail(email):
    if email == '':
        return True
    return isValidInput(email,  "^[\S]+@[\S]+\.[\S]+$")    


def isValidSignup(username, pw, verify, email):
    if isValidUsername(username) and isValidPw(pw) and (pw == verify) and isValidEmail(email):
        return True
    return False    

def calcIndex(idx):
    if idx >= 26:
        return idx-26
    return idx
    
def shiftLetter(letter):

    if letter.lower() not in abc:
        return letter 
    if letter.isupper():
        letter = letter.lower()
        return abc[calcIndex(abc.find(letter)+13)].upper()      
    return abc[calcIndex(abc.find(letter)+13)]

def shiftSent(sent):
    out = ''
    for letter in sent:
        out = out + shiftLetter(letter)
    return cgi.escape(out)          


def renderForm(text=''):

    form = '''
    <html><head>
        <title>Unit 2 Rot 13</title>
      </head>

      <body>
        <h2>Enter some text to ROT13:</h2>
        <form method="post">
          <textarea name="text" style="height: 100px; width: 400px;">%s</textarea>
          <br>
          <input type="submit">
        </form>
      

    </body></html>
    ''' % text
    return form

class Rotation(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(renderForm())
    def post(self):
        rotated = shiftSent(self.request.get('text'))
        self.response.write(renderForm(text=rotated))    


class BasicInputHandler(webapp2.RequestHandler):
    def get(self):
        env = Environment(loader=PackageLoader('shiftapp', 'templates'))
        template = env.get_template('basicsignup.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(\
            username = ''\
            , pw = ''\
            ,verify = ''\
            ,email = ''\
            , username_errormsg=''\
            , pw_errormsg=''\
            , pw_verify_errormsg=''\
            , email_errormsg=''
            ))
    def post(self):
        username = self.request.get('username')    
        pw = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if isValidSignup(username, pw, verify, email):
            self.redirect('/unit2/welcome?username=' + username)
        else:
            username_errormsg = ''
            email_errormsg = ''
            pw_verify_errormsg = ''
            pw_errormsg = ''

            if not isValidUsername(username):
                username_errormsg = "That's not a valid username."
            if not isValidEmail(email):
                email_errormsg = "That's not a valid email."
            if pw != verify:
                pw_verify_errormsg = "Your passwords didn't match."
            if not isValidPw(pw):
                pw_errormsg = "That wasn't a valid password."       
                    
            env = Environment(loader=PackageLoader('shiftapp', 'templates'))
            template = env.get_template('basicsignup.html')

            self.response.write(template.render(\
            username = username\
            , pw = pw\
            ,verify = verify\
            ,email = email\
            , username_errormsg=username_errormsg\
            , pw_errormsg=pw_errormsg\
            , pw_verify_errormsg=pw_verify_errormsg\
            , email_errormsg=email_errormsg
            ))
                    

class SignupSuccessHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome, ' + self.request.get('username'))
# class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         q = self.request.get('q')
#         #self.response.out.write(self.request)
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write(self.request)

application = webapp2.WSGIApplication([
    ('/unit2/rot13', Rotation),
    ('/unit2/basicinput', BasicInputHandler),
    ('/unit2/welcome', SignupSuccessHandler)
], debug=True)  