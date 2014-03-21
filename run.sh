#./scripts/vars.sh
#python /arquivos/projeto/workspace/pecbrasil/pec/run.py runserver
git pull
chown politica /home/politica/git/hub/* -R
chgrp politica /home/politica/git/hub/* -R
cd /home/politica/git/hub/pecbrasil
python runcherry.py & 
