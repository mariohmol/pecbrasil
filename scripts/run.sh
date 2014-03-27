cp -rf /home/sisfocus/public_html/ftp2/data/* /home/politica/pecbrasil/data/
python import.py -o runVotacaoCandidato -a P > log.txt
python import.py -o runPontuacao -a P > log.txt
python import.py -o runDespesas -a P > log.txt
python import.py -o runProposicao -a P > log.txt