import argparse
import logging
import json
import os
import requests

logging.basicConfig(
    format='%(asctime)-15s: %(name)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('connectors-deploy')
LOGGER.setLevel(logging.INFO)

API_ROOT_TEMPLATE = {
    "dev": "http://localhost:8083",
    "staging": "http://stag.majoo-dw.id:8083",
    "prod": "http://prod.majoo-dw.id:8083"
}

CONNECTORS_CONFIG_ROOT_TEMPLATE = f"./connectors"
CONNECTOR_EXT = ".json"


def main():
    args = parse_args()

    LOGGER.info("Starting...")

    raw_config_filenames = find_files(get_connectors_config_root(args))

    LOGGER.info(f"Found connector configs: {raw_config_filenames}")

    processed_configs = process_config_files(raw_config_filenames)

    update_or_create_connectors(processed_configs, args)

    LOGGER.info("Completed")


def find_files(path_to_use):
    config_filenames = []

    for path, dirs, files in os.walk(path_to_use):
        for file in files:
            if file.endswith(CONNECTOR_EXT):
                config_filenames.append(os.path.abspath(path + "/" + file))

    return config_filenames


def process_config_files(raw_config_filenames):
    configs = []

    for filename in raw_config_filenames:
        with open(filename) as f:
            configs.append(f.read())

    return configs


def get_api_root(args):
    return API_ROOT_TEMPLATE[args.env]


def get_connectors_config_root(args):
    # return CONNECTORS_CONFIG_ROOT_TEMPLATE + args.env
    return CONNECTORS_CONFIG_ROOT_TEMPLATE


def update_or_create_connectors(configs, args):
    api_root = get_api_root(args)
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}

    for config in configs:
        config_json = json.loads(config)

        LOGGER.info(f"Adding/updating {config_json['name']} connector")

        if args.dry_run:
            LOGGER.info(
                "Dry run is enabled, just printing config: \n" + config)
        else:
            # Update or Create a connector
            url = f"{api_root}/connectors/{config_json['name']}/config/"
            response = requests.put(
                url,
                data=config,
                headers=headers)

            LOGGER.info(f"Response: {response.status_code}")

            response.raise_for_status()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--env',
        required=True,
        choices=['dev', 'staging', 'prod'],
        help='Kafka Connect environment')

    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        default=False,
        action='store_true',
        help='Dry-run mode')

    return parser.parse_args()


if __name__ == "__main__":
    main()
