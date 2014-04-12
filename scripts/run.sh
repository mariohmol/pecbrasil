cp -rf /home/sisfocus/public_html/ftp2/data/* /home/politica/pecbrasil/data/
python import.py -o runCandidaturas -a P > log.txt
python import.py -o runVotacaoCandidato -a P > log.txt
python import.py -o runPontuacao -a P > log.txt
python import.py -o runDespesas -a P > log.txt
python import.py -o runProposicao -a P > log.txt
<<<<<<< HEAD
=======
python import.py -o runProposicaoAcao -a P > log.txt
python import.py -o runVotacaoProposicao -a P > log.txt
>>>>>>> 4fc27554c9119b4f23e404b29fe6a2d9c0097fec
