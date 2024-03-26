import os
from setuptools import setup

# README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-mailman3-web>`_.
"""

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='uwtheme',
    version='0.1',
    packages=['uwtheme'],
    include_package_data=True,
    install_requires=[
        'Django~=3.2',
        'django-allauth>=0.56',
        'django-compressor==2.4.1',
        'django-mailman3==1.3.11',
        'djangorestframework==3.15.0',
        'HyperKitty==1.3.8',
        'mailmanclient',
        'postorius==1.3.10',
        'lxml==4.9.4',
        'whoosh',
        'UW-Django-SAML2~=1.6',
        'uw_list_manager @ git+https://github.com/uw-it-aca/uw-list-manager@develop#egg=uw-list-manager',
    ],
    license='Apache License, Version 2.0',  # example license
    description='UW theme for mailman 3',
    long_description=README,
    url='https://github.com/uw-it-aca/uw-mailman3-web',
    author='"UW-IT AXDD"',
    author_email='aca-it@uw.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
