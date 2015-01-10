import cgi
import webapp2

abc = 'abcdefghijklmnopqrstuvwxyz'

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




form = '''
<html><head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text" style="height: 100px; width: 400px;"></textarea>
      <br>
      <input type="submit">
    </form>
  

</body></html>
'''

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(form)


# class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         q = self.request.get('q')
#         #self.response.out.write(self.request)
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write(self.request)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    
], debug=True)	