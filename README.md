# λ

λ -- pronounced Lambda -- is a small interpreter for Pythonic Lambda functions and List Comprehension.

## Warning :building_construction:
The following program is thought as a personal replacer for [awk](https://git.savannah.gnu.org/git/gawk.git "awk"),  therefore is under heavy development to **increase** functionalities and performance of the program.

### Table of Contents
1. [License](#license)
2. [Installation](#installation)
3. [Usage](#usage)
4. [How to contribute](#how-to-contribute)


---

### License
The code is released under MIT License

---

### Installation
1. Clone the repository
2. Go inside the cloned `Lambda` directory and open here a Terminal
3. Make sure you can run the build-script with `chmod+x build.sh`
4. Run the script by typing `./build.sh` in your terminal
5. Move the compiled binary `lambda` under `/usr/local/bin` 

---

### Usage
##### Lambda Functions
You start by typing *lambda* to invoke the program, followed by any option flag, then the required parameters.
```bash
lambda "#1 ** #2" 2 3 4
```
The output is the same of applying in a python script the following code, extra arguments are automatically discarded.
```python
fun = (lambda x,y: x ** y)
result = fun(2, 3)
```

##### List Comprehension
You start by typing *lambda* to invoke the program, followed by any option flag -- in the following example we use `--dtype` to tell what type to use for the arguments, otherwise they are treated as python **str** type by default, then the required parameters as usual.

To tell the program we want to treat the args as a List and not individually we must use the `#@` inside the function and `#i` as the current iterated element of the list.
```bash
lambda --dtype=int "#i + 2 for #i in #?"  1 2 10 25
```

The output is the same of applying in a python script the following code
```python
args = [1, 2, 10, 25]
result = [x + 2 for x in args]
```

##### Lambda Function and Reduction
You start by typing *lambda* to invoke the program, followed by the `-r`flag to enable the *reduce* chain and the initial value.
Then we can insert option flags -- in the following example we use `-dt` which is the short version of `--dtype` to tell what type to use for the arguments.
```bash
lambda -r 0 -dt=int "#1+#2" 1 7 13 29
```

The output is the same of applying in a python script the following code
```python
from functools import reduce

args = [1, 7, 13, 29]
result = reduce((lambda x,y: x+y), args, 0)
```

##### Lambda Function concatenation through Lambda Scripts
Consider we want to apply a series of lambda expressions, carrying the result of each expression.

We start by defining the series of lambda expressions in a file, line by line.
For example here is how to apply the formula from the Pythagorean Theorem
```python
#1**2 + #2**2
#1**0.5
str(#1)+' is the result of the applied Pythagorean Formula'
```

Then we can pass it the invocation of the lambda program.
```bash
lambda --dtype=int script::/absolute/path/to/script 2 4
```

which is the same of writing the following python code:
```python
x = 2
y = 4
pythagorean = (x**2+y**2)**0.5
result = f'{pythagorean} is the result of the applied Pythagorean Formula'
```

Some notes about using custom scripts:
- Arguments type is inferenced between each phase of the script except the first where is mandatory to distinguish the data type with the flag -dt TYPE or --dtype=TYPE
- If a reduce parameter is given to the script, it will treat only the first line as an execution of the reduction

##### Using modules
Adding the `--module=[MODULE]` flag will allow to import at runtime the module `MODULE`.
For example if we define `--module=numpy` we will be able to use everything inside `numpy` like for example `numpy.random.default_rng().random()` to generate a random number inside our expression.

To add multiple modules use the following syntax `--module="MODULE1,MODULE2..."`

A small example:
```bash
lambda -D --dtype=int --module=math "#i+math.pi for #i in #?" 1 2 3 4 5 6 7 9 0
```

will return the output of:

```python
import math
args = [1, 2, 3, 4, 5, 6, 7, 9, 0]
result = [x+math.pi for x in args]
```

---

### How to contribute
When contributing to this repository, please first discuss the change you wish to make via issue with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

Pull Request Process

    Ensure any install or build dependencies are removed before the end of the layer when doing a build.
    Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
    Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is SemVer.
    Pull request will be merged once reviewed and fully tested.
