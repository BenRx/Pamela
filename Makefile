install:
	./install.sh

uninstall:
	./uninstall.sh

check:
	./check.sh

test:
	@echo 'Des tests unitaires ?! LOL !'

clean:
	make uninstall

re:
	make install
