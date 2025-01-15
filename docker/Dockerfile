FROM continuumio/anaconda3:latest

RUN apt update -y && apt upgrade -y
RUN apt install -y build-essential
# conda init bash without restarting session
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> "/root/.bashrc"

# set lamdai-api env the default for new bash sessions
RUN echo "conda activate InnAlyze" >> "/root/.bashrc"
