# bib-add-year

A simple command-line tool to process `.bib` files that contain a `date` field,  
extract the year, and add it as a separate `year` field (if not already present).

Useful when working with BibLaTeX or BibTeX databases that use `date = {YYYY-MM-DD}`  
but you also need `year = {YYYY}` for compatibility with older styles.



## Installation

Using [uv](https://github.com/astral-sh/uv):

```bash
# From a local clone
uv pip install -e .
```

This will install an executable named `bib-add-year`.


## Usage

```bash
bib-add-year INPUT.bib [--output OUTPUT.bib]
```

- By default, the tool **modifies the file in place**.
- With `-o/--output`, the processed file is written to a new location.

### Example

**Input (`refs.bib`):**

```bibtex
@article{smith2020,
  author = {Smith, John},
  title = {A study},
  date = {2020-05-12},
}
```

**Run:**
```bash
bib-add-year refs.bib -o refs_with_year.bib
```

**Output:**
```bibtex
@article{smith2020,
  author = {Smith, John},
  title = {A study},
  date = {2020-05-12},
  year = {2020},
}
```

---

## Features

- Extracts the year from `date = {YYYY-MM-DD}` or `date = {YYYY}`.
- Adds a `year` field if missing.
- Leaves existing `year` fields untouched.
- Zero dependencies (pure Python).


## Development

Clone the repository and install in editable mode with dev dependencies:

```bash
uv pip install -e ".[dev]"
```

Then you can run linting/tests:

```bash
ruff check .
pytest
```


## License

MIT License. See [LICENSE](LICENSE) for details.