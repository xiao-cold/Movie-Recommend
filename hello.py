from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request

app=Flask(__name__)

@app.route('/login/')
@app.route("/login/<username>")
def hello_world(username=None):
    name=request.cookies.get('username')
    print(name)
    return render_template('example2.html',username=username)
@app.route('/hello/')
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('example.html',name=name)

@app.route('/list/')
def _list():
    username = request.args.get('username')
    password = request.args.get('password')
    return 'list'+'/'+username+'/'+password

@app.route('/')
def helloworld():
    context={'users':{'username':'aaa','age':12,'addr':'xxx'}}
    return render_template('index.html',**context)


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)

### HTTP Methods
# @app.get('/login')
# def login_get():
#     return show_the_login_form()
# @app.post('/login')
# def login_post():
#     return do_the_login()



if __name__ == '__main__':
    app.run()