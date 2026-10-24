FROM crocodilestick/calibre-web-automated:v4.0.8

COPY railway-entrypoint.sh /railway-entrypoint.sh
COPY root/ /
RUN chmod +x /railway-entrypoint.sh /etc/s6-overlay/s6-rc.d/railway-perms/run

EXPOSE 8083
ENTRYPOINT ["/railway-entrypoint.sh"]
