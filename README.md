## Python COPASI test suite
This project hosts a testing framework for COPASI. Next to a collection of tests found under the `test-suite` folder. Under the `copasi_test` folder all the manipulation / comparison routines are housed. 

### Installation
The test suite should work with python 2.x and python 3.x, provided the following packages are installed: 

* python-copasi
* pandas

### Usage

#### Running Tests:
Still work in progress, currently most inspection is done interactively using jupyter notebooks. To invoke from the command line: 

	python test_copasi.py <Test> <CopasiSE> <OutDir> [Task Name]

where

* `<Test>` is a full path to the folder of the test suite, or a test subfolder thereof. All tests found will be run.  
* `<CopasiSE>` is the full path to a COPASI SE executable that is to be tested. 
* `<OutDir>` is the output folder in which temporary models are created to run the tests, along with the test results. 
* `[Task Name]` is an optional task name that the test suite should be filtered for, so that only tasks with that name will be run. Examples here include: `Steady-State`, `Time-Course`, `Scan`...

#### Comparing output only:
To simply invoke the comparison routines (and not re-run the tests), invoke from the command line: 

	python compare_only.py <Test> <CopasiSE> <OutDir>

where

* `<Test>` is a full path to the folder of the test suite, or a test subfolder thereof. All tests found will be run.  
* `<CopasiSE>` is the full path to a COPASI SE executable that is to be tested. 
* `<OutDir>` is the output folder in which temporary models are created to run the tests, along with the test results. 

#### Comparing the results from two versions of CopasiSE:
To simply invoke the comparison routines (and not re-run the tests), invoke from the command line: 

	python compare_versions.py <Test> <CopasiSE1> <OutDir1> <CopasiSE2> <OutDir2>

where

* `<Test>` is a full path to the folder of the test suite, or a test subfolder thereof. All tests found will be run.  
* `<CopasiSE1>` is the full path to a COPASI SE executable that is to be tested. 
* `<OutDir1>` is the output folder in which temporary models are created to run the tests, along with the test results. 
* `<CopasiSE2>` is the full path to a COPASI SE executable that is to be tested. 
* `<OutDir2>` is the output folder in which temporary models are created to run the tests, along with the test results. 

### Output
When running the tests, usually an abbreviated output is expected, that would look something like: 

	.........................E.
	There was 1 error
	
	00002:report-00002-BIOMD0000000001 - Status different: An equilibrium steady state (zero fluxes) was found. != A steady state with given resolution was found.
	
where basically a dot '.' is printed for each test / model that is being run, a 'W' for occurring warnings and an 'E' for a test failure. All failures will be printed once all tests are run. 

It is possible to get the full output by specifying the environment variable `COPASI_TEST_PRINT=1` prior to invoking the script. If that variable is set, the full output will be printed which would look something like this: 

	687      INFO    - Starting test 00002 for BIOMD0000000001
	1235     ERROR   - 00002:report-00002-BIOMD0000000001 - Status different: An equilibrium steady state (zero fluxes) was found. != A steady state with given resolution was found.
	1235     INFO    - Starting test 00002 for BIOMD0000000002
	1508     INFO    - Starting test 00002 for BIOMD0000000003

here the first column indicates the time in msecs, since the tests began, the second column the status information and the third one the message that was logged. 

### License

The packages available on this page are provided under the 
[Artistic License 2.0](http://copasi.org/Download/License/), 
which is an [OSI](http://www.opensource.org/) approved license. This license 
allows non-commercial and commercial use free of charge.
 