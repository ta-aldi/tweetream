from confluent_kafka.admin import AdminClient
from dotenv import load_dotenv
import os

# Load dotenv library
load_dotenv()

conf = {'bootstrap.servers': os.getenv('KAFKA_SERVERS')}
adminC = AdminClient(conf)

print(adminC.list_topics().topics)