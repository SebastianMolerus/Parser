:: removing previous coverage output
rmdir /s /q "..\htmlcov"

:: install coverage package
python install_coverage.py

:: run coverage & generate html
cd ".."
coverage run -m unittest discover -p "*_test.py"
coverage html

:: open report
cd "htmlcov"
start index.html

PAUSE