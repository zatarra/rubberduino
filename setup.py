from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="rubberduino",
    version='0.1',
    description='Tool to convert Rubber Ducky scripts to arduino compatible code.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/zatarra/rubberduino',
    author='zatarra',
    author_email='david.gouveia@gmail.com',
    license="MIT",
    packages=["rubberduino"],
    install_requires=[
        'markdown',
    ],
    scripts=["rubberduino-convert"]
)
