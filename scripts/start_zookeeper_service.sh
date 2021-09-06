#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Automating steps from: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-an-apache-zookeeper-cluster-on-ubuntu-18-04

# Please run this script as superuser!

sudo systemctl start zookeeper
sudo systemctl enable zookeeper
