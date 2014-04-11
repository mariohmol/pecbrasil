#./scripts/vars.sh
#python /arquivos/projeto/workspace/pecbrasil/pec/run.py runserver
git pull

chown politica /home/politica/pecbrasil/* -R
chgrp politica /home/politica/pecbrasil/* -R
cd /home/politica/pecbrasil
pkill -f runcherry
rm site.log
python runcherry.py & 
