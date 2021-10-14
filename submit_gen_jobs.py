"""# submit
for mz in [100.+10.*i for i in range(51)]:
    submit(mz=mz, mdark=10., rinv=0.3)
"""# endsubmit

import qondor, seutils, os.path as osp

cmssw = qondor.svj.init_cmssw(
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/svjproduction-tarballs/CMSSW_10_2_21_latest_el7_gen_2018.tar.gz'
    )

physics = qondor.svj.Physics({
    'year' : 2018,
    'mz' : qondor.scope.mz,
    'mdark' : qondor.scope.mdark,
    'rinv' : qondor.scope.rinv,
    'mingenjetpt' : 375.,
    'max_events' : 50000,
    'part' : 1
    })

cmssw.download_madgraph_tarball(physics)
expected_outfile = cmssw.run_step('step0_GRIDPACK', 'step1_LHE-GEN', physics)

if not qondor.BATCHMODE: seutils.drymode()
seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/lpcdarkqcd/boosted/efficiencies/'
    'genjetpt375_{date}_mz{mz:.0f}_mdark{mdark:.0f}_rinv{rinv}.root'
    .format(
        date = qondor.get_submission_timestr(),
        **physics
        )
    ) 
