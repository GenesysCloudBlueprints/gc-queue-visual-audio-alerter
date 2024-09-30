<a id="readme-top"></a>
  <h1 align="center">gc-queue-visual-audio-alerter</h1>
  <p align="center">
    Audio and Visual alerter for Genesys Cloud queued interactions
    <br />
  </p>

<!-- ABOUT THE PROJECT -->
## About The Project

![alerter diagram](https://github.com/GenesysCloudBlueprints/gc-queue-visual-audio-alerter/blob/main/blueprint/images/CloudQuery.png?raw=true)

This script can be used by Genesys Cloud customers who require external audio/visual alerting devices to be deployed in their premises. An example would be a warehouse setting or on-call environment where the agent/staff is not required at their desk at all times.

When a call enters one of the monitored queues, the device will emit sound and light, alerting the staff member(s) to the waiting interaction. The script can monitor multiple queues concurrently.

The Script is designed to run on a small single-board computer such as the Raspberry Pi Zero W, using it's GPIO pins as outputs to control the light/sound.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

![python logo](https://github.com/GenesysCloudBlueprints/gc-queue-visual-audio-alerter/blob/main/blueprint/images/python_logo_sm.png?raw=true)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

The <a href="https://github.com/MyPureCloud/platform-client-sdk-python">Genesys Cloud Python Platform API Client SDK</a> is required to run this script.
As are standard python libraries: time, requests.
* pip
  ```sh
  pip install PureCloudPlatformClientV2 time requests
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Configure a new Genesys Cloud OAuth client as described <a href="https://help.mypurecloud.com/articles/create-an-oauth-client/">here</a>
2. Clone the repo
   ```sh
   git clone https://github.com/GenesysCloudBlueprints/gc-queue-visual-audio-alerter
   ```
3. Install python dependencies
   ```sh
   pip install PureCloudPlatformClientV2 time requests
   ```
4. Edit `gc-queue-visual-audio-alerter/src/gc-queue-visual-audio-alerter.py` to add the following:
	- `PURECLOUD_CLIENT_ID` - The Client ID from the OAuth client you created in Genesys Cloud
	- `PURECLOUD_CLIENT_SECRET` - The Client Secret from the OAuth client you created in Genesys Cloud
	- `buzz_pin` - GPIO Pin used for the buzzer (or relay controlling the audio alerting device)
	- `led_pin` - GPIO Pin used for the led (or relay controlling the visual alerting device)
	- `query_interval_time` (optional) - Time between API queries in seconds (Default 5)
	- `buzz_duration` (optional) - Duration of audio alert in seconds (Default 2)
	- `queue_names` - Populate array with names of queues to be monitored, eg: `["Sales", "Accounts"] `
	- `PureCloudPlatformClientV2.configuration.host` - API URL for relevant region <a href="https://developer.genesys.cloud/platform/api/">list here</a>
  
5. Configure `gc-queue-visual-audio-alerter.py` to run as service at boot (This will depend on the OS/Distro you're running).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

When run as a service, the script will poll the Genesys Cloud API ad the desired intervals to check for interactions waiting in the designated queues.
If any of the queues have a waiting interaction, the LED and buzzer will be triggered until the queues are clear.

<!-- CONTRIBUTING -->
## Contributing

<a href="https://github.com/GenesysCloudBlueprints/gc-queue-visual-audio-alerter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=GenesysCloudBlueprints/gc-queue-visual-audio-alerter" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

My Github page for Genesys Projects: https://github.com/mb-genesys
Project Link: https://github.com/GenesysCloudBlueprints/gc-queue-visual-audio-alerter

<p align="right">(<a href="#readme-top">back to top</a>)</p>





