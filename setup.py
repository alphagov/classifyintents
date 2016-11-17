from setuptools import setup, find_packages

setup(name='classify',
      version='0.4.2',
      description='Package supporting classification of the GOV.UK intents survey',
      url='http://github.com/ivyleavedtoadflax/classify',
      author='Matthew Upson',
      packages = find_packages(exclude=['tests']),
      author_email='matthew.a.upson@gmail.com',
      license='OGL',
      zip_safe=False,
      install_requires=['pandas==','numpy==']a
      )
