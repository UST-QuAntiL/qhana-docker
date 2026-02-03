FROM postgres:12

ENV QC_ATLAS_CONTENT_REPOSITORY_URL "https://github.com/UST-QuAntiL/planqk-atlas-content.git"
ENV QC_ATLAS_CONTENT_REPOSITORY_PATH "/var/qc-atlas/testdata"
ENV QC_ATLAS_CONTENT_REPOSITORY_BRANCH "master"
ENV SUBFOLDER_CONTENT_REPO_BACKUP_FILES "example-data/SQL/backup-files"
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_USER postgres
ENV JDBC_DATABASE_PORT 5432
ENV POSTGRES_DB db

# install dependencies (git)
RUN  apt-get update \
  && apt-get update -qq && apt-get install -qqy \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY clone-data-repo.sh clone-data-repo.sh

# if ssh key is set, clone data repo with the sql scripts for initalization and start postgres afterwards
CMD  chmod 700 clone-data-repo.sh && ./clone-data-repo.sh && su postgres -c "/usr/local/bin/docker-entrypoint.sh postgres"
