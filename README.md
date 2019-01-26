# Divigil - Distro Vigil

Download and keep watch (vigil) for new releases of your favourite distributions. Supports plugins to search for distributions from extra sources. 
Currently supported: Distrowatch.com, Debian (also including checking checksum)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You can use the setup.py to install divigil automatically. Alternatively you will need the following python packages:

```
- apscheduler 
```

### Installing

You can install the project by using the setup.py like so:

```
python setup.py install
```

Or simply copy the project folder to wherever you want.

Now you will want to configure divigil. You can have a look in the config file.
The regular expressions are python regex. 
You can use websites such as https://pythex.org to construct a regular expression that works with whatever ISO you are trying to download.
Be sure to at least set the download folder to wherever you want divigil to download to.

## Deployment

Lastly, you might want to add this to your preferred init system and run it as a daemon.
An example systemd service file is included in the examples folder.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

