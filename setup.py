
from setuptools import setup
from setuptools import find_packages


with open('README.rst') as fp:
    long_description = fp.readline()

with open('requirements.txt') as fp:
    requirements = [req.strip() for req in fp.readlines() if not req.startswith('--')]


setup(
    name='tarantism',
    description='',
    long_description=long_description,
    version='0.1',
    url='http://github.com/marrrvin/tarantism/',
    author='Sergey Orlov',
    author_email='foobar@list.ru',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
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
