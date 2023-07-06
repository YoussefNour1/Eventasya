# build_files.sh
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput