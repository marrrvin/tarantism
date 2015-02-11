
from setuptools import setup
from setuptools import find_packages


with open('README.md') as fp:
    long_description = fp.readline()


setup(
    name='tarantism',
    description='',
    long_description=long_description,
    version='0.2',
    url='https://gitlab.corp.mail.ru/target-web/tarantism',
    author='Sergei Orlov',
    author_email='sergey.orlov@corp.mail.ru',
    packages=find_packages(exclude=('tests', 'tests.contrib')),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
