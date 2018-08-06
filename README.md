## Python COPASI test suite
This project hosts a testing framework for COPASI. Next to a collection of tests found under the `test-suite` folder. Under the `copasi_test` folder all the manipulation / comparison routines are housed. 

### Installation
The test suite should work with python 2.x and python 3.x, provided the following packages are installed: 

* python-copasi
* pandas

### Usage
Still work in progress, currently most inspection is done interactively using jupyter notebooks. To invoke from the command line: 

	python test_copasi <Test> <CopasiSE> <OutDir>

where

* `<Test>` is a full path to the folder of the test suite, or a test subfolder thereof. All tests found will be run.  
* `<CopasiSE>` is the full path to a COPASI SE executable that is to be tested. 
* `<OutDir>` is the output folder in which temporary models are created to run the tests, along with the test results. 

### License

The packages available on this page are provided under the 
[Artistic License 2.0](http://copasi.org/Download/License/), 
which is an [OSI](http://www.opensource.org/) approved license. This license 
allows non-commercial and commercial use free of charge.
 