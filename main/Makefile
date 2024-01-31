gen:
	python -m PyQt5.uic.pyuic -x gui.ui -o ui_gen.py
	powershell -Command "(gc ui_gen.py) -replace 'files/logo.ico', 'C:/Users/Lab2/Desktop/stand/test_stand/main/files/logo.ico' | Out-File -encoding ASCII ui_gen.py"