

import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime



jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  bio=ndb.StringProperty(required=False)
  college=ndb.StringProperty(required=False)
  fb=ndb.StringProperty(required=False)
  insta=ndb.StringProperty(required=False)
  twitter=ndb.StringProperty(required=False)
  linkedin=ndb.StringProperty(required=False)

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      email_address = user.nickname()
      cssi_user = CssiUser.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">Sign Out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if cssi_user:
        welcome_template = jinja_env.get_template('welcome.html')
        welcome= welcome_template.render({
        'firstname' : cssi_user.first_name,
        'lastname' : cssi_user.last_name ,
        'signout' : signout_link_html
        })
        self.response.write(welcome)
      # If the user hasn't been to our site, we ask them to sign up
      else:
        newuser_template = jinja_env.get_template('signup1.html')
        newuser = newuser_template.render({})
        self.response.write(newuser)

    else:
      signin_template= jinja_env.get_template('pleasesignup.html')
      signin = signin_template.render({'signin':  users.create_login_url('/') })
      self.response.write(signin)



  def post(self):
    user = users.get_current_user()
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    cssi_user = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        id=user.user_id())
    cssi_user.put()
    signup_template=jinja_env.get_template('signup.html')
    html= signup_template.render({
    'first_name' : cssi_user.first_name
    })
    self.response.write(html)


    # self.response.write('Thanks for signing up, %s!' %
    #     cssi_user.first_name)

class CreateProfileHandler(webapp2.RequestHandler):
    def get(self):
        profile_template= jinja_env.get_template('form-profile.html')
        html=profile_template.render({})
        self.response.write(html)
        webapp2.redirect('/profile')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        p_template=jinja_env.get_template('beta1.html')
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        cssi_user.bio= self.request.get('bio')
        cssi_user.college=self.request.get('college')
        cssi_user.fb=self.request.get('fb')
        cssi_user.insta=self.request.get('insta')
        cssi_user.twitter=self.request.get('twitter')
        cssi_user.linkedin = self.request.get('linkedin')
        cssi_user.put()
        html=p_template.render({
        'firstName':cssi_user.first_name ,
        'lastName': cssi_user.last_name,
        'college':cssi_user.college,
        'fb':cssi_user.fb,
        'insta':cssi_user.insta,
        'twitter':cssi_user.twitter,
        'linkedin': cssi_user.linkedin,
        'bio':cssi_user.bio
        })
        self.response.write(html)

class PostData(ndb.Model):
    email_address = ndb.StringProperty()
    text = ndb.StringProperty()
    time = ndb.DateProperty()

class PostHandler(webapp2.RequestHandler):
    def get (self):
        make_a_post_template=jinja_env.get_template('make-a-post.html')
        html= make_a_post_template.render({
        })
        self.response.write(html)
    def post(self):
        post_template= jinja_env.get_template("make-a-post.html")
        posts= post_template.render({})
        post_data = self.request.get("Post Box")
        user_email= self.request.get("email_address")
        time = datetime.now()
        post_box= PostData(email_address = user_email, text= post_data, time=time)


        # now= datetime.now()
        # print '%02d/%02d/%04d %02d:%02d:%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
        post_box.put()
        return webapp2.redirect("/listposts")

class PostData(ndb.Model):
    email_address = ndb.StringProperty(required=True)
    text = ndb.StringProperty(required = True)
    time = ndb.DateTimeProperty(required = True)

class ListPostsHandler(webapp2.RequestHandler):
    def get(self):
        all_posts_query = PostData.query()
        all_posts = all_posts_query.fetch()
        for post in all_posts:
            ctime = '%02d/%02d/%04d %02d:%02d:%02d' % (post.time.month, post.time.day, post.time.year, post.time.hour, post.time.minute, post.time.second)
            self.response.out.write(post.email_address + "     " + post.text + "     " + ctime)

            self.response.out.write('<br>')

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        mainpage_template= jinja_env.get_template('mainpage.html')
        mainpage=mainpage_template.render({})
        self.response.write(mainpage)

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/createprofile', CreateProfileHandler),
  ('/profile', ProfileHandler),
  ('/postbox', PostHandler),
  ('/listposts', ListPostsHandler),
  ('/main', MainPageHandler)

], debug=True)
