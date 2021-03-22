import requests
import json
from datetime import datetime
import math
import os

def get_last_update_date():
    dirname = os.path.dirname(__file__)
    # if the file exists get the last update timestamp
    try:
        filename = os.path.join(dirname, 'lastUpdate.txt')
        with open(filename) as f:
            last_timestamp = f.readlines()
    # if the is no file yet script will use a timestamp from a "startUpdate.txt" file.
    except:
        filename = os.path.join(dirname, 'startUpdate.txt')
        with open(filename) as f:
            last_timestamp = f.readlines()
    return last_timestamp[0]

# generate a new timestamp with a current time. it'll be the time of the last update
def get_new_timestamp():
    now = datetime.utcnow()
    time_now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(time_now)
    return time_now

# update the time of the last update
def modify_last_update_date(time_now):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'lastUpdate.txt')
    file1 = open(filename,"w") 
    file1.writelines(time_now) 
    file1.close()

def send_request(pubStartDate, pubEndDate, startIndex=0):
    Headers = {'Authorization': 'token {}'.format("testtoken")}
    Params = {"pubStartDate": pubStartDate, "pubEndDate": pubEndDate, "startIndex": startIndex}
    response = requests.get("http://localhost:4000/getlogs/bytimerange", headers=Headers, params=Params)
    return response.json()

def print_records(response):
    records = response['data']
    for record in records:
        # convert it back to json format
        record_json = json.dumps(record)
        print(record_json)


def main():
    # get last update timestamp
    last_update_tstamp = get_last_update_date()

    # generate new timestamp
    new_timestamp = get_new_timestamp()

    # send a first request 
    response = send_request(last_update_tstamp, new_timestamp)

    # print each record 
    print_records(response)

    # check if there is more then one page
    total = int(response['totalResults'])
    pageResults = int(response['pageResults'])

    if total > pageResults:
        pages_total = math.ceil(total/100)

        for page_index in range(1, pages_total):
            #repeat the request with a next page index
            response = send_request(last_update_tstamp, new_timestamp, page_index)
            # print each record 
            print_records(response)

    # update lastUpdate.txt file with the new timestamp:
    modify_last_update_date(new_timestamp)



if __name__ == "__main__":
    main()
