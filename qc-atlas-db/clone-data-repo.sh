#!/bin/bash
# If the content repo is already mounted locally, use it without SSH.
if [ -d "${QC_ATLAS_CONTENT_REPOSITORY_PATH}/${SUBFOLDER_CONTENT_REPO_BACKUP_FILES}" ]; then
    echo "local content repo detected, initializing db from local files"
    cp ${QC_ATLAS_CONTENT_REPOSITORY_PATH}/${SUBFOLDER_CONTENT_REPO_BACKUP_FILES}/* /docker-entrypoint-initdb.d/
    exit 0
fi
# if ssh key is not empty, init the db with data:
echo "checking if ssh key for the atlas content repo is present"
FILE=/run/secrets/ssh_secret
if test -f "$FILE"; then
    echo "ssh key present"
    # add ssh key and add github as known host
    mkdir /root/.ssh/ && cp /run/secrets/ssh_secret /root/.ssh/id_rsa
    chmod 400 /root/.ssh/id_rsa && ssh-keyscan github.com >> /root/.ssh/known_hosts
else
    echo "ssh key not present, proceeding without it"
fi
# clone repo and copy the file with the sql statements to the folder that is executed on startup of the postgres db
git clone --single-branch --branch ${QC_ATLAS_CONTENT_REPOSITORY_BRANCH} ${QC_ATLAS_CONTENT_REPOSITORY_URL} ${QC_ATLAS_CONTENT_REPOSITORY_PATH}
if [ -d "${QC_ATLAS_CONTENT_REPOSITORY_PATH}/${SUBFOLDER_CONTENT_REPO_BACKUP_FILES}" ]; then
    cp ${QC_ATLAS_CONTENT_REPOSITORY_PATH}/${SUBFOLDER_CONTENT_REPO_BACKUP_FILES}/* /docker-entrypoint-initdb.d/
else
    echo "unable to find specified directory with example data in the repository"
fi
