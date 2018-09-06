PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH=${PYTHONPATH}:${PWD}
export PATH=${PATH}:${PWD}/scripts
