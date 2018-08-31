from setuptools import setup, find_packages


setup(
    name='rc_database_server',
    version='0.0.1',
    description='Simple database server for RC pairing interview',
    author="Yuriy Bash",
    author_email='yuriybash@gmail.com',
    url='https://github.com/yuriybash/rc_database_server',
    platforms=['Any'],
    tests_require=[
        'mock',
    ],
    test_suite='tests',
    packages=find_packages(exclude=('tests', ))
)
