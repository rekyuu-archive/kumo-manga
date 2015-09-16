import json, os


ARCHIVES = ['zip', 'rar', '7z']

with open('./config.json', encoding='utf8') as file_:
   config = json.loads(file_.read())
   root = config['root']


"""
Returns a listing of folders and archives
"""

def return_listing (directory = ''):
   if directory == '':
      path = root
   else:
      path = root + '/' + directory

   files = []
   folders = []

   for item in os.listdir(path):

      # If the item is a directory
      if os.path.isdir(path + '/' + item):

         for sub_item in os.listdir(path + '/' + item):

            # If there is a subdirectory
            if os.path.isdir(path + '/' + item + '/' + sub_item):
               if item not in folders:
                  folders.append(item)
                  break

            # Checks to see if this is an archive or a directory
            if os.path.isfile(path + '/' + item + '/' + sub_item):
               file_type = sub_item.split('.')[-1]

               # If there are archives in the directory
               if file_type in ARCHIVES:
                  if item not in folders:
                     folders.append(item)
                     break

               # If there are no archives (usually only images)
               if sub_item == os.listdir(path + '/' + item)[-1]:
                  files.append((item, item))

      # If the item is a file
      elif os.path.isfile(path + '/' + item):
         files.append((item.split('.')[0], item))

   return {"files": sorted(files), "folders": sorted(folders)}
