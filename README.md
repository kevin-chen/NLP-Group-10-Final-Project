# NLP-Group-10-Final-Project

## NLP

- Pre-Preprocessing
  - Port Stem
  - Stop Words + Remove Punctuation
  - Lower Case Alpha

## Commands
- python3 -m venv env
- source env/bin/activate
- pip3 install -r requirements.txt
- python sandbox.py

## HPC
- Initialize the env

```
## (use venv command to create environment called "venv")
python3 -m venv env
## Inhering all packages
python3 -m venv env --system-site-packages

## activate
source env/bin/activate
## install packages
pip install <package you need>
## restore
pip install -r requirements.txt
```

- Submit batch request

```
sbatch nlp-group10-init.sbatch
squeue -u $USER
tail -3 nlp-group10-init.out
cat nlp-group10-init.out
```

## Issues
- Even though pandas was installed, error says "module not installed"
  - this was because I am running a virtual environment, and have to run python sandbox.py not python3 sandbox.py