#!/usr/bin/env bash
# ------------------------------------------------------------------
# [Michael J. Davis]
#    setup.sh
#          Setup python's virtualenv, install requirements,
#          and set environment variables with one command.
# ------------------------------------------------------------------

VERSION=0.2.1
# If executing setup.sh from root dir of this repo, you can simply do ```source setup.sh``` without args.
USAGE='Usage: source setup.sh -hv -p "/path/to/python/" -r "repoName" -q "/path/to/repo_root_dir"'

REQ_MAJOR=2
REQ_MINOR=7
REQ_PATCH=9

# --- Option processing --------------------------------------------
while getopts ":v:h:p:r:q:" o; do
    case "${o}" in
      v)
        echo "Version $VERSION"
        return 0;
        ;;
      h)
        echo $USAGE
        return 0;
        ;;
      p)
        PYTHON=$OPTARG
        ;;
      r)
        REQUIRED_VENV=$OPTARG
        ;;
      q)
        REQUIREMENTS_DIR=$OPTARG
        ;;
      ?)
        echo "Unknown option $OPTARG"
        return 0;
        ;;
      :)
        echo "No argument value for option $OPTARG"
        return 0;
        ;;
      *)
        echo $USAGE
        echo "Unknown error while processing options"
        return 0;
        ;;
    esac
  done

# -----------------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
# -----------------------------------------------------------------

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! "$REQUIRED_VENV" ]
then
  REQUIRED_VENV="$( basename "$THIS_DIR" )"
fi

if [ ! "$PYTHON" ]
then
    echo "No python version designated."
    echo "Using machine's default python version"
    PYTHON="$( which python )"
fi

PMAJOR="$( "$PYTHON" -c 'import platform; major, minor, patch = platform.python_version_tuple(); print(major);' )"
PMINOR="$( "$PYTHON" -c 'import platform; major, minor, patch = platform.python_version_tuple(); print(minor);' )"
PPATCH="$( "$PYTHON" -c 'import platform; major, minor, patch = platform.python_version_tuple(); print(patch);' )"

if [[ "$PMAJOR" -eq $REQ_MAJOR ]] && [[ "$PMINOR" -ge $REQ_MINOR ]] && [[ "${PPATCH//[!0-9]/}" -ge $REQ_PATCH ]]
then
    echo "Python version is good enough: $PMAJOR.$PMINOR.$PPATCH."
else
    echo "Python version must be 2.7.9 or greater."
    echo "Yours is $PMAJOR.$PMINOR.$PPATCH :("
    return 1
fi

export VIRTUALENVWRAPPER_PYTHON="$PYTHON"

mkdir -p logs

export WORKON_HOME=~/.virtualenvs

if [ ! -d $HOME/.virtualenvs/ ]
then
  if [ -f $HOME/.venvburrito/startup.sh ]
  then
    if [ ! -f $HOME/.venvburrito/bin/virtualenvwrapper.sh ]
    then
      curl -sL https://bitbucket.org/dhellmann/virtualenvwrapper/raw/5c88ad1fbd749f473784b3346b949fb35d9459a0/virtualenvwrapper.sh --output $HOME/.venvburrito/bin/virtualenvwrapper.sh
    fi
    source $HOME/.venvburrito/startup.sh 2> /dev/null
  else
    if [ -f /usr/local/bin/virtualenvwrapper.sh ]
    then
      source /usr/local/bin/virtualenvwrapper.sh 2> /dev/null
    else
      curl -sL https://raw.githubusercontent.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL
      curl -sL https://bitbucket.org/dhellmann/virtualenvwrapper/raw/5c88ad1fbd749f473784b3346b949fb35d9459a0/virtualenvwrapper.sh --output $HOME/.venvburrito/bin/virtualenvwrapper.sh
      source $HOME/.venvburrito/startup.sh 2> /dev/null
    fi
  fi
else
  if [ ! -f $HOME/.virtualenvs/virtualenvwrapper.sh ]
  then
    curl -sL https://bitbucket.org/dhellmann/virtualenvwrapper/raw/5c88ad1fbd749f473784b3346b949fb35d9459a0/virtualenvwrapper.sh --output $HOME/.virtualenvs/virtualenvwrapper.sh
  fi
  source $HOME/.virtualenvs/virtualenvwrapper.sh 2> /dev/null
fi

export WORKON_HOME=~/.virtualenvs

if [ ! -d ~/.virtualenvs/"$REQUIRED_VENV" ]
then
  mkvirtualenv "$REQUIRED_VENV" --python="$PYTHON"
fi


if [ ! "$REQUIREMENTS_DIR" ]
then
  REQUIREMENTS_DIR="."
fi

PYTHONHOME=~/.virtualenvs/"$REQUIRED_VENV"/
export PYTHONHOME="$PYTHONHOME"

# Support both unix and Windows :hankey:
if [ -d $PYTHONHOME/bin/ ]
then
  source $PYTHONHOME/bin/activate
else
  source $PYTHONHOME/Scripts/activate
fi

export PYTHONPATH="$THIS_DIR":$HOME/.virtualenvs/"$REQUIRED_VENV"/lib/python2.7/site-packages:"$REQUIREMENTS_DIR"

if [ -d ~/.virtualenvs/"$REQUIRED_VENV"/bin/ ]
then
  ~/.virtualenvs/"$REQUIRED_VENV"/bin/pip install -r "$REQUIREMENTS_DIR"/requirements.txt
else
  ~/.virtualenvs/"$REQUIRED_VENV"/Scripts/pip install -r "$REQUIREMENTS_DIR"/requirements.txt
fi
