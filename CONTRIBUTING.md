# Contributing guide

The commands below should be used in a Bash-like shell

## Setup

### Transfer binary
The `trigger_cal` binary is used to retrieve library files used by this code. This binary can be found at `/usr/bin/trigger_cal`.

### Build Docker Image
Since the binary was made with PyInstaller, it can be extracted with pyinstxtractor. This happens as part of a Docker image build process.
Install a recent version of Docker and then run:
`docker build --progress=plain -t=steam_deck_overwrite_trigger_cal .`

## Development
To explore files extracted from the `trigger_cal` binary, start a shell in a container built from the image created in the previous step:
`docker run --rm -it steam_deck_overwrite_trigger_cal sh`

And then navigate to the `/home/trigger_cal_extracted` directory.
Here you can use `decompyle3` or `uncompyle6` to decompile the pyc files if needed for reference

Since the code reads from and writes to the trigger HID, the only way to test things is to pack it into a binary using the next step, and run it on the Steam Deck

## Repacking the custom code back into a binary using PyInstaller
If you use any shell that uses MinGW (such as Git Bash), first run `export MSYS_NO_PATHCONV=1`.

To build the binary, run: `docker run --rm -it -v $(pwd)/src/overwrite_trigger_cal.py:/app/overwrite_trigger_cal.py -v $(pwd)/dist:/app/dist steam_deck_overwrite_trigger_cal`

Built binary is now ready at `dist/overwrite_trigger_cal`

Tip: Map the dist folder in the Docker container directly into an SMB share to easily access it on the Steam Deck, e.g.:
`docker run --rm -it -v $(pwd)/src/overwrite_trigger_cal.py:/app/overwrite_trigger_cal.py -v /c/shared:/app/dist overwrite_trigger_cal`