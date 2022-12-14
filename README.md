# Docker Template for ML

This is a Docker template that helps to start writing qualitative Machine Learning software.

**Table of Contents**

- [Quick Start Guide for Linux](#quickstart-guide-for-linux)
- [System Requirements](#system-requirements)
- [Academic work](#academic-work)
- [Features](#features)
    - [Logging](#logging)
- [Folder Structure](#folder-structure)
- [Usage](#usage)
    - [Prerequisites / Installation](#prerequisites--installation)
        - [For running in Docker](#for-running-in-docker)
    - [Training](#training)
        - [Run in Docker](#run-in-docker)
    - [Testing](#testing)
    - [Configuration](#configuration)
        - [Arguments](#mtec-access)
        - [Configuration File](#configuration-file)
- [Customization and Modification](#customization-and-modification)
    - [Custom CLI options](#custom-cli-options)
    - [Update Requirements File](#update-requirements-file)
- [License](#license)
- [Acknowledgements](#contribution)

## Quickstart Guide for Linux
**Note**: Training data for IVOCT are not provided in this repository due to data protection reasons.
1. Clone the [Repository](https://github.com/lennardkorte/IDDATDLOCT/archive/refs/heads/main.zip) to your home directory
1. Add training data under: ```/<home_directory>/IDDATDLOCT/data/```
1. Install [Docker and NVIDIA Container Toolkit](#for-running-in-docker)
1. execute training and testing
    ```bash
    $ bash exe/run_train_and_eval_docker.sh
    ```

## System Requirements
- either or:
    - Windows 10 build is 17063 or later
    - MacOS Mojave or later
    - Ubuntu 20.04 or later
- required:
    - NVIDIA Graphics Card
    - Minimum 16GB RAM
- recommended:
    - 250 GB SSD Storage

## Academic work
See [Academic work]()

## Features
TODO

### Logging
TODO

## Folder Structure
  ```
  docker-template/
  │
  ├── academic work/        - academic documentation and interpretation
  │
  ├── data/                 - holds large data files like training data and Examples
  │
  ├── cfgs/                 - holds configuration files
  │   ├── config_standard.json      - specifies the standard configuration of application
  │   └── config.py                 - evaluates configurations, arguments and provides Config object
  │
  ├── src/                  - holds all python source code and standard configuration
  │   ├── logger.py                 - for logging result files and printing tasks
  │   ├── main.py                   - entrance point for application
  │   ├── docker_template.py         - Main app code
  │   ├── utils_wandb.py            - Wandb logging class
  │   └── utils.py                  - Helper functions and utilities
  │
  └── .dockerignore         - manages build files for docker
  │
  └── .gitignore            - specifies intentionally untracked files Git should ignore
  │
  ├── Dockerfile            - contains all the commands to assemble an image
  │
  ├── LICENCE               - contains legal notice
  │
  ├── requirements.txt      - contains all modules required for applications execution
  │
  └── ...
  
  ```

## Usage
**Note:** All commands in the following are intended to be executed in the bash command line. 

### Prerequisites / Installation
Check if NVIDIA graphics card is available with:
```bash
$ ls -la /dev | grep nvidia
```

#### For running in Docker
**Note:** NVIDIA Container Toolkits are Linux only drivers. Therefore containerization as well as this guide is Linux only.
1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/)
    ```bash
    $ curl -fsSL https://get.docker.com -o get-docker.sh
    
    $ sudo sh get-docker.sh
    ```
2. Install [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
    ```bash
    $ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
        && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
        && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    
    $ sudo apt-get update && sudo apt-get install -y nvidia-docker2

    $ sudo systemctl restart docker
    ```
3. Availability of GPU's in Docker can be testes with the following command: 
    ```bash
    $ sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
    ```

### Training
#### Run in Docker
(Linux only)
```bash
$ sudo bash exe/run.sh
```

### Testing
The application tests the trained model automatically after it has been training with the best validated model and the last trained model.

### Data Sampling

The Pipeline can automatically generate a small number of samples that are output in  '*.h5'- and '*.jpg'-format. For this the flag ```--show_samples``` has to be added as described above. These samples are equally distributed over the training data set and stored in the data directory under `./data/h5s/data_augmentation/` and `./data/jpgs/data_augmentation/`. They are brightened and so may help to illustrate the preprocessing and data augmentation techniques.

### Configuration
#### Arguments
The configuration of the application can also be changed via command line arguments specified directly, when starting the program, e.g.:

##### Choose Devices for multi GPU training
```bash
$ bash exe/run_train_and_eval_docker.sh -gpu 1,2
```
##### Choose configuration file
```bash
$ bash exe/run_train_and_eval_docker.sh -ycf ./config.json
```

#### Configuration File
Configurations are copied and stored in the `name/` directory after starting the application for protocolling purposes. Different configurations may be provided via config file in `.json`-format under the path (`any_dir/config.json`) given by argument. When using docker the directory for the configuration file must be `./config.json`. Only configurations that have to be changed need to be specified. The standard configuration looks like this:
```json
{
    // Examples
    "key1": "value1",
    "groukey2p": "value2"
}
```

## Customization and Modification

### Custom CLI options
If some configurations need to be changhed often or quickly, then it is usefull to have command line options. By registering custom options as follows you can change some of them using CLI flags.

 ```python
  CustomArgs = collections.namedtuple('CustomArgs', 'flags type target')
  options = [
      CustomArgs(['--op1', '--option1'], type=float, target=('option1')),
      CustomArgs(['--op2', '--option2'], type=int, target=('option2'))
      # Add more custom args here
  ]
  ```
`target` argument is sequence of keys, which are used to modify that option in the configuration. In this example, `target` 
for the learning rate option is `('option1')` because `config['option1']` points to the option1.

### Update Requirements File
In case any changes were made to the code affecting the imports of the application, the requirements file can always be updated (or replaced in case there is one already) by generating a new requirements file with:
```bash
$ pip3 install pipreqs

$ pipreqs --savepath ./requirements.txt ./src
```
**Note:** All modules have to be installed for this command to work propperly which are supposed to be imported (unexpected behaviour). 

## License
This project is licensed under the MIT License. See [License]() for more details

## Acknowledgements
TODO