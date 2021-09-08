#!/bin/bash

# Script created by: Michael Susanto (@michaelsusanto81)

# Automating steps from: https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-debian-10

# Install OpenJDK as one of the Kafka's Dependencies
echo "Installing OpenJDK . . ."
sudo apt update && sudo apt -y install default-jdk

# Downloading and Extracting Kafka Binary
# This script using Kafka 2.8.0 (Scala 2.13)
echo "Downloading Kafka Binary . . ."
mkdir ~/Downloads
curl "https://dlcdn.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz" -o ~/Downloads/kafka.tgz
mkdir ~/kafka && cd ~/kafka
tar -xvzf ~/Downloads/kafka.tgz --strip 1

echo "Done."
echo "See https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-debian-10 for more details. (Start from Step 3)"
