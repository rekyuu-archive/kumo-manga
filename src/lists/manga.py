import io, json, os, rarfile, random
from sys import platform
from zipfile import ZipFile
from heapq import merge

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
      files = quick(os.listdir(path))
      image = path + '/' + cover_cleaner(files)

      with open(image, 'rb') as file_:
         cover = file_.read()
         return cover

   elif os.path.isfile(path):
      filetype = path.split('.')[-1]

      if filetype == 'zip':
         with ZipFile(path) as archive:
            files = sort_titles(archive.namelist())
            image = cover_cleaner(files)

            with archive.open(image) as file_:
               cover = file_.read()
               return cover

      elif filetype == 'rar':
         with rarfile.RarFile(path) as archive:
            files = sort_titles(archive.namelist())
            image = cover_cleaner(files)

            with archive.open(image) as file_:
               cover = file_.read()
               return cover

"""
Properly orders pages for a manga - needs some serious thought put into it
"""
# Wrapper to do an initial shuffle to prevent a quicksort worstcase
def sort_titles (titles):
   random.shuffle(titles)
   return quicksort_titles(titles)

# Quicksort with custom compare
def quicksort_titles (arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            c = compare_files(i,pivot)
            if c < 0:
                less.append(i)
            elif c > 0:
                more.append(i)
            else:
               pivotList.append(i)

        less = quicksort_titles(less)
        more = quicksort_titles(more)
        return less + pivotList + more

# The comparison function
def compare_files (page1, page2):
   if page1 == page2:
      return 0
   diffs = [i for i in range(min(len(page1), len(page2))) if page1[i] != page2[i]]
   # Find the first difference index which is an int
   index1 = -1
   for i in diffs:
      try:
         int(page1[i])
         index1 = i
         break
      except ValueError:
         continue

   index2 = -1
   for i in diffs:
      try:
         int(page2[i])
         index2 = i
         break
      except ValueError:
         continue

   if index1 == -1 or index2 == -1:
      return -1 if page1 < page2 else 1

   seq1, seq2 = ""
   while index1 < len(page1) and index2 < len(page2):
      try:
         int(page1[i])
         int(page2[i])
         seq1 += page1[i]
         seq2 += page2[i]
         break
      except ValueError:
         break
   return -1 if int(seq1) < int(seq2) else 1

"""
Pulls the current image as a page
"""

def get_page (filepath, pagenum):
   path = root + '/' + filepath

   if os.path.isdir(path):
      files = sort_titles(os.listdir(path))
      files = pages_cleaner(files)

      image = path + '/' + files[pagenum - 1]
      with open(image, 'rb') as file_:
         page = file_.read()
         return page

   elif os.path.isfile(path):
      filetype = path.split('.')[-1]

      if filetype == 'zip':
         with ZipFile(path) as archive:
            files = sort_titles(archive.namelist())
            files = pages_cleaner(files)

            image = files[pagenum - 1]
            with archive.open(image) as file_:
               page = file_.read()
               return page

      elif filetype == 'rar':
         with rarfile.RarFile(path) as archive:
            files = sort_titles(archive.namelist())
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
