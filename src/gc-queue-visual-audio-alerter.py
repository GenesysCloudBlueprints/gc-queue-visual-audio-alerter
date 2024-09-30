#  Audio-alert for queued interactions - for Raspberry Pi
#  https://github.com/GenesysCloudBlueprints/gc-queue-visual-audio-alerter
#
#  Install required dependecies: PureCloudPlatformClientV2, time, requests (sudo pip install PureCloudPlatformClientV2 time requests)
#  Install omxplayer (If you're using a device with audio output and wish to use a sound file) (sudo apt-get install omxplayer)
#
#  By Mark Booth
#  Last updated 2024-09-20

print("Initialising...")

import base64, json, requests, os, time
import PureCloudPlatformClientV2
import RPi.GPIO as GPIO
from PureCloudPlatformClientV2.rest import ApiException

buzz_pin = 7            # GPIO Pin used for buzzer
led_pin = 5             # GPIO Pin used for LED
query_interval_time = 5 # Time between queries (in seconds)
buzz_duration = 2       # Duration of audible alert (in seconds)

queue_names = ["Sales", "Accounts"]                                                     # Populate with names of queues to monitor
os.environ["PURECLOUD_CLIENT_ID"] = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"              # Provide OAuth Client ID
os.environ["PURECLOUD_CLIENT_SECRET"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"   # Provide OAuth Client Secret

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzz_pin, GPIO.OUT)
GPIO.output(buzz_pin, 0)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, 0)

print('Audiable alert when interactions are waiting in queue(s) using PureCloud Python SDK')

PureCloudPlatformClientV2.configuration.host = "https://api.mypurecloud.com.au" # Update with relevant region url
apiClient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(os.environ['PURECLOUD_CLIENT_ID'], os.environ['PURECLOUD_CLIENT_SECRET'])
routing_api = PureCloudPlatformClientV2.RoutingApi(apiClient)
analytics_api = PureCloudPlatformClientV2.AnalyticsApi(apiClient)

def validate_queue_name(queue_name):
    queue_id = 0
    queue_waiting_interactions = 0

    try:
        api_response = routing_api.get_routing_queues(name=queue_name)
        if(len(api_response.entities) < 1):
            print(" - Queue '" + queue_name + "' not found. excluding.")
            return -1
        elif(len(api_response.entities) > 1):
            print(" - Found more than one queue with the name '" + queue_name + "' excluding.")
            return -1
        else:
            queue_id = api_response.entities[0].id
            print(" - Found queue '" + queue_name + "' - adding queue id '" + queue_id + "' to array.")
            queue_ids.append(queue_id)

    except ApiException as e:
        print("Error on RoutingAPI -> " + e)

def print_queue_name_array():
    print("Queue names: ", end='')
    print(queue_names)

def print_queue_id_array():
    print("Queue ids: ", end='')
    print(queue_ids)

def get_queue_waiting_interactions(queue_id):
    try:
        query = PureCloudPlatformClientV2.QueueObservationQuery()
        query.metrics = ['oWaiting']
        query.filter = PureCloudPlatformClientV2.ConversationAggregateQueryFilter()
        query.filter.type = 'or'
        query.filter.clauses = [PureCloudPlatformClientV2.ConversationAggregateQueryClause()]
        query.filter.clauses[0].type = 'or'
        query.filter.clauses[0].predicates = [PureCloudPlatformClientV2.ConversationAggregateQueryPredicate()]
        query.filter.clauses[0].predicates[0].dimension = 'queueId'
        query.filter.clauses[0].predicates[0].value = queue_id
        query_result = analytics_api.post_analytics_queues_observations_query(query)
        queue_waiting_interactions = query_result.results[0].data[0].stats.count
    except ApiException as e:
        print("Error on RoutingAPI -> " + e)

    return queue_waiting_interactions

if __name__ == "__main__":
    queue_ids = [] # Leave this array blank, it will be populated by the script
    #queue_name = input("Enter queue name: ") # Uncomment to allow runtime-input of single queue name
    print_queue_name_array()
    for queue_name in queue_names:
        validate_queue_name(queue_name)
    #print_queue_id_array()

    print("Monitoring queues for interactions...");

    while True:
        total_waiting_interactions = 0
        for queue_id in queue_ids:
            queue_waiting_interactions = get_queue_waiting_interactions(queue_id)
            if queue_waiting_interactions > 0:
                print(queue_id + " has " + str(queue_waiting_interactions) + " interaction(s) Waiting")
                total_waiting_interactions += 1
        if total_waiting_interactions > 0:
            #os.system('omxplayer /home/pi/sound.mp3 > /dev/null 2>&1') # Uncomment if using omx player to play sound file instead of buzzer beep
            GPIO.output(buzz_pin, 1)
            time.sleep(buzz_duration)
            GPIO.output(buzz_pin, 0)
        else:
            #print("Waiting for queued interactions...")
            pass
        if total_waiting_interactions == 0:
            GPIO.output(led_pin, 0)
        else:
            GPIO.output(led_pin, 1)
        time.sleep(query_interval_time)
