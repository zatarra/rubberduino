[![Build status][travis-image]][travis-url] 
[![Coverage percentage][coveralls-image]][coveralls-url]

# rubberduino

Tool to convert Rubber Ducky scripts to arduino compatible code.

## Requirements

- Python 2.7.9+

## Install

```
pip install git@github.com:zatarra/rubberduino.git#egg=rubberduino
```

## Develop

This package comes with a setup.sh script which swiftly
creates a virtualenv and installs dependencies from requirements.txt
without the hassle of virtualenv wrapper:

```
. ./setup.sh -p python2.7.9
```

## Test

```
py.test -v -s --cov-report term-missing --cov=rubberduino -r w tests
```

## License

[MIT](LICENSE) 2016 zatarra

[travis-image]: https://travis-ci.org/zatarra/rubberduino.svg?branch=master
[travis-url]: https://travis-ci.org/zatarra/rubberduino
[coveralls-image]: https://coveralls.io/repos/zatarra/rubberduino/badge.svg
[coveralls-url]: https://coveralls.io/r/zatarra/rubberduino
