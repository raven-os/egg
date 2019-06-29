from setuptools import setup

DEPENDENCIES = [
    'six',
    'termcolor',
]

TEST_DEPENDENCIES = [
    'hypothesis',
    'mock',
    'python-Levenshtein',
]

VERSION = '0.1.0'
URL = 'https://github.com/raven-os/egg'


LONG_DESCRIPTION = """
Python Fire is a library for automatically generating command line interfaces
(CLIs) with a single line of code.
It will turn any Python module, class, object, function, etc. (any Python
component will work!) into a CLI. It's called Fire because when you call Fire(),
it fires off your command.
""".strip()

SHORT_DESCRIPTION = """
A library for automatically generating command line interfaces.""".strip()


class CleanCommand(setuptools.Command):
    """
    Custom clean command to tidy up the project root, because even
        python setup.py clean --all
    doesn't remove build/dist and egg-info directories, which can and have caused
    install problems in the past.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='egg',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Grange Benjamin',
    author_email='grange.benjamin@epitech.eu',
    license='Apache Software License',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],

   entry_points={
        'console_scripts': [
            'egg-runtests=egg.tests.runtests:main',
            'egg-exec=egg.test:main',
        ],
    },
#             'gryphon-runtests=gryphon.tests.runtests:main',
#             'gryphon-exec=gryphon.execution.app:main',
#             'gryphon-cli=gryphon.execution.console:main',
#             'gryphon-dashboards=gryphon.dashboards.app:main',

    keywords='command line interface cli python fire interactive bash tool',

    packages=setuptools.find_packages(),
    #packages=['egg', 'egg.gtk', 'egg.ncurses', 'egg.interfaces'],

    include_package_data=True,
    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
    cmdclass={
        'clean': CleanCommand,
    },
)
