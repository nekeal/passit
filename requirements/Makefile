objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

all: $(outputs)

%.txt: %.in
	pip-compile -v --output-file $@ $<

dev.txt: base.txt
ci.txt: base.txt
deployment.txt: base.txt

check:
	@which pip-compile > /dev/null

clean: check
	- rm *.txt
