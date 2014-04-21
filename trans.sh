pybabel -v extract -F babel.cfg -o messages.pot ./
cp messages.pot ./pecbrasil/translations
pybabel update -i messages.pot -d pecbrasil/translations
cd pecbrasil
pybabel compile -f -d ./translations
