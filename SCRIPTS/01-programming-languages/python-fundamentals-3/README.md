# Python fundamentals 3

File: `SCRIPTS/01-programming-languages/python-fundamentals-3/README.md`

Folder: `SCRIPTS/01-programming-languages/python-fundamentals-3`

Five small Python 3.10+ lessons use only the standard library. Each script validates its boundary inputs and prints JSON where practical. Run commands from the repository root; no script writes to input files or uses the network.

## Lessons

- `nested_records.py`: nested dictionaries, lists and sorted aggregate output.
- `generator_pipeline.py`: a lazy generator that filters and transforms integers.
- `text_file_summary.py`: bounded UTF-8 reading of regular, non-symlink files.
- `dataclass_tasks.py`: validated records represented by frozen dataclasses.
- `module_usage.py`: a runnable script importing the sibling `module_helpers.py` module.

The file summary rejects symlinks, missing paths, directories, invalid UTF-8 and files over 1 MiB. Other lessons keep inputs in memory and cap counts to make resource behavior explicit. These are teaching examples, not production file scanners or schema validators.

## Examples

```text
python SCRIPTS/01-programming-languages/python-fundamentals-3/nested_records.py "[{\"name\":\"Ada\",\"profile\":{\"city\":\"London\"},\"active\":true,\"tags\":[\"math\"]}]"
python SCRIPTS/01-programming-languages/python-fundamentals-3/generator_pipeline.py -3 -2 0 3 4
python SCRIPTS/01-programming-languages/python-fundamentals-3/text_file_summary.py examples/notes.txt
python SCRIPTS/01-programming-languages/python-fundamentals-3/dataclass_tasks.py "[{\"title\":\"Learn\",\"priority\":1}]"
python SCRIPTS/01-programming-languages/python-fundamentals-3/module_usage.py Ada --repeat 2
```

`text_file_summary.py` requires an existing UTF-8 fixture; the test suite creates a temporary one and removes it during cleanup.
