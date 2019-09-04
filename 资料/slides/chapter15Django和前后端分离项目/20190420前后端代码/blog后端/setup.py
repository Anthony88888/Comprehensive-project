
from distutils.core import setup
import glob


setup(name='blog',
      version='1.0',
      description='blog projects',
      author='wayne',
      author_email='wayne@magedu.com',
      url='https://www.magedu.com/python',
      packages=['blog', 'post', 'user', 'user.templatetags'],
      data_files = glob.glob('templates/*.html') + ['requirements'],
      py_modules=['manage']
     )