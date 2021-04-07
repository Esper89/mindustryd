#!/bin/bash

if [[ "$EUID" -ne 0 ]]; then
	echo "Root permissions required to install mindustryd"
	exit 1
fi

pip3 install -e .
