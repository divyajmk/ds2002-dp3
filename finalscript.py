#!/home/gitpod/.pyenv/shims/python3



import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/jww2fj"
sqs = boto3.client('sqs')

# create dictionary
messages = {}
# create list to store receipt handles for when deleting messages
receipt_handle = []

def delete_message(handles):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message

        # Want to loop through 10 messages
        for _ in range(10):
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

                #store in dictionary
                messages[order] = word
                # store in list too 
                receipt_handle.append(handle)

                # Print the message attributes - this is what you want to work with to reassemble the message
                print(f"Order: {order}")
                print(f"Word: {word}")

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                break

                
    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()

    #print dictionary
    print("Messages Dictionary:", messages)

    # assemble words according to their order values
    assembled_phrase = ' '.join(messages[order] for order in sorted(messages.keys()))

    # Print the assembled phrase
    print("Assembled Phrase:", assembled_phrase)

    # Now, delete messages 
    for handle in receipt_handle:
        delete_message(handle)
