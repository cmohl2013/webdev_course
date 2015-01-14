import os
import webapp2
import jinja2
from math import fmod
from google.appengine.ext import db

#jinja_env = jinja2.Environment(loader=jinja2.PackageLoader('templateapp', 'templates'))
            


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


#jinja_env.filters['fmod'] = fmod
# render template here


def putData(title, content):
    post = Blogpost(title=title, content=content)
    post.put()
    return post         



class Blogpost(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)



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

class BlogFrontpageHandler(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC ")

        self.render('blog.html', posts = posts)

class PostHandler(Handler):
    def get(self, post_id):
        #posts = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC ")
        post = Blogpost.get_by_id(int(post_id))
        #post = posts.get_by_id(post_id)
        self.render('single_post.html', post=post)
        #pass
class NewpostHandler(Handler):
    def get(self):
        self.render('new_post.html')    

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')
        error = ''
        if not title:
            error = 'give a title'
        if not content:
            error = 'provide a content'    
        if not content and not title:
            error = 'provide content and title'
        if error != '':    
            self.render('new_post.html', error = error, title = title, content = content)    

        else:
            post = putData(title, content)
            self.redirect('/blog/' + str(post.key().id()))    
  
            
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzbuzzHandler),
    ('/blog', BlogFrontpageHandler),
    ('/blog/newpost', NewpostHandler),
    ('/blog/(\d+)', PostHandler)
    
], debug=True)  