from ownblog import app ,bcrypt ,db,mail
from flask import Flask ,render_template , redirect ,url_for,flash ,request
from ownblog.forms import LoginForm , RegistrationForm ,PostForm , CommentForm
from ownblog.models import User , Post ,Comment
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user ,current_user, logout_user ,login_required
import pywhatkit as kit
from flask_mail import Message
                

@app.route("/home", methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def home():
    pw_hash = bcrypt.generate_password_hash('hunter2')
    
    b=b'$2b$12$/OZApvVtFC2V0broXd2kyefzDpWFrKv/QgTjH3PvG.u7kexVLHEcW'
    a=bcrypt.check_password_hash(b, 'hunter2')
    print(a)
    page= request.args.get('page', 1, type=int)
    posts= Post.query.paginate(page=page, per_page=4)
    return render_template('home.html',title="SPEM Project", posts=posts)


@app.route("/login" , methods=["post","get"])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form)

@app.route("/register", methods=["post","get"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data)
        user= User(username=form.username.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("User created!!","info")
        return redirect(url_for('login'))
    return render_template("register.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_required
@app.route("/post",methods=["Post","GET"])
def post():
    form =PostForm()
    if form.validate_on_submit():
        flash("Post created", 'success')
        post= Post(title=form.title.data, content=form.post.data , author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html',form=form)

@app.route("/upvote/<int:post_id>")
def upvote(post_id):
    post= Post.query.filter_by(id=post_id).first()
    post.upvotes= post.upvotes+1
    post.author.karma= post.author.karma+1
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/downvote/<int:post_id>")
def downvote(post_id):
    post= Post.query.filter_by(id=post_id).first()
    post.downvotes= post.downvotes+1
    post.author.karma= post.author.karma-0.5
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>" , methods=["post","get"])
def see_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    comment_on_post = Comment.query.filter_by(post_id=post_id).all()
    form= CommentForm()
    if form.validate_on_submit():
        comment_add= Comment(content=form.post.data , author_id=current_user.id , post_id=post.id)
        db.session.add(comment_add)
        db.session.commit()
        return redirect(url_for('see_post',post_id=post.id))
    
    if request.method=="POST" and "email" in request.form:
        msg = Message('Take this',
                  sender='noreply@demo.com',
                  recipients=[request.form.get("email_send")])
        msg.body = '''
                    {}
                    '''.format(post.content)
        mail.send(msg)

    if request.method=="POST" and "delete" in request.form:
        post_id=request.form.get('delete')
        post= Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect (url_for('home'))




    return render_template('see_post.html',post=post , comments=comment_on_post , form=form)

@app.route("/user/<int:user_id>")
def see_user(user_id):
    user= User.query.filter_by(id=user_id).first()
    return render_template('see_user.html' , user=user)

@app.route("/post/edit/<int:post_id>" , methods=["post","GET"])
def edit_post(post_id):
    post= Post.query.filter_by(id=post_id).first()
    if current_user!=post.author:
        return redirect(url_for('home'))
    form= PostForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content = form.post.data
        db.session.commit()
        return redirect(url_for('home'))
    form.title.data= post.title
    form.post.data=post.content
    return render_template("edit.html", form=form)

@app.route("/post/delete/<int:post_id>" , methods=["POST"])
def delete_post(post_id):
    post= Post.query.filter_by(id=post_id).first()
    if current_user!=post.author:
        return redirect(url_for('home'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Your Post has been deleted' , 'success')
        return redirect (url_for('home'))

@app.route("/whatsapp/<int:post_id>" , methods=["POST","GET"])
def whatsapp(post_id):
    post= Post.query.filter_by(id=post_id).first()
    print(post.content)
    kit.sendwhatmsg("+918116008881", "{}", 19, 55).format(post.content)
    return redirect(url_for('home'))
    
import tweepy as tw
import inspect
from apiclient.discovery import build
@app.route("/twitter" , methods=["POST","GET"])
def twitter():
            
    consumer_key ="Ms3wyaIb58mtQYH54SfJIz4Hl"
    consumer_secret ="V2sEIPGzAWyJGbCxqoJgbvEdyF7hqjlXfLCV8NVCW6LlFr4NRZ"
    access_token ="1046412032399028227-BOFIefOaJ0M549dNyzE9D0G8BExJFO"
    access_token_secret ="thau8J2FEutlfiR06DAwpAZni9lv7qL9R1Y5zcz4E8zpu"

    auth = tw.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tw.API(auth)

    search_words = "SRM"
    date_since = "2018-11-16"

    new_search = search_words + " -filter:retweets"
    search = "MKBHD"

    if request.method=="POST" and "action" in request.form:

        a=request.form.get('search')
        search_words = a
        new_search = search_words + " -filter:retweets"
        search=a
    # Collect tweets
    tweets = tw.Cursor(api.search,
                q=new_search,
                lang="en",
                since=date_since).items(10)

    data=[]
    url=[]
    i=0
    for tweet in tweets:
        url.append("https://twitter.com/twitter/statuses/"+str(tweet.id))
        data.append(tweet.text)


    api_key = "AIzaSyCLcd-_5RCgK7lYE2XuF1vuXOCaCARTrfo"
    youtube = build('youtube','v3',developerKey = api_key)
    
    

    request_yt = youtube.search().list(q=search,part='snippet',type='video')
    res = request_yt.execute()
    yt_data=[]
    yt_url=[]
    for item in res['items']:

        yt_data.append(item['snippet']['title'])
        # print(['id']['videoId'])
        string='https://www.youtube.com/watch?v='
        yt_url.append(string+item['id']['videoId'])

    return render_template("twitter.html",data=data,yt_data=yt_data,url=url,yt_url=yt_url)

    




