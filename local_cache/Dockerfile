FROM ubuntu:18.04
RUN sed -i 's/http:\/\/.*.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/' /etc/apt/sources.list
RUN apt-get update && \
    apt-get install apt-cacher-ng -y && \
    ln -sf /dev/stdout /var/log/apt-cacher-ng/apt-cacher.log && \
    ln -sf /dev/stderr /var/log/apt-cacher-ng/apt-cacher.err && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*
COPY acng.conf /etc/apt-cacher-ng/acng.conf
EXPOSE 80
VOLUME ["/var/cache/apt-cacher-ng"]
ENTRYPOINT ["/usr/sbin/apt-cacher-ng"]
CMD ["-c","/etc/apt-cacher-ng"]
