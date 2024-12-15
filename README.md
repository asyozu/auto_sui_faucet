# Auto Sui Faucet

[![License](https://img.shields.io/github/license/asyozu/auto_sui_faucet)](LICENSE)  [![Issues](https://img.shields.io/github/issues/asyozu/auto_sui_faucet)](https://github.com/asyozu/auto_sui_faucet/issues)

## Overview

**Auto Sui Faucet** is an automated tool designed to streamline the process of acquiring Sui tokens for development and testing purposes. By automating the faucet interactions, developers can save time and focus on building applications within the Sui blockchain ecosystem.

## Features

- Automated requests to the Sui faucet.
- Configurable parameters to suit individual needs.
- Lightweight.

## Installation

To set up the Auto Sui Faucet, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/asyozu/auto_sui_faucet.git
   ```
2. Navigate to the project directory:
   ```
   cd auto_sui_faucet
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

Alternatively, download the prebuilt Windows executable from the [latest release](https://github.com/asyozu/auto_sui_faucet/releases/latest).

## Usage

1. Configure the settings by editing the configuration file:
   ```
   config.json
   ```

   | Key                | Description                                                                                      | Example                                                                                     |
   |--------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
   | `recipient_address`| Address to receive Sui tokens.                                                                   | `0xf5daa612aecf13d9c59f8f62cc09e8dd8748205eb6fc2ad1bda966c9e30de8ea`                        |
   | `sleep_time`       | Time interval (in seconds) between requests. Must be greater than or equal to 1800.             | `1800`                                                                                     |
   | `faucet`           | The faucet type to use, such as `devnet` or `testnet`.                                           | `devnet`                                                                                   |

2. Run the script:
   ```
   python3 main.py
   ```
3. Monitor the output to ensure tokens are successfully received.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter issues or have questions, feel free to open a discussion or contact the maintainer through the [GitHub Issues](https://github.com/asyozu/auto_sui_faucet/issues) section.

## Acknowledgements

- The Sui blockchain community for their support and resources.
- Open-source contributors for inspiration and guidance.
