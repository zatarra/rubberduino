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

## Adjust the symbol mapping

Currently this is adjusted to PT keyboards. You can try to create a custom map that suits you by checking which numbers give you the desired symbols. The quick and dirty way of doing it is to use a small arduino sketch that will print out the corresponding symbols of each number. Please check the symbols_mapper.txt or just load an arduino with the following sketch:

```
#include <Keyboard.h>
// Rubber ducky script converter developed by: David Gouveia <david.gouveia [_at_] gmail.com>
// https://www.davidgouveia.net
// Basic Symbol Mapping application. This will allow you to check which symbols can be found on each number

void setup(){
  Keyboard.begin();
  delay(5000);
  for ( int i=0; i < 200; i++ )
  {
    Keyboard.print(i);
    Keyboard.print(" maps to ");
    Keyboard.write(i);
    Keyboard.print( "\n" );
  }

  Keyboard.end();
}


void loop(){}
```

After uploading the sketch, you have five seconds to point the cursor to a text editor tool. It will start showing you symbols and their assigned number. Use this to build a new symbol map. 


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

[MIT](LICENSE) 2016 David Gouveia

[travis-image]: https://travis-ci.org/zatarra/rubberduino.svg?branch=master
[travis-url]: https://travis-ci.org/zatarra/rubberduino
[coveralls-image]: https://coveralls.io/repos/zatarra/rubberduino/badge.svg
[coveralls-url]: https://coveralls.io/r/zatarra/rubberduino
