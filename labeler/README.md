# GAIA TA2 Labeler

## Installation

```
pip install flask
```

## Usage

```
python ws.py <source_file> <label_file>
```

Label file will be created if file doesn't exist.

## Source file structure

It's a json lines file, each line is:

```
{
  "id": "http://www.isi.edu/gaia/entities/e9dcb2bc-a699-4a63-b56c-279c7d09beb1---http://www.isi.edu/gaia/entities/f77067ae-c424-4166-bf88-b668a479fd46",
  "r1": {
    "id": "http://www.isi.edu/gaia/entities/e9dcb2bc-a699-4a63-b56c-279c7d09beb1",
    "source": "IC001MQC7",
    "mentions": [
      {
        "name": "Indian Express",
        "context": "<b>Indian Express</b>",
        "context_short": "...<b>Indian Express</b>..."
      }
    ]
  },
  "r2": {
    "id": "http://www.isi.edu/gaia/entities/f77067ae-c424-4166-bf88-b668a479fd46",
    "source": "HC000ZSAY",
    "mentions": [
      {
        "name": "Petersburg Nevsky Express",
        "context": "<b>Petersburg Nevsky Express</b> on November 27, 2009.",
        "context_short": "...<b>Petersburg Nevsky Express</b> on November 27, 2009...."
      }
    ]
  }
}
```
