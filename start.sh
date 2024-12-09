echo "Criando atalho e inserindo no bashrc"
echo alias celeryShell="'celery shell -A src.worker'" >> ~/.bashrc
echo alias pytestV="'pytest -v'" >> ~/.bashrc
echo alias coverageAll="'coverage run --rcfile=./.coveragerc -m unittest -v -b'" >> ~/.bashrc
echo alias coverageRM="'coverage report --rcfile=./.coveragerc -m'" >> ~/.bashrc
echo alias coverageHTML="'coverage html'" >> ~/.bashrc
echo alias pylintALL="'pylint --fail-under=10.00 src/ -j 0'" >> ~/.bashrc
echo alias pylint-fail-underALL="'pylint-fail-under --fail_under 10.00 src/ -j 0'" >> ~/.bashrc
echo "Apagando arquivo celerybeat-schedule e celerybeat.pid antes de iniciar"
rm celerybeat-schedule
rm celerybeat.pid
chmod +x /code/scripts/*.sh
cp /code/scripts/*.sh  /usr/local/bin/
echo "Iniciando worker habilitados em Procfile.dev"
honcho -f Procfile.dev start