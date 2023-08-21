# tap-applehealth

Singer tap for the `export.xml` file from Apple Health. Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Supported Data

- [x] Workout
- [ ] Record
- [ ] ActivitySummary

## Installation

Install from PyPi:

```bash
pipx install tap-applehealth
```

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| file_path           | True     | None    | The file path of the export.xml file. It can be a local file or a `s3://` path. |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

A full list of supported settings and capabilities is available by running: `tap-applehealth --about`

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Supported Python Versions

* 3.8
* 3.9
* 3.10
* 3.11

## Usage

You can easily run `tap-applehealth` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-applehealth --version
tap-applehealth --help
tap-applehealth --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

You will need [Poetry](https://python-poetry.org/docs/#installation) installed on your machine.

```bash
# Install package dependencies
poetry install
```

### Use pre-commit

```bash
pre-commit run --all-files
```

### Create and Run Tests

Create tests within the `tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-applehealth` CLI interface directly using `poetry run`:

```bash
poetry run tap-applehealth --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-applehealth
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-applehealth --version
# OR run a test `elt` pipeline:
meltano elt tap-applehealth target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
