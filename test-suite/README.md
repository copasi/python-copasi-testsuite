
# COPASI Testsuite

### Structure
The testsuite consists of a folder containing individual tests in subfolders. Each test is specified by a `settings.txt` file along with all results necessary. The name of the subfolder is uniquely identified by the folder name. 

## settings.txt
This file controls what the test is about to do. It is a plain text file of key value pairs separated by colon. Additionally comments can be included in the file, by using the `#` symbol. After that symbol the rest of the line is ignored.  

The following special keywords are recognized by the runner: 

* `task`: this determines what is to be done in the test case. Supported at this point are:
 
	* Steady-State
	* Time-Course
	* Scan
	* Elementary Flux Modes
	* Optimization
	* Parameter Estimation
	* Metabolic Control Analysis
	* Lyapunov Exponents
	* Time Scale Separation Analysis
	* Sensitivities
	* Moieties
	* Cross Section
	* Linear Noise Approximation
	* as-is
	* sbml export
	
* `location`: this can be a relative path to either a model file or a directory of model files. If relative the absolute location of the path will be calculated by applying the relative path from within the test folder

* `filter`: optional field, if specified contains a regular expression that allows to filter the model files in a specified directory. For example in case the location specifies the curated directory of the biomodels release, a filter of `BIOMD000000000[0-5]` would only run over the model files 0 to 6.   

* `format`: the format of the model file(s) either SBML or COPASI

* `result`: a description of how the result of the run should be compared. Possible options are: 


	* `report`: the output should be the default report of the task
	* `copmpare`: perform comparison even if an exception occurred before (and is ignored)
	* `run-only`: to be chosen if the result of the task run is not to be evaluated, just whether a task succeeds or not
	* `xml equivalence`: xml comparison disregarding xml comments, time stamps, keys and the like

	
* `result_file`: by default, the expected files are assumed to be in the form: `report-{test id}-{model name}.txt`, so for example `report-00007-BIOMD0000000002.txt`. If this naming scheme does not seem convenient, the `result_file` option allows to overwrite what the filename would be.

* `method`: if specified a particular method will be applied to the task.

* `description`: an optional string describing the test

* `ignore_exception`: if present, any exception that occurs while running the test case will be ignored. Can be used in conjunction with `result:compare` to perform comparison of the test results. 

The settings file may contain additional parameters, that when specified will be passed along to the task / problem / method.


### Example settings  file


	# this test runs the biomodels 0-19 as a time course for a duration of 10 
	# time units with 50 output steps
	task: timecourse
	location: ..\BioModels_Database-r31_pub-sbml_files\curated
	filter: BIOMD00000000[0-1]\d
	format: sbml
	result: run-only
	start: 0
	duration: 10.0
	steps: 50

