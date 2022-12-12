#FROM centos:7
#WORKDIR /data
#ADD nginx-1.20.1.tar.gz /data
#COPY run.sh /run.sh
#RUN yum install gcc gcc-c++ make prce-devel openssl-devel git crontabs -y  && chmod a+x /run.sh \
#  && cd /data/nginx-1.20.1 && useradd www -s /sbin/nologin \
#  && CONFIG="\
#     --prefix=/usr/local/nginx \
#     --with-http_stub_status_module \
#     --with-http_v2_module \
#     --with-http_ssl_module  \
#     --with-http_gzip_static_module \
#     --with-http_realip_module  \
#     --with-http_flv_module \
#     --with-stream \
#     --sbin-path=/usr/sbin/nginx \
#     --modules-path=/usr/lib/nginx/modules \
#     --conf-path=/usr/local/nginx/conf/nginx.conf \
#     --user=www \
#     --group=www \
#      " \
#  && ./configure $CONFIG && make && make install && rm -rf /data/* && yum remove gcc gcc-c++ make -y && yum clean all
#EXPOSE 80
#ENTRYPOINT ["/bin/sh","-c"]
#CMD ["sh /run.sh"]

FROM ubuntu:latest
COPY pull-repo.sh /pull-repo.sh
WORKDIR /
RUN apt update && apt upgrade -y && apt install nginx cron git -y && service cron start && service nginx start \
&& echo '*/5 * * * * root cd /var/www/html && git clone https://github.com/jergt-pro/index.git' >> /etc/crontab
ENTRYPOINT ["/bin/sh","-c"]
CMD ["/pull-repo.sh"]


