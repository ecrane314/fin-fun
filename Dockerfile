#  sudo docker build -t alpine-hello .
#  Uses Dockerfile in . directory to build and works.
#  2022 April 3


#FROM alpine:latest  
#--per research, NOT very compatible with python. Uses musl instead of glibc, latter of which is one to which most wheels are compiled.

FROM debian:11
#best for python, apparently. Comes with it. Using versioned vs latest for safety. About ~50MB, seems good

#FROM python:slim etc 
#--NOTE these images are debian based AND created by docker, not by python people. Deminishes added value.


RUN apt-get update && apt-get install -y \
   --no-install-recommends \
    git
#    xserver-xorg \
#    x11-xserver-utils \
#    xinit \
#    openbox
#

# Need this --ERROR:zygote_host_impl_linux.cc(90)] Running as root without \
#  --no-sandbox is not supported. See https://crbug.com/638180.
USER chromium

ENTRYPOINT [ "echo" ]
CMD [ "Hello, World!" ]

#RUN apt-get install -y --no-install-recommends chromium
#
#RUN groupadd -r chromium && useradd -r -g chromium -G audio,video chromium

#ENTRYPOINT [ "chromium" ]
#CMD [ "--no-sandbox" ]
#
# Run and enter the container, not sure if this works
# docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --name chromium eac-chrome