#required to solve building issues

#pip install cython
#pip install pybind11
#pip install cppimport

# remove old conda env
conda env remove -n "InnAlyze"
rm -rf /opt/conda/envs/InnAlyze

# create conda env, and possibly update some packages in the cache
conda env create -f ./environment.yml

# reload .bashrc
. /root/.bashrc

## install sentry-sdk on prod, and skip on dev and local machines
#if [ -z "$PRD_MACHINE" ]; then
#  echo "PRD_MACHINE variable is not set, skipping sentry-sdk installation"
#else
#  pip install sentry-sdk==1.19.1
#fi

#pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@v0.6#egg=detectron2"
#pip install httpcore==0.9.1
#pip install httpx==0.13.3
# launch api
alembic upgrade head
python -m uvicorn main:app --reload --port 8008 --host 0.0.0.0
