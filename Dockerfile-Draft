#
# docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --name chromium eac-chrome
#
#
#
#

FROM debian:stable

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    xserver-xorg \
    x11-xserver-utils \
    xinit \
    openbox

RUN apt-get install -y --no-install-recommends chromium

RUN groupadd -r chromium && useradd -r -g chromium -G audio,video chromium

# Need this --ERROR:zygote_host_impl_linux.cc(90)] Running as root without \
#  --no-sandbox is not supported. See https://crbug.com/638180.
USER chromium

ENTRYPOINT [ "chromium" ]
CMD [ "--no-sandbox" ]