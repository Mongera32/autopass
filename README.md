# Autopass

DISCLAIMER:
The author of this project makes no guarantees whatsoever about this package and takes no responsability for any loss or theft of data stored by it.

# Installation

sudo apt-get update

sudo apt-get install ccrypt

pip install -r requirements.txt

echo "python3 `echo $PWD`/main.py \$1 \$2 \$3 \$4 \$5" > vault

chmod u+x vault

sudo mv vault /usr/local/bin
