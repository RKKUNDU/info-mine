#!/bin/bash

# get the source code
wget https://github.com/RKKUNDU/info-mine/archive/main.zip

# unzip
unzip main.zip

# remove the zip after extraction
rm main.zip

# install python
sudo apt-get install python3

# install packages 
pip3 install cryptography==2.8
pip3 install tabulate==0.8.7
pip3 install requests==2.22.0
pip3 install beautifulsoup4==4.9.3

# create infomine executable
echo "#!/bin/bash
cd $(pwd)/info-mine-main/
python3 parser.py \${@}" > infomine

# add permission
chmod +x infomine

# move it to bin directory
sudo mv infomine /bin/infomine
