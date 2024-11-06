## Additinal test scripts
This folder contains some additional test scripts


### run_steady_state_combinations

Simple command line tool that runs steady state computations over a file or all COPASI / SBML files in a given path. For that all permutations of target criteria and Forward / Newton / Both will be computed. The resulting file will contain all generated models the log files created and a `steady-state-results.html` file that displays the results including copasi-urls to the generated models

All command line options

```bash
python run_steady_state_combinations.py --help
usage: run_steady_state_combinations.py [-h] [--output_dir OUTPUT_DIR] [--max_time MAX_TIME] [--copasi_se COPASI_SE] path

Run steady state combinations for COPASI models.

positional arguments:
  path                  Path to the file or directory containing COPASI models.

options:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Output directory for results (default ./out/).
  --max_time MAX_TIME   Maximum time for the run with CopasiSE (default 20 seconds).
  --copasi_se COPASI_SE
                        Path to the CopasiSE executable. (default CopasiSE)
```

