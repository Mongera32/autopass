default: req vault.csv.cpt

vault.csv.cpt: vault.csv
	$(shell ccencrypt vault.csv)

req:
	pip install -r requirements.txt
