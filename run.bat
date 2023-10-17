@echo off
:: Navigate to the directory containing qutip.yml
cd /d "%~dp0"
call conda env create -f qutip.yml
call conda activate qutip
python tktest2.py
```