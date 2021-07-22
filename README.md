# Blog project
blog with posts on django

# Pages

   - login/ view class - LoginView. Login give you abilyty to subscribe to Blogs you like, and publish your own posts in your blog.
     - GET return login page
     - POST make log-in
     
   - logout/ view class - LogoutView
     - POST make log-out

   - blogs/  view class - BlogList. 
     - GET return blogs list page with additional information
     
   - blogs/<blog_id>/subscribe/  view class - Subscribe
     - POST Subscribe to Blog with blog_id
   - blogs/<blog_id>/unsubscribe/ view class - Unsubscribe
     - POST Unubscribe from Blog with blog_id
   - blogs/<blog_id>/blogedit/ view class - BlogUpdateView
     - GET if you owner of blog with blog_id return blog editing page, else return 403
     - POST change description of your blog
   - blogs/<blog_id>/ view class - BlogDetailView
      - GET return posts list page of blog with blog_id

   - myfeed/ view class - PostList
      - GET return post list page of blogs which you subscribed on
   - post/post_id/read/ view class - Read
      - POST make read flag on post with post_id
   - post/post_id/ view class - PostDetailView
      - GET return post page with post_id
   - post/post_id/edit/ view class - PostUpdateView
      - GET if you owner of post with post_id return post editing page, else return 403
      - POST change title and text of post with post_id
   - post/post_id/delete/ view class - PostDeleteView
      - GET if you owner of post with post_id return post deleting page, else return 403
      - POST delete your post with post_id
   - myposts/ view class - MyPostList
      - GET return list of your posts

   - createpost/ PostCreate
      - GET return post creating page
      - POST create post in your blog. Creating post will send emails to your blog subscribers 
      
 # Launching instruction
 For easy lauching need **docker-compose**
 
 In *blogs/blogs/* edit **settings.py**
 
 Your ip or domain
    PROJECT_DOMAIN = 'http://YOUR_IP_OR_DOMAIN:8000'
    
 Edit email host. Gmail is default host  
  
    EMAIL_HOST='smtp.gmail.com' 

 Edit your email host user and password

    EMAIL_HOST_USER='YOUR_EMAIL'
    EMAIL_HOST_PASSWORD='YOUR_PASSWORD'
 
 
 Start in project root folder:
 
    docker-compose build
    
 Project don't have registration functional. Need to create superuser(admin) to create users.
 
    docker-compose run createsuperuser
    
 Run django server
 
    docker-compose up
      
  Project will be available on http://YOUR_IP_OR_DOMAIN:8000
  To add users go to /admin/ (IT HAS NO STATIC, need to use webserver (eg. Nginx, Apache etc))
      
      
