

import jinja2
import os
import webapp2
import datetime

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
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if cssi_user:
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              cssi_user.first_name,
              cssi_user.last_name,
              email_address,
              signout_link_html))
      # If the user hasn't been to our site, we ask them to sign up
      else:
        self.response.write('''
            <div style= "color:blue" >Welcome to our site, %s!  Please sign up! </div><br>
            <form method="post" action="/">
            <input type="text" name="first_name">
            <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))



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

        cssi_user.put()
        html=p_template.render({
        'firstName':cssi_user.first_name ,
        'lastName': cssi_user.last_name,
        'college':cssi_user.college,
        'fb':cssi_user.fb,
        'insta':cssi_user.insta,
        })
        self.response.write(html)








class PostHandler(webapp2.RequestHandler):
    def get (self):
        make_a_post_template=jinja_env.get_template('make-a-post.html')
        html= make_a_post_template.render({
        })
        self.response.write(html)
    def post(self):
        post_data = self.request.get("Post Box")
        user_email= self.request.get("email_address")
        time = datetime.now()
        post_box= PostData(email_address = user_email, text= post_data, time=time)
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
            self.response.out.write(post.email_address + "     " + post.text + "     ")
            self.response.out.write('<br>')
            self.response.out.write(ctime)
            self.response.out.write("    ")
            self.response.out.write('<br>')
            self.response.out.write('<br>')


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/createprofile', CreateProfileHandler),
  ('/profile', ProfileHandler),
  ('/postbox', PostHandler),
  ('/listposts', ListPostsHandler),
], debug=True)
