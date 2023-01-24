@ECHO OFF
if not exist "pyenv" (
	py -m venv pyenv
) 

.\pyenv\Scripts\activate