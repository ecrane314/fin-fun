#  sudo docker build -t alpine-hello .
#  Uses Dockerfile in . directory to build and works.
#  2022 April 3

FROM alpine:latest


ENTRYPOINT [ "echo" ]
CMD [ "Hello, World!" ]