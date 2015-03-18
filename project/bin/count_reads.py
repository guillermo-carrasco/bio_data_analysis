#! /usr/bin/env python

import contextlib
import glob
import os

@contextlib.contextmanager
def chdir(new_dir):
    """Context manager to temporarily change to a new directory.
    """
    cur_dir = os.getcwd()
    # This is weird behavior. I'm removing and and we'll see if anything breaks.
    #safe_makedir(new_dir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(cur_dir)

projects = glob.glob('[A-Z].*')
read_count = {project: {} for project in projects}

for project in projects:
    with chdir(project):
        # There are two different sample naming conventoins, this piece deals with
        # that to build a set of samples
        samples = glob.glob('P[0-9]*')
        sample_tpye = 'A'
        if not samples:
            samples = glob.glob('*P[0-9]*')
            sample_tpye = 'B'
        for sample in samples:
            if not os.path.isdir(sample):
                continue
            print "Processing sample {} for project {}...".format(sample, project)
            with chdir(sample):
                if sample_tpye == 'A':
                    sample_id = '_'.join(sample.split('_')[0:2])
                else:
                    sample_id = '_'.join(sample.split('_')[-3:-1])
                if not read_count[project].get(sample_id):
                    read_count[project][sample_id] = {}
                # Read FastQC data
                with open('FastQC/{}_trimmed_fastqc/fastqc_data.txt'.format(sample), 'r') as f:
                    l = f.readline()
                    while l.find('#Length') < 0:
                        l = f.readline()
                    count_line = f.readline()
                    while not count_line.find('>>') == 0:
                        length, count = count_line.split()
                        if not read_count[project][sample_id].has_key(length):
                            read_count[project][sample_id][length] = float(count)
                        else:
                            read_count[project][sample_id][length] += float(count)
                        count_line = f.readline()

        for _sample in read_count[project].keys():
            with open('{}_length_distribution.txt'.format(_sample), 'w') as f:
                for length, count in sorted(read_count[project][_sample].iteritems(), key=lambda x: x[0]):
                    f.write(str(length) + '\t' + str(count) + '\n')
