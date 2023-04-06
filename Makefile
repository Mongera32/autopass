default: req vault.csv.cpt

vault.csv.cpt: vault.csv
	$(shell ccencrypt vault.csv)

vault.csv:
	touch vault.csv

req:
	pip install -r requirements.txt
