#!/usr/bin/bash

source /data/craws.cfg
source /opt/conda/.bashrc

micromamba activate

remap -o /level1c -l /level1b/*
