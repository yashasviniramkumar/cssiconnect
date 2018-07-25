

import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb



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
      self.response.write('''
        <div style="color:blue">Please log in to use our site! </div> <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))



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
        p_template=jinja_env.get_template('profilepage.html')
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
        'linkedin': cssi_user.linkedin
        })
        self.response.write(html)

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/createprofile', CreateProfileHandler),
  ('/profile', ProfileHandler)
        })
        self.response.write(html)








class PostHandler(webapp2.RequestHandler):
    def post(self):
        post_data = self.request.get("Post Box")
        user_email= self.request.get("email_address")
        post_box= PostData(email_address = user_email, text= post_data, time= datetime.datetime.now())
        post_box.put()
    def get (self):



class PostData(ndb.Model):
    email_address = ndb.StringProperty()
    text = ndb.StringProperty()
    time = ndb.DateProperty()

class ListPostsHandler(webapp2.RequestHandler):
    def get(self):
        all_posts_query = PostData.query()
        all_posts = all_posts_query.fetch()
        for post in all_posts:
            self.response.out.write(post.email_address + post.text + str(post.time))
            self.response.out.write('<br>')






    # save to to MainHandl
        # add timestamp




app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/createprofile', CreateProfileHandler),
  ('/profile', ProfileHandler),
  ('/postbox', PostHandler),
  ('/listposts', ListPostsHandler),
>>>>>>> 87415cdad4ec84a460fdfbac084ce5f0e954cb1d
], debug=True)
