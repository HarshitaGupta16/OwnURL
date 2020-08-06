#app.py becomes urlshort.py

#if we want to save our step of assigning varible FLASK_APP=hello (hello.py is name of file) then we can name th file app.py instead of hello.py
#flask is smat enough to know that inside of the directory if there is a file named app.py that is the default app that it should be running.
#but we will set FLASK_ENV=development for development mode


from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint              
import json
import os.path
from werkzeug.utils import secure_filename                             #to check if file is safe to save

#abort allows us to, when something goes wrong, send a special message depending on what it is
#one of the great feature of flask is it makes easy to save information into a cookie so that when user comes back to our website, we have some data ready for them to see. 
#Sessions and cookies are a way to store some info into user's browser, it uses it as a key value store to say(like keep me signed in button, it uses cookie)
#session allows us to access cookies

bp = Blueprint('urlshort', __name__)

#print(__name__)
"""
@app.route('/')
def home():
    return render_template('home.html', name='Harshita')

"""

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())        #besides saying we want home.html, let's say we also want to provide all different codes that comes as part of cookies
                                                                     #.keys() gets us all the values that are thee on sort of the left side of the dictionary, right, all the values that say true
                                                                     #that we are setting them equal to. This info is passed to home.html


@bp.route('/about')
def about():
    return 'This is a url-shortner'


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}                                                               #create dict with code as key and url as value

        if os.path.exists('urls.json'):                                         #if this files already exists
            with open('urls.json') as urls_file:                                #if it exists then open it as urls_file
                urls = json.load(urls_file)                                   #we will load the data of json file into the dictionary back to compare that key(code) and the url doesn't already exist

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')    #we have to pass forward this flash to the template that you are about to display
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():                                                   #To check if it is a file or a URL
            print(request.form.keys)                                   
            urls[request.form['code']] = {'url':request.form['url']}

        else:
            f = request.files['file']                                            #grab the file from the form and put it in variable 'f', in this we give key as file inside it
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save(r'E:\TCS-LearningProgram\AscendPythonFlask\FlaskEssentialTraining-LinkedInCourse\url-shortner-with-blueprint\urlshort\static\user_files/' + full_name)  #You either need to duplicate all backslashes or prefix the string with r (to produce a raw string).
                                                                                                          #Users can upload file with same name so make sure that we don't overwrite the information
                                                                                                          # We know that codes are going to be unique so we take code that user has povided and the file name and combine those 2 things
                                                                                                          # so that they don't collide with each other. 
            urls[request.form['code']] = {'file':full_name}

        #urls[request.form['code']] = {'url': request.form['url']}               #for value we have to specify whether it is a url or a file, so another dict inside where pass'url' as key and url given by user as value
        with open('urls.json', 'w') as url_file:                                #'w' specifies for writing, this will check only move forward if u are able to create or open this url.json file with the name url_file
            json.dump(urls, url_file)                                           #we save urls to this file url_file
            session[request.form['code']] = True                                #save those codes into cookie, that login user has created. Inside session, we provide key that we want to save into dictionary
                                                                                   #we don''t need to store value associated with this course sp we store True, so that we get those codes saved into cookies.
                                                                                   #To display session information we do it on homepage
        return render_template('your_url.html', code=request.form['code'])      #we need to get access to the information from the request, in this case it was a get request, 
                                                                                #so to get the input code we need to import request
                                                                                #in request.args, args is a dictionary for different parameters that could be passed in as get parameters
                                                                                #this info is passed forward to our template.
    else:
        #return 'This is not valid.'
        #return render_template('home.html')         #rather than rendering to the home template which will only show home page content and not change url, we should redirect them bcz redirecting will change the url as well.                           
#now we cannot enter anything manually in the url becuse we are using POST request     
        #return redirect('/')                        #here we have to manually type the path for home, what if path change its direction and become '/home', so use ul_for                        
        return redirect(url_for('urlshort.home'))    #url_for() creates the url for us based on the function name

#if we use GET request then all of the data is displayed on the url .
#with POST request we use request.form instead of request.args 
#we will make use of dictionary(json)

@bp.route('/<string:code>')  #look for after the first slash on the website, any sort of string and put it in a variable called code.
#This is called a variable route, it says look at the sting and then pass that string to function which determine what to give back to the user.
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():            #this tells if code they have entered matches anything that we found here, we can go ahead and display that url back to user
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))             #url_for() looking for static file

    return abort(404)                    

@bp.errorhandler(404)                 #if we want to create our custom error page, we can create our own route. Now, instead of route we will call it errorhandler
                                       #this is the error handler for 404 code
def page_not_found(error):
    return render_template('page_not_found.html'), 404          #404 here specifies that this should come back with a 404 error code, this will tell browser that itis a 404 error                                       


#imagine someone has created lot of codes, could have really long list of things, so it is better to introduce API into our project. 
@bp.route('/api')                          
def session_api():                                 #return back session keys in a list and make sure it is in JSON format. For this flask has a tool jsonify.
    return jsonify(list(session.keys()))           #jsonify takes any sort of list or dictionary and turns it into JSON code for you
