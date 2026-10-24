FROM crocodilestick/calibre-web-automated:v4.0.8

COPY railway-entrypoint.sh /railway-entrypoint.sh
RUN chmod +x /railway-entrypoint.sh

EXPOSE 8083
ENTRYPOINT ["/railway-entrypoint.sh"]
