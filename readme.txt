How to use:

======FIRST TIME USE======:
1. Make sure Python is already installed on your system
2. Install requirements.txt by typing the following on terminal
    On Windows:
    pip install -r requirements.txt
    On Linux:
    pip3 install -r requirements.txt


======TWITTER CRAWLING=====:
Twitter crawling argument:
On windows:
1. Posting crawling:
	python crawling.py -p -u [username target tanpa @, contoh @jokowi -> jokowi] -c [jumlah yang akan di crawling, maks 3200]
2. Replies crawling:
	python crawling.py -r -i [tweet_id postingan]
3. Hashtag crawling:
	python crawling.py -ht -k [hashtag tanpa #, sementara masih cuman bisa diinputkan 1 dulu]
On Linux:
1. Posting crawling:
	python3 crawling.py -p -u [username target tanpa @, contoh @jokowi -> jokowi] -c [jumlah yang akan di crawling, maks 3200]
2. Replies crawling:
	python3 crawling.py -r -i [tweet_id postingan]
3. Hashtag crawling:
	python3 crawling.py -ht -k [hashtag tanpa # (sementara masih cuman bisa dilakukan input 1 keyword hashtag)]

======OKEZONE CRAWLING======:
(yet to be written)