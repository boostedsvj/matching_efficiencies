Mini repository to calculate MC matching efficiencies and genjet pT > 375 GeV efficiencies for the boosted SVJ analysis.

# Submitting jobs

```
qondor-submit submit_gen_jobs.py
```

When jobs are finished, tar up the `err_*` files:

```
tar cvf matching_eff_job_logs_<date>.tar <job_directory>/err_*.txt
```

For a precalculated tarball:

```
xrdcp root://cmseos.fnal.gov//store/user/lpcdarkqcd/boosted/efficiencies/matching_eff_job_logs_Oct12.tar .
```

# Using this repo

See the [notebook](fit.ipynb)
