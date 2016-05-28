""" condor submit script generator """
import argparse
import os
import re


def readline(file):
    """Get snippet source string"""
    current_file_dir = os.path.dirname(__file__)
    absolute_path = os.path.join(current_file_dir, file)
    with open(absolute_path) as src:
        return src.readlines()


def main():
    """ Condor submit script generator """
    parser = argparse.ArgumentParser(
        description='Condor submit script generator')
    parser.add_argument('bench', metavar='bench', nargs=1,
                        help='Benchmark launch files')
    parser.add_argument('m2sconf', metavar='m2sconf', nargs=1,
                        help='Multi2Sim config files')
    args = parser.parse_args()

    bench = readline(args.bench[0])
    m2sconf = readline(args.m2sconf[0])
    redirect = ' 2>&1 | grep -m 2 \'Cycles =\' | tail -n1 > '
 
    for config in m2sconf:
    	for line in bench:
		pat_conf = re.compile(ur'/(\w+)/si-config')
		conf = re.search(pat_conf, config).group(1)
		pat_name = re.compile(ur'(\w+).bin')
		name = re.search(pat_name, line).group(1)
		pat_len = re.compile(ur'-x\s(\d+)')
		len = re.search(pat_len, line)
		output = conf + "_" + name
		if len:
			output += "_" + len.group(1)
		src = config.replace("\n"," ") + line.replace("\n", " ")
		#src = src.replace("\n"," ") + redirect + output
		print "Arguments = --si-sim detailed " + src
		print "Error = " + output + ".err"
		print "Output = " + output + ".out"
		print "Log = " + output + ".log"
		print "Queue\n"

if __name__ == '__main__':
    main()

