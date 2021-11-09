"""
Description
"""

import tarfile, os, os.path as osp, sys, re, numpy as np
from time import strftime

genjetptfilter_pat = re.compile(
    r'GenJetPTFilter efficiency: nPass: (\d+)\s*nFail: (\d+)'
    )
mz_pat = re.compile(r'mMediator=(\d+)')
nevents_pat = re.compile(r'maxEvents=(\d+)')

def read_tar(infile):
    print(f'Reading {infile}')
    n_genjetpt_pass = {}
    n_genjetpt_fail = {}
    n_submitted = {}
    with tarfile.open(infile) as tar:
        for member in tar.getmembers():
            if not osp.basename(member.name).startswith('err'): continue
            print(f'  Reading {member.name}')
            with tar.extractfile(member) as f:
                content = f.read().decode()

            try:
                mz = int(mz_pat.search(content).group(1))
                n_genjetpt_pass.setdefault(mz, 0)
                n_genjetpt_fail.setdefault(mz, 0)
                n_submitted.setdefault(mz, 0)

                n_submitted[mz] += int(nevents_pat.search(content).group(1))
                genjetptfilter_match = genjetptfilter_pat.search(content)
                n_genjetpt_pass[mz] += int(genjetptfilter_match.group(1))
                n_genjetpt_fail[mz] += int(genjetptfilter_match.group(2))
            except AttributeError:
                print('    Failed')
                continue

    mzs = np.array(list(sorted(n_submitted.keys())))
    n_genjetpt_pass = np.array([n_genjetpt_pass[mz] for mz in mzs])
    n_genjetpt_fail = np.array([n_genjetpt_fail[mz] for mz in mzs])
    n_submitted = np.array([n_submitted[mz] for mz in mzs])

    n_total = n_genjetpt_fail + n_genjetpt_pass
    matching_eff = n_total / n_submitted
    genjetpt_eff = n_genjetpt_pass / n_total
    return mzs, n_genjetpt_pass, n_genjetpt_fail, n_submitted, matching_eff, genjetpt_eff

def print_arrays(*args):
    print(
        f'{"mz (GeV)":>9}'
        f' {"n_submitted":>13} {"pass_genjetpt":>13} {"fail_genjetpt":>13} '
        f' {"matching_eff":>13} {"genjetpt_eff":>13}'
        )
    for mz, passed, failed, submitted, match_eff, genjetpt_eff in zip(*args):
        print(f'{mz:9.0f} {submitted:13} {passed:13} {failed:13} {match_eff:13.7f} {genjetpt_eff:13.7f}')

def dev():
    print_arrays(*read_tar('matching_eff_job_logs_Oct12.tar'))


def main():
    dev()



if __name__ == '__main__':
    main()