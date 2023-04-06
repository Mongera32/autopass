COMMAND = $(ccencrypt vault.csv)

default: requirements, vault.csv.cpt

vault.csv.cpt: vault.csv
  $(shell COMMAND)

requirements:
  pip install -r requirements.txt
