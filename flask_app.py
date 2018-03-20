import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import datetime
#import bcrypt


#conn.execute("create table post(id integer primary key autoincrement, status text, image text, date_posted datetime, user_id integer);")
#conn.execute("create table like(id integer primary key, post_id integer, like_by user_id)")
#conn.execute("create table comment(id integer primary key, post_id integer, comment text ,comment_by user_id)")
#conn.execute("create table user(id integer primary key, username text, password text, dob datetime, gender text, country text, email text)")
#conn.execute("create table request(id integer primary key, from_id integer, to_id integer)")
#conn.execute("create table friend(id integer primary key, from_id integer, to_id integer)")
#conn.execute("create table message (id integer primary key, from_id integer, to_id integer, msg text, date datetime)")


app = Flask(__name__)
app.secret_key = os.urandom(12)
#conn = sqlite3.connect("/home/tmvinoth3/mysite/social.db")
conn = sqlite3.connect("social.db")
#conn.execute("alter table user add column image text")
#conn.commit()
#conn.execute("alter table user add column msg_count integer")
#conn.execute("alter table user add column notify_count integer")
#conn.commit()


@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'GET':
            return render_template('social_login.html')
    elif request.method == 'POST':
            print("Check Login  Post")
            uname = request.form['uname']
            print("Check Login User Query")
            users = conn.execute("select * from user where username='{}'".format(uname))
            print("Check Login Post")
            dictUsers = [dict(id=item[0],username=item[1],password=item[2]) for item in users]
            if len(dictUsers) == 0:
                return render_template('social_login.html',msg=0)
            else:
              res = dictUsers[0]
              print("Check Password {}".format(request.form['pwd'].encode('utf-8')), res['password'])
              #if bcrypt.check_password_hash(res['password'],request.form['pwd'].encode('utf-8')):
              #if bcrypt.checkpw(request.form['pwd'].encode('utf-8'),res['password'].encode('utf-8')): 
              if request.form['pwd'] == res['password']:
                  session[res['username']] = True
                  print("Session name", res['username'], session[res['username']])
                  session['user'] = res['username']
                  session['user_id'] = res['id']
                  session['logged'] = True
                  print("Check UserID => ",session['user_id'])
                  return redirect(url_for('display'))
              else:
                  return render_template('social_login.html',msg=0)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'GET':
            return render_template('social_signup.html')
    elif request.method == 'POST':

            uname = request.form['uname']
            pwd = request.form['pwd']
            pwdConfirm = request.form['pwdConf']
            if 'gender' in request.form:
                gender = request.form['gender']
            country = request.form['country']
            dob = request.form['dob']
            email = request.form['email']
            file = request.files['image']
            image = file.filename
            if image == "":
                image = "user.jpeg"
            else:
                file.save(file.save(os.path.join("static/img", file.filename)))#file.save(file.save(os.path.join("/home/tmvinoth3/mysite/static/img", file.filename)))
            if pwd != pwdConfirm:
                return render_template('social_signup.html',msg='Password Mismatch')
            #pwd = bcrypt.generate_password_hash(request.form['pwd'].encode('utf-8'))
            #pwd = bcrypt.hashpw(request.form['pwd'].encode('utf-8'), bcrypt.gensalt())
            users = conn.execute("select * from user where username='{}'".format(uname))
            dictUsers = [dict(id=item[0]) for item in users]
            #print(dictUsers,len(dictUsers))
            if len(dictUsers) == 0:
                conn.execute("insert into user (username, password, dob, gender, country, email, image) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(uname, pwd, dob, gender, country, email, "img/{}".format(image)))
                conn.commit()
                return redirect(url_for('login'))
            else:
                return render_template('social_signup.html',msg='Username already exists')

@app.route('/logout/<string:user>',methods=['GET','POST'])
def logout(user):
    if request.method == 'POST':
        return login()
    else:
        session[user] = False
        return render_template('social_login.html',msg=2)

@app.route('/notLogged',methods=['GET','POST'])
def notLogged():
    return render_template('social_login.html',msg=300)

@app.route('/home',methods=['GET','POST'])
def display():
    print("Check Session Befor Display",session.get('logged'))
    if session.get('logged') == True:
      if request.method == "POST":
          if request.form['create'] == 'Post':
              print("Check create method ")
              return create()
          elif request.form['create'] == "Update":
              print("Check update method in display")
              return update()
          else:
              print("Check update_User method in display")
              return update_User()
      conn.execute("update user set msg_count=0 where msg_count='None' or msg_count=null or msg_count=''")
      conn.commit()
      msgQuery = conn.execute("select m.from_id,u.username from message m join user u on m.from_id=u.id where m.to_id={}".format(session['user_id']))
      msgs = [dict(uid=u[0], uname=u[1]) for u in msgQuery]
      userInfoQuery = conn.execute("select msg_count,notify_count from user where id={}".format(session['user_id']))
      userInfo = [dict(msgCount=u[0],notifyCount=u[1]) for u in userInfoQuery]
      session['msgCount'] = (userInfo[0])['msgCount']
      session['notifyCount'] = (userInfo[0])['notifyCount']
      print("Check Messgae Count ",(userInfo[0])['msgCount'])
      print("Check UserInfo: ",userInfo)
      #posts = conn.execute("select p.id,p.status,p.image,p.date_posted,u.username,l.like_by from post p join user u on p.user_id=u.id left join like l on p.id=l.post_id where l.like_by={} and p.user_id in(select f.from_id from user u join friend f on u.id=f.to_id where f.to_id={}) or p.user_id={}".format(session['user_id'],session['user_id'],session['user_id']))
      #postQuery = conn.execute("select commentpost.id,commentpost.status,commentpost.image,commentpost.date_posted,commentpost.username,commentpost.like_by,c.comment,c.comment_by from (select *,l.like_by as like_by from (select p.id as id,p.status as status,p.image as image,p.date_posted as date_posted,u.username as username from post p join user u on p.user_id=u.id where p.user_id in(select f.from_id from user u join friend f on u.id=f.to_id where f.to_id={}) or p.user_id={}) likepost left join like l on likepost.id=l.post_id) commentpost left join comment c on commentpost.id=c.post_id ".format(session['user_id'],session['user_id']))
      postQuery = conn.execute("select p.id as id,p.status as status,p.image as image,p.date_posted as date_posted,u.username as username, p.user_id, u.image from post p join user u on p.user_id=u.id where p.user_id in(select f.from_id from user u join friend f on u.id=f.to_id where f.to_id={}) or p.user_id={} order by p.id desc".format(session['user_id'],session['user_id']))
      #post = [dict(id=p[0],status=p[1],image=p[2],date=p[3],username=p[4],liked_by=p[5],comment=p[6],comment_by=p[7]) for p in posts]
      posts = []
      print("Check1")
      for p in postQuery:
          print("Check User Image ",p[6])
          post = dict(id=p[0],status=p[1],image=p[2],date=p[3],username=p[4],puser_id=p[5],user_image=p[6])
          likeQuery = conn.execute("select like_by,u.username from like l join user u on l.like_by=u.id where l.post_id={}".format(p[0]))
          likes = [dict(liked_by=l[0],uname=l[1]) for l in likeQuery]
          liked_by = 0
          for li in likes:
              liked_by = li['liked_by'] if li['liked_by'] == session['user_id'] else 0
          commentQuery = conn.execute("select comment,comment_by,username from comment c join user u on c.comment_by=u.id where post_id={}".format(p[0]))
          comments = [dict(comment=c[0],comment_by=c[1],uname=c[2]) for c in commentQuery]
          post["liked_by"] = liked_by
          post["likes"] = likes
          post["comments"] = comments
          posts.append(post)
      print("Check after loop")
      #post.update({'id': session['user_id'], 'key 3': 'value 3'}) =
      userQuery = conn.execute("select * from user where id !={} and id not in(select r.to_id from user u join request r on u.id=r.from_id where u.id={}) and id not in(select r.to_id from user u join friend r on u.id=r.from_id where u.id={})".format(session['user_id'],session['user_id'],session['user_id']))
      users = [dict(id=u[0],username=u[1]) for u in userQuery]
      reqSentUsersQuery = conn.execute("select * from user where id !={} and id in(select r.to_id from user u join request r on u.id=r.from_id where u.id={}) and id not in(select r.to_id from user u join friend r on u.id=r.from_id where u.id={})".format(session['user_id'],session['user_id'],session['user_id']))
      reqSent = [dict(id=u[0],username=u[1]) for u in reqSentUsersQuery]
      myRequestQuery = conn.execute("select * from user where id in(select r.from_id from user u join request r on u.id=r.to_id where r.to_id={})".format(session['user_id']))
      reqUsers = [dict(id=r[0],username=r[1]) for r in myRequestQuery]
      friendQuery = conn.execute("select * from user where id !={} and id in(select r.to_id from user u join friend r on u.id=r.from_id where u.id={})".format(session['user_id'],session['user_id']))
      friends = [dict(id=r[0],username=r[1]) for r in friendQuery]
      for u in users:
          for r in reqUsers:
              if u['id'] == r['id']:
                  users.remove(u)
          for rs in reqSent:
              if u['id'] == rs['id']:
                  users.remove(u)
      return render_template('displayHome.html',post=posts,users=users,reqUsers = reqUsers, reqSent = reqSent, friends=friends,userInfo=userInfo,msgs=msgs)
    else:
       return render_template('social_login.html',msg=300)

@app.route("/post",methods=['POST','GET'])
def create():
         if request.method == 'GET':
          return render_template('post.html')
         else:
          print("Check Before datetime")
          #post_date = datetime.datetime.now()
          post_date = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
          file = request.files['image']
          image = file.filename
          if image != "":
            file.save(os.path.join("static/img", file.filename))
			#file.save(os.path.join("/home/tmvinoth3/mysite/static/img", file.filename))
            image = "img/{}".format(image)
          #conn.execute("insert into post (status,image,date_posted) values ('{}','{}','{}')".format(request.form['status'], "img/{}".format(request.form['image']),post_date))
          conn.execute("insert into post (status,image,date_posted,user_id) values ('{}','{}','{}',{})".format(request.form['status'], image,post_date,session['user_id']))
          conn.commit()
          return redirect(url_for('display'))

@app.route("/update",methods=['POST','GET'])
def update():
         if request.method == 'POST':
          post_date = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
          file = request.files['image']
          image = file.filename
          print("Check Before file Image", image)
          if image == "":
            print("Check Before Old Image", request.form['imageOld'])
            image = request.form['imageOld']
          else:
            image ="img/{}".format(image)
            file = request.files['image']
            file.save(os.path.join("static/img", file.filename))
            #file.save(os.path.join("/home/tmvinoth3/mysite/static/img", file.filename))
          #conn.execute("insert into post (status,image,date_posted) values ('{}','{}','{}')".format(request.form['status'], "img/{}".format(request.form['image']),post_date))
          conn.execute("update post set status='{}',image='{}',date_posted='{}',user_id={} where id={}".format(request.form['status'], image,post_date,session['user_id'],request.form['post_id']))
          conn.commit()
          return redirect(url_for('display'))

@app.route("/updateUser",methods=['POST','GET'])
def update_User():
        if request.method == 'POST':

                uname = request.form['uname']
                if 'gender' in request.form:
                    gender = request.form['gender']
                country = request.form['country']
                dob = request.form['dob']
                email = request.form['email']
                file = request.files['image']
                image = file.filename
                print("Check update method in updateUser filename",file.filename)
                if image == "":
                  image = request.form['imageOld']
                else:
                  image ="img/{}".format(image)
                  file = request.files['image']
                  print("Check before save updateUser")
                  file.save(os.path.join("static/img", file.filename))
                  #file.save(os.path.join("/home/tmvinoth3/mysite/static/img", file.filename))
                users = conn.execute("select * from user where username='{}'".format(uname))
                dictUsers = [dict(id=item[0]) for item in users]
                print("Check update method in updateUser after dict")
                if len(dictUsers) > 0:
                    conn.execute("update user set username='{}', dob='{}', gender='{}', country='{}', email='{}', image='{}' where id={}".format(uname, dob, gender, country, email, image, session['user_id']))
                    conn.commit()
        return redirect(url_for('display'))

@app.route("/getUserInfo",methods=['POST'])
def getUserInfo():
          print("Check getUserInfo")
          id = request.json['id']
          userInfoQuery = conn.execute("select username, dob, gender, country, email, image from user where id={}".format(id))
          userInfo = [dict(uname=u[0],dob=u[1],gender=u[2],country=u[3],email=u[4],image=u[5]) for u in userInfoQuery]
          return jsonify(userInfo[0])

@app.route("/sendRequest",methods=['POST'])
def sendRequest():
        if request.method == 'POST':
          print("Send Request")
          conn.execute("insert into request (from_id,to_id) values ({},{})".format(session['user_id'],request.json['toId']))
          conn.commit()
        return redirect(url_for('display'))

@app.route("/cancelRequest",methods=['POST'])
def cancelRequest():
        if request.method == 'POST':
          print("Cancel Request")
          conn.execute("delete from request where from_id={} and to_id={}".format(session['user_id'],request.json['toId']))
          conn.commit()
        return redirect(url_for('display'))

@app.route("/acceptRequest",methods=['POST'])
def acceptRequest():
        if request.method == 'POST':
          print("Accept Request")
          conn.execute("insert into friend (from_id,to_id) values ({},{})".format(session['user_id'],request.json['toId']))
          conn.execute("insert into friend (from_id,to_id) values ({},{})".format(request.json['toId'],session['user_id']))
          conn.execute("delete from request where from_id={} and to_id={}".format(request.json['toId'],session['user_id']))
          conn.commit()
        return redirect(url_for('display'))

@app.route("/unfriend",methods=['POST'])
def unfriend():
        if request.method == 'POST':
          print("Unfriend Request")
          conn.execute("delete from friend where from_id={} and to_id={}".format(request.json['toId'],session['user_id']))
          conn.execute("delete from friend where from_id={} and to_id={}".format(session['user_id'],request.json['toId']))
          conn.commit()
        return redirect(url_for('display'))

@app.route("/denyRequest",methods=['POST'])
def denyRequest():
        if request.method == 'POST':
          print("Deny Request")
          conn.execute("delete from request where from_id={} and to_id={}".format(request.json['toId'],session['user_id']))
          conn.commit()
        return "unfriend success"

@app.route("/like",methods=['POST'])
def like():
        if request.method == 'POST':
          print("Like Post")
          print(request.json['post_id'],request.json['liked_by'])
          conn.execute("insert into like (post_id,like_by) values ({},{})".format(request.json['post_id'],request.json['liked_by']))
          conn.commit()
        return "like success"

@app.route("/unlike",methods=['POST'])
def unlike():
        if request.method == 'POST':
          print("Unlike Post")
          print(request.json['post_id'],request.json['liked_by'])
          conn.execute("delete from like where post_id={} and like_by={}".format(request.json['post_id'],request.json['liked_by']))
          conn.commit()
        return "unlike success"

@app.route("/comment",methods=['POST'])
def comment():
        if request.method == 'POST':
          print("Comment Request")
          print(request.json['post_id'],request.json['comment'],request.json['comment_by'])
          conn.execute("insert into comment (post_id,comment,comment_by) values ({},'{}',{})".format(request.json['post_id'],request.json['comment'],request.json['comment_by']))
          conn.commit()
        return redirect(url_for('display'))

@app.route("/msg",methods=['POST'])
def msg():
        if request.method == 'POST':
          print("Message Request")
          conn.execute("insert into message (from_id,to_id,msg,date) values ({},{},'{}',date('now'))".format(session['user_id'],request.json['toId'],request.json['msg']))
          conn.execute("update user set msg_count=msg_count+1 where id={}".format(request.json['toId']))
          conn.commit()
        return "message success"

@app.route("/showMsgs",methods=['POST'])
def showMsg():
        if request.method == 'POST':
          print("Show Messgae Request")
          msgsQuery = conn.execute("select * from (select u.username, m.msg, m.from_id,m.date as date from message m join user u on m.from_id=u.id where u.id={} and m.to_id={} union select u.username, m.msg, m.from_id, m.date as date from message m join user u on m.from_id=u.id where m.from_id={} and m.to_id={}) msgs order by msgs.date".format(request.json['id'],session['user_id'],session['user_id'],request.json['id']))
          msgs = [dict(uname=m[0],msg=m[1],id=m[2]) for m in msgsQuery]
          conn.commit()
        return jsonify(msgs)

@app.route("/clearMsgCount",methods=['POST'])
def clearMsg():
        if request.method == 'POST':
          print("Clear message Request")
          conn.execute("update user set msg_count=0 where id={}".format(session['user_id']))
          conn.commit()
        return "clear message success"

@app.route("/clearNotifyCount",methods=['POST'])
def clearNotification():
        if request.method == 'POST':
          print("Message Request")
          conn.execute("update user set notify_count=0 where id={}".format(session['user_id']))
          conn.commit()
        return "success"

app.route("/testpost",methods=['POST'])
def testPost():
    if session.get('logged') == True:
        if request.method == 'POST':
          print(request.json['check'])
        return "Success"
    else:
        return render_template('social_login.html',msg=300)

@app.route("/delete/<int:post_id>")
def delete(post_id):
 if session.get('logged') == True:
     conn.execute("delete from post where id='{}'".format(post_id))
     conn.execute("delete from like where post_id='{}'".format(post_id))
     conn.execute("delete from comment where post_id='{}'".format(post_id))
     conn.commit()
     return redirect(url_for('display'))
 else:
     return render_template('social_login.html',msg=300)

if __name__ == "__main__":

 app.run()



