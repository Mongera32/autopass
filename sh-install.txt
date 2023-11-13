# Updating apt-get and installing linux dependencies
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install ccrypt
# Installing Python dependencies
pip install -r requirements.txt
# Creating Shell script
echo "python3 `echo $PWD`/main.py \$1 \$2 \$3 \$4 \$5" > vault
chmod u+x vault
sudo mv vault /usr/local/bin
