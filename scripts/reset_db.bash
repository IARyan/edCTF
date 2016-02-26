#!/bin/bash
# Resets the edCTF database
# Used within the DEVELOPMENT environment.

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# stop apache
sudo /usr/sbin/apachectl stop

# drop database
cd ${EDCTF_DJANGO} \
  && sudo python -c "import database; database.delete_all_ctfs()"
sudo -u postgres psql -c "DROP DATABASE ${EDCTF_DATABASE};"


# remove migration files
find ${EDCTF_DJANGO}/api/migrations/ -type f -not -name '__init__.py' -and -not -name '.gitignore' -exec rm {} +

# regenerate database
${EDCTF_SCRIPTS}/build_backend.bash

# restart service
${EDCTF_SCRIPTS}/start.bash
