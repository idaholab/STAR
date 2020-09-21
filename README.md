![masthead](/images/Masthead.png)

# Structured Threat Automated Response (STAR)

Structured Threat Automated Response (STAR) provides a flexible framework to automatically execute courses of action in response to received cyber observable data objects. Based on Structured Threat Information Expression (STIX) v2.1, STAR enables the execution of tailored responses to cyber issues in an operational environment.

STAR is a script that creates a python run-time for automated response action included in the STIX Course of Action object. This script can parse a valid STIX json file and execute the included Course of Action.

See the [STAR Innovation Sheet](20-50510_R2_STAR Innovation Sheet_06252020.pdf) for an overview.

## Installation
Install system dependencies:
`sudo apt install build-essential python3-venv curl libxml git tshark`

STAR requires python3. Ensure an up to date Python 3 version is installed on your system (STAR has been tested with Python 3.7/8 on Ubuntu 18.04/20.04). 

Copy the project folder to desired system location. Run the following to install the python dependencies.

`python3 install -r requirements.txt`

### STructured Threat Observable Tool Set (STOTS)
STAR uses the previously released Structured Threat Observable Tool Set (STOTS) for receiving structured observable data. STOTS can be downloaded from https://github.com/idaholab/STOTS.


## STAR Run Modes

Run STAR in API mode

`python3 STAR.py`

Run a COA directly from STAR

`python3 STAR.py /path/to/coa.json`


## CLI

A simple CLI is provided to test running COAs that exist in a STIX 2.0 bundle
CLI mode is used when the JSON STIX file is passed as the first argument to the script


## API

The API exists to create a seamless interaction with the included monitoring engines
and their current method of submitting Cyber Observables via http POST requests.
The available routes that can be accessed are within STAR:

* `/api/stix-object` for uploading Cyber Observables to be analyzed in order to trigger a COA

* `/stix-bundle` for uploading the initial STIX bundle to be parsed for indicators and COAs

  

## Example Usage

Launching STAR

```
python3 /<PATH>/STAR.py
```

Uploading a STIX2.0 Bundle to STAR

```
curl -F 'file=@/<PATH>/COA.json' http://127.0.0.1:9001/stix-bundle  
```

Manually POST'ing an Observable to STAR

```
curl -d '{cyber-obs : foo}' -H Content-Type : application/json -X POST http://127.0.0.1:9001/api/stix-object
```

FileEngine Monitoring and POST'ing an Observable to STAR

```
python3 /<PATH>/FileEngine.py -d <DELAY_IN_SECS> -u <USERNAME> -p <PASSWORD> --os <Windows|Linux> <REMOTE_IP> 127.0.0.1:<STAR_PORT> '<REMOTE_MONITORED_FOLDER>'
```

ProcessEngine Monitoring and POST'ing an Observable to STAR

```
python3 /<PATH>/ProcessEngine.py -d <DELAY_IN_SECS> -u <USERNAME> -p <PASSWORD> --os <Windows|Linux> <REMOTE_IP> 127.0.0.1:<STAR_PORT> <PROCESS_NAME PROCESS_NAME …>
```

PacketEngine Playback and POST'ing an Observable to STAR

```
python3 /<PATH>/PacketEngine/packetengine.py -r /<PATH>/PreCollected.pcap -t 127.0.0.1 -p <STAR_PORT>
```

ProcessEngine Monitoring and POST'ing an Observable to STAR

```python
python3 /<PATH>/PacketEngine/packetengine.py -i <ETHERNET_INTERFACE> -t 127.0.0.1 -p <STAR_PORT>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.


## Other Software
Idaho National Laboratory is a cutting edge research facility which is a constantly producing high quality research and software. Feel free to take a look at our other software and scientific offerings at:

[Primary Technology Offerings Page](https://www.inl.gov/inl-initiatives/technology-deployment)

[Supported Open Source Software](https://github.com/idaholab)

[Raw Experiment Open Source Software](https://github.com/IdahoLabResearch)

[Unsupported Open Source Software](https://github.com/IdahoLabCuttingBoard)

## License

Copyright 2020 Battelle Energy Alliance, LLC

Licensed under the 3-Part BSD (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  https://opensource.org/licenses/BSD-3-Clause

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

