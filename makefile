install:
	pip install -r requirements.txt
test:
	pytest
train:
	python src/train.py
run:
	python app.py
clean:
	rm-rf--pycache--