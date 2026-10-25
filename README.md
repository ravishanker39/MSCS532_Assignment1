# MSCS532 Assignment 1

## Purpose

This project implements Insertion Sort in Python to arrange an array of integers
in monotonically decreasing order, interpreted as nonincreasing order when
duplicates occur: every value is greater than or equal to the next value.
The program retains all input values and performs the sorting itself, without
calling `sorted()` or `list.sort()`.

The assignment draws on the insertion-sort algorithm in Chapter 2 of
*Introduction to Algorithms* (Cormen et al., 2022). Insertion Sort grows a sorted
prefix one element at a time. It is an incremental algorithm, rather than a
divide-and-conquer algorithm such as Merge Sort.

## Project files

| File | Purpose |
| --- | --- |
| `insertion_sort.py` | Descending Insertion Sort, comments, and a runnable demonstration |
| `test_insertion_sort.py` | Automated correctness, stability, and command-line checks |
| `README.md` | Setup instructions, explanation, examples, complexity, and references |
| `.gitignore` | Excludes the local virtual environment and generated files from Git |

## Python setup on macOS

The course requires Python 3.8 or higher. Install a currently supported Python 3
release for your Mac from [python.org](https://www.python.org/downloads/) if
necessary. The macOS installer uses a `.pkg` workflow; the assignment's
Windows-style "Add Python to PATH" checkbox is not a macOS installation step.
Python's macOS documentation explains its installation options (Python Software
Foundation, n.d.-b).

Open Terminal and verify the installed interpreter:

```bash
python3 --version
```

In the project folder, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

A virtual environment isolates project packages from other Python environments
(Python Software Foundation, n.d.-c). This project needs no third-party packages.
The commands below use `python3`; after activation, `python` also refers to the
environment's interpreter. Run `deactivate` when finished.

## Visual Studio Code setup

Install or update [Visual Studio Code](https://code.visualstudio.com/), then open
this project folder with **File > Open Folder**. Install the **Python** extension
published by **Microsoft** from the Extensions view. Use **Command+Shift+P** on
macOS, run **Python: Select Interpreter**, and select the interpreter inside
`.venv`. Microsoft documents interpreter selection and running Python from the
editor (Microsoft, n.d.-a).

Open `insertion_sort.py` and use **Run Python File in Terminal**, or run the
commands below in **Terminal > New Terminal**. To inspect a pass of the algorithm,
place a breakpoint on `current_value = values[position]` and use the Python
debugger to inspect `position`, `scan`, and `values`. Code Runner is optional in
the assignment; the official Python extension already supports running this
program. VS Code is the editor and debugging interface; the selected Python
interpreter executes the program.

## Running the program

From the project directory, run the built-in example:

```bash
python3 insertion_sort.py
```

Expected output:

```text
Original array: [28, -4, 13, 28, 0, 9, -11]
Descending array: [28, 28, 13, 9, 0, -4, -11]
```

To supply another array, enter space-separated integers:

```bash
python3 insertion_sort.py 16 -3 8 16 0
```

Expected output:

```text
Original array: [16, -3, 8, 16, 0]
Descending array: [16, 16, 8, 0, -3]
```

The command-line interface accepts integers. A noninteger argument produces a
usage error. With no arguments, the program uses the demonstration array. The
sorting function itself also handles an empty list.

## How descending insertion works

At each position, the algorithm saves the current value, scans the sorted prefix
to its left, and shifts smaller values one place to the right. It then inserts
the saved value into the available position. The direction is determined by:

```python
while scan >= 0 and values[scan] < current_value:
```

An ascending version shifts larger values. Here, the `<` comparison shifts
smaller values so that larger values appear first. Checking `scan >= 0` before
indexing also prevents the scan from wrapping around to Python's negative indices.

For the input `[16, -3, 8, 16, 0]`, the completed passes are:

| Pass | Value inserted | Array after insertion |
| --- | --- | --- |
| Initial | None | `[16, -3, 8, 16, 0]` |
| 1 | -3 | `[16, -3, 8, 16, 0]` |
| 2 | 8 | `[16, 8, -3, 16, 0]` |
| 3 | 16 | `[16, 16, 8, -3, 0]` |
| 4 | 0 | `[16, 16, 8, 0, -3]` |

The loop invariant is that the prefix before the current position is already
sorted in nonincreasing order and contains the same elements as the corresponding
original prefix. Initially, a prefix with one element is sorted. Each pass shifts
only smaller elements, then inserts the saved element, extending the sorted
prefix without losing or adding values. When the loop ends, the prefix covers
the entire array. Empty and single-element arrays require no passes.

Equal values are not shifted past the current value because the comparison is
strict. This preserves their relative order, making the implementation stable.
The function mutates the original list and returns that same list.

## Efficiency and computer architecture

For an array of length `n`, an already descending input needs no shifts, so its
best-case running time is Theta(n). Ascending input with distinct values requires
1 + 2 + ... + (n - 1) shifts, or n(n - 1)/2, giving Theta(n squared) worst-case
time. Random permutations of distinct values also have Theta(n squared) expected
running time. The function uses O(1) auxiliary space: it keeps indices and a
saved value rather than constructing a second array. These bounds use the usual
model in which each integer comparison and assignment has constant cost; Python
integers can have additional cost when their bit lengths grow.

The input list still occupies O(n) storage, even though the sorting algorithm
needs only constant extra storage. In CPython, Python source is compiled into
bytecode that the interpreter executes (Python Software Foundation, n.d.-a).
The interpreter's machine instructions run on the CPU, while the list and its
objects reside in process memory. Repeated comparisons and shifts therefore
consume processing time and memory-access work. This explains why Insertion Sort
is suitable for small arrays but becomes costly on large, unfavorable inputs.

VS Code helps inspect execution through breakpoints and variable views. Git
records version history, while GitHub hosts a remote repository for access and
collaboration. VS Code's Source Control view provides a Git interface for staging,
committing, and synchronizing changes (Microsoft, n.d.-b). A Python virtual
environment isolates packages; it is not a separate virtual computer.

## Testing

Run the tests from the project directory:

```bash
python3 -m unittest -v
```

The suite contains 13 tests covering empty input, one element, descending and
ascending input, equal values, negative values, mixed values, in-place behavior,
stability, and command-line behavior. One test enumerates all 1,093 arrays of
length zero through six over the values -1, 0, and 1 and compares the result to
Python's built-in descending sort. The built-in sort is used only as an independent
test oracle; it is not used by the assignment's sorting implementation.

The stability test gives equal integers distinct labels and confirms that those
labels keep their original relative order. The command-line checks verify the
default example, custom input, and rejection of invalid text.

Validation: all 13 tests passed with Python 3.12.14, including the exhaustive
check of 1,093 small arrays.

## Version control

This public repository separates project documentation, the sorting implementation,
and automated tests into focused commits. Git records each change locally, and
GitHub provides remote hosting. Repository creation and file management follow
GitHub's documented workflow (GitHub, n.d.-a, n.d.-b).

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
*Introduction to algorithms* (4th ed.). The MIT Press.
https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/

GitHub. (n.d.-a). *Adding a file to a repository*. GitHub Docs.
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

GitHub. (n.d.-b). *Creating a new repository*. GitHub Docs.
https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository

Microsoft. (n.d.-a). *Getting started with Python in VS Code*.
https://code.visualstudio.com/docs/python/python-tutorial

Microsoft. (n.d.-b). *Source control in VS Code*.
https://code.visualstudio.com/docs/sourcecontrol/overview

Python Software Foundation. (n.d.-a). *Glossary*. Python documentation.
https://docs.python.org/3/glossary.html

Python Software Foundation. (n.d.-b). *Using Python on macOS*. Python documentation.
https://docs.python.org/3/using/mac.html

Python Software Foundation. (n.d.-c). *venv — Creation of virtual environments*.
Python documentation. https://docs.python.org/3/library/venv.html
