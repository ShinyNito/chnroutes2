produce:
	#git pull
	curl -o chnroutes.txt https://raw.githubusercontent.com/misakaio/chnroutes2/master/chnroutes.txt
	
	python3 produce.py
	# sudo mv routes4.conf /etc/bird/routes4.conf
	# sudo mv routes6.conf /etc/bird/routes6.conf
	# sudo birdc configure
	# sudo birdc6 configure
