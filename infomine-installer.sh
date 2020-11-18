#!/bin/bash

wget https://github.com/RKKUNDU/info-mine/archive/main.zip

unzip main.zip

rm main.zip

# install python
sudo apt-get install python3

# install packages 
pip3 install cryptography==2.8
pip3 install tabulate==0.8.7
pip3 install requests==2.22.0
pip3 install beautifulsoup4==4.9.3
 

#echo "Source Codes are currently present in $(pwd)/info-mine-main directory. Do you want to move the source code to somewhere else? [y/n]"

#read 

echo "#!/bin/bash
cd $(pwd)/info-mine-main/
python3 parser.py \${@}" > infomine

chmod +x infomine

sudo mv infomine /bin/infomine
