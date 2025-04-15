snapcraft:
	snapcraft --verbosity=trace

build-deb:
	dpkg-source --build .
	sudo pbuilder --build ../*.dsc
	mkdir -p deb
	cp -vR /var/cache/pbuilder/result/cubetimer* deb/

	
