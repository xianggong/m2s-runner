ROOT = $(PWD)/..
M2S_ROOT = $(ROOT)/multi2sim
M2S = $(M2S_ROOT)/bin/m2s
BENCH_DIR = $(ROOT)/benchmark
CONFIG_DIR = $(ROOT)/config

all: gen

gen:
	if [ -a $(BENCH_DIR) ]; then make -C ../benchmark ini; fi;
	if [ -a $(BENCH_DIR) ]; then find $(BENCH_DIR) -iname "benchmark.ini" -exec cat {} \; > benchmark.ini; fi;
	if [ -a $(CONFIG_DIR) ]; then find $(CONFIG_DIR) -iname 'si-config' > si-config; fi;
	if [ -e si-config ] ; then sed -i -e 's/^/ --si-config /' si-config; fi;
	if [ -a $(CONFIG_DIR) ]; then find $(CONFIG_DIR) -iname 'mem-config' > mem-config; fi;
	if [ -e mem-config ]; then sed -i -e 's/^/ --mem-config /' mem-config; fi;
	if [ -e si-config ] && [ -e mem-config ]; then paste -d " " si-config mem-config > configs; fi;
	if [ -e si-config ] && [ -e mem-config ]; then rm -f si-config mem-config; fi;

condor: gen
	if [ -e benchmark.ini ] && [ -e configs ]; then echo "Executable = $(M2S)" > submit; fi;
	if [ -e benchmark.ini ] && [ -e configs ]; then python gencondor.py benchmark.ini configs 2>&1 >> submit; fi;

run: condor
	condor_submit submit

analyze:
	echo 'name,cycle,passed' > result.csv
	ls -v *.err | xargs grep 'Cycles =' | sed -n 'n;p;' | sed 's/\./ /g' | awk '{print $$1","$$NF}' 2>&1 > cycles
	ls -v *.out | xargs grep 'Passed' | sed 's/:/ /g' | awk '{print $$NF}'> verification
	paste -d ',' cycles verification >> result.csv

clean:
	rm -f mem-config si-config configs benchmark.ini submit cycles verification *.out *.log *.err *.csv
