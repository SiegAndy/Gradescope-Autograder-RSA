# Gradescope-Autograder-RSA
Autograder for RSA assignment on Gradescope

## How to use
* Run `bash make_autograder.sh` will zip all needed files into a zip file.
* Upload zip file to gradescope in `Configure Autograder` tab
  

## How to test locally
* Place `grading.json` under the `./src` folder 
* Place `rsa.py` under the `./src` and `./src/autograder/submission` folder
* Move to src folder `cd ./src`
* Test with `python3 text_test.py`

## How to test remotely
Upload the custom `rsa.py` file to gradescope like how the student submit their work.


## How to add new tests
* Edit the files or create new ones in the `tests` folder
* To create new tests in existed files, just need to add new methods to the class. (method name must be starting with `"test_"`)
* To create new tests in new file, the new file, new class, and new methods should all have the name started with `"test_"`.


## Current tests
* Check whether file with expected name is uploaded
* Check whether file does not import any function/class which directly compute RSA operations
* Check whether class has correct implementation for `compute_key()`, `encrypt()`, and `decrypt()` method.
* Check whether class has assigned class attributes in the `compute_key()` method.


## Misc

In the `./holdout/rsa/main.py`, it provides the function `generate_instance()` which can generate parameters for `grading.json`.