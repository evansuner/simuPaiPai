FROM node:16-alpine

WORKDIR /app

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
RUN npm config set unsafe-perm true \
	&& npm install -g egg-scripts \
	&& apk add --no-cache tzdata \
	&& ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
	&& echo 'Asia/Shanghai' >/etc/timezone
COPY . /app/
RUN npm i --registry=https://registry.npmmirror.com
EXPOSE 7799
CMD [ "npm", "start" ]