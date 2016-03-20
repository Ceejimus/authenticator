FROM postgres

RUN groupadd -r postgres \
	&& useradd -r -g postgres postgres

RUN mkdir -p /data/pgdata \
	&& chown -R postgres:postgres /data/pgdata

VOLUME /data/pgdata

USER postgres

CMD ["echo", "Data Container for Postgres"]