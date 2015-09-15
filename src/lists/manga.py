import io, json, os, rarfile
from sys import platform
from zipfile import ZipFile

if platform == 'win32':
   rarfile.UNRAR_TOOL = './deps/unrar.exe'
IMAGE_TYPES = ['jpg', 'jpeg', 'gif', 'png']


with open('./config.json', encoding='utf8') as file_:
   config = json.loads(file_.read())
   root = config['root']


"""
Functions to make sure only images are pulled
"""

def cover_cleaner (filelist):
   for item in filelist:
      if item.split('.')[-1].lower() in IMAGE_TYPES:
         result = item
         break
   return result


def pages_cleaner (filelist):
   result = []
   for item in filelist:
      if item.split('.')[-1].lower() in IMAGE_TYPES:
         result.append(item)
   return result


"""
Pulls the first image of a archive
"""

def get_cover (filepath):
   path = root + '/' + filepath

   if os.path.isdir(path):
      files = sorted(os.listdir(path))
      image = path + '/' + cover_cleaner(files)

      with open(image, 'rb') as file_:
         cover = file_.read()
         return cover

   elif os.path.isfile(path):
      filetype = path.split('.')[-1]

      if filetype == 'zip':
         with ZipFile(path) as archive:
            files = sorted(archive.namelist())
            image = cover_cleaner(files)

            with archive.open(image) as file_:
               cover = file_.read()
               return cover

      elif filetype == 'rar':
         with rarfile.RarFile(path) as archive:
            files = sorted(archive.namelist())
            image = cover_cleaner(files)

            with archive.open(image) as file_:
               cover = file_.read()
               return cover


"""
Pulls the current image as a page
"""

def get_page (filepath, pagenum):
   path = root + '/' + filepath

   if os.path.isdir(path):
      files = sorted(os.listdir(path))
      files = pages_cleaner(files)

      image = path + '/' + files[pagenum - 1]
      with open(image, 'rb') as file_:
         page = file_.read()
         return page

   elif os.path.isfile(path):
      filetype = path.split('.')[-1]

      if filetype == 'zip':
         with ZipFile(path) as archive:
            files = sorted(archive.namelist())
            files = pages_cleaner(files)

            image = files[pagenum - 1]
            with archive.open(image) as file_:
               page = file_.read()
               return page

      elif filetype == 'rar':
         with rarfile.RarFile(path) as archive:
            files = sorted(archive.namelist())
            files = pages_cleaner(files)

            image = files[pagenum - 1]
            with archive.open(image) as file_:
               page = file_.read()
               return page


"""
Returns total pages for hyperlinking
"""

def get_total_pages (filepath):
   path = root + '/' + filepath

   if os.path.isdir(path):
      files = os.listdir(path)
      return len(files)

   elif os.path.isfile(path):
      filetype = path.split('.')[-1]

      if filetype == 'zip':
         with ZipFile(path) as archive:
            files = archive.namelist()
            return len(files)

      elif filetype == 'rar':
         with rarfile.RarFile(path) as archive:
            files = archive.namelist()
            return len(files)