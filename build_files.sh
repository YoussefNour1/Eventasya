# build_files.sh
sudo apt install default-libmysqlclient-dev
pip install -r requirements.txt
python manage.py collectstatic --noinput
