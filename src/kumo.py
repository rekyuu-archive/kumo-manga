import io, json
import redis
from lists import folder, manga
from flask import Flask, render_template, send_file
from flask_httpauth import HTTPBasicAuth

app  = Flask(__name__)
auth = HTTPBasicAuth()
r = redis.Redis(host='localhost', port=6379, db=0)

"""
Helper definitions.
"""

def url_parent (url):
   try:
      fork = url.split('/')
      del fork[-1]
      path = '/'.join(fork)
   except IndexError:
      path = ''

   return path


def get_title (url):
   fork = url.split('/')
   title = fork[-1]
   if len(title.split('.')) >= 2:
      title = title.split('.')[0]

   return title


"""
Authentication

Add @auth.login_required below the last @app.route()
line to add simple HTML auth.
"""

with open('./config.json', encoding='utf8') as file_:
   config = json.loads(file_.read())
   users = config['auth']

@auth.get_password
def get_pw (username):
   if username in users:
      return users.get(username)
   return None


"""
Routing
"""

@app.route('/')
def index ():
   return render_template('index.html')

@app.route('/list')
@app.route('/list/')
def manga_list ():
   return render_template(
      'list.html',
      items = folder.return_listing()
   )

@app.route('/list/<path:subfolder>')
def manga_list_folder (subfolder):
   return render_template(
      'list.html',
      current = subfolder,
      parent = url_parent(subfolder),
      items = folder.return_listing(subfolder)
   )

@app.route('/read/<path:filename>')
@app.route('/read/<path:filename>/<int:pagenum>')
def manga_read (filename, pagenum=1):
   return render_template(
      'read.html',
      current = filename,
      current_page = pagenum,
      manga_title = get_title(filename),
      total_pages = manga.get_total_pages(filename),
      parent = url_parent(filename)
   )

# Image handling

@app.route('/cover/<path:filepath>')
def manga_cover (filepath):
   cover = r.get(filepath)
   if not cover:
      cover = manga.get_cover(filepath)
      r.set(filepath, cover)
   return send_file(io.BytesIO(cover))

@app.route('/page/<path:filepath>/<int:pagenum>')
def manga_page (filepath, pagenum=1):
   page = r.get(filepath + str(pagenum))
   if not page:
      page = manga.get_page(filepath, pagenum)
      r.set(filepath + str(pagenum), page)
   return send_file(io.BytesIO(page))


"""
Server
"""

if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5266, debug = False)
