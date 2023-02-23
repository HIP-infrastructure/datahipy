#!/bin/sh

docker run -it --rm -v /mnt/nextcloud-dp/nextcloud/data/:/data -v $(pwd)/scripts:/scripts hip/bids-converter:latest $@