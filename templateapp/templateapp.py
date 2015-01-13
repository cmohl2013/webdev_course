import os
import webapp2
import jinja2
from math import fmod
#jinja_env = jinja2.Environment(loader=jinja2.PackageLoader('templateapp', 'templates'))
            


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


#jinja_env.filters['fmod'] = fmod
# render template here



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        #template = env.get_template('basicsignup.html')
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))        


class MainPage(Handler):
    def get(self):
        
        items = self.request.get_all('food')
        self.render('shopping_list.html', items = items)
        #self.write(output)

class FizzbuzzHandler(Handler):
    def get(self):
        
        n = self.request.get('n')

        try:
            n = int(n)
        except:
            n=0    
        #template = env.get_template('fizzbuzz.html')
        self.render('fizzbuzz.html', n=n)
        print n
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzbuzzHandler)
    
], debug=True)  