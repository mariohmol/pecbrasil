'cp' -rf /home/sisfocus/public_html/ftp2/data/* /home/politica/pecbrasil/data/
#'cp' -rf /home/peclube/git/pecbrasil/data/data/* /home/politica/pecbrasil/data/
#python import.py -o runCandidaturas -a P > log.txt
#python import.py -o runVotacaoCandidato -a P > log.txt
python import.py -o runPontuacao -a P > log.txt
python import.py -o runDespesas -a P > log.txt
python import.py -o runProposicao -a P > log.txt
python import.py -o runProposicaoAcao -a P > log.txt
python import.py -o runVotacaoProposicao -a P > log.txt
