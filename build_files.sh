# build_files.sh
apt-get install python3-venv
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput