FROM archlinux

# Dependencies
RUN pacman --noconfirm -Syyu
RUN pacman --noconfirm -S base-devel git pyenv

# Setup Python 3.8
RUN pyenv install 3.8 && \
    pyenv global 3.8 && \
    ln -s $(dirname $(pyenv which python)) /pybin
ENV PATH="${PATH}:/pybin"

# Install (de)compilation tools
RUN pip install pyinstaller decompyle3 uncompyle6
WORKDIR /home
RUN git clone https://github.com/extremecoders-re/pyinstxtractor && chmod -R 777 /home

# Extract trigger_cal binary
COPY ./trigger_cal ./
RUN python ./pyinstxtractor/pyinstxtractor.py ./trigger_cal

# Set up files for building
RUN mkdir -p /app && cp -r /home/trigger_cal_extracted/PYZ-00.pyz_extracted/{controller_if.pyc,hid_dev_mgr.pyc,valve_message_handler.pyc,hid} /app
COPY ./src/overwrite_trigger_cal.py /app/

WORKDIR /

CMD ["pyinstaller", "-F", "/app/overwrite_trigger_cal.py", "--distpath", "/app/dist"] 