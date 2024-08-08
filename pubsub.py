import argparse
import sys

import google.cloud.pubsub_v1 as pubsub_v1
from typing import Optional
import json
import time
import secrets
import string

message_list = []


def list_topics(project_id: str) -> None:
    project_id = project_id
    publisher = pubsub_v1.PublisherClient()
    project_path = f"projects/{project_id}"
    for topic in publisher.list_topics(request={"project": project_path}):
        print(topic)


def create_topic(project_id: str, topic_id: str) -> None:
    project_id = project_id
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")


def list_subscriptions(project_id: str) -> None:
    project_id = project_id
    subscriber = pubsub_v1.SubscriberClient()
    project_path = f"projects/{project_id}"
    with subscriber:
        for subscription in subscriber.list_subscriptions(
                request={"project": project_path}
        ):
            print(subscription.name)


def create_subscription(project_id: str, topic_id: str, subscription_id: str) -> None:
    project_id = project_id
    topic_id = topic_id
    subscription_id = subscription_id

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    with subscriber:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
    print(f"Subscription created: {subscription}")


def receive_messages(project_id: str, subscription_id: str, timeout: Optional[float] = None) -> None:
    from concurrent.futures import TimeoutError
    project_id = project_id
    subscription_id = subscription_id
    timeout = 846000.0
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        msgRcvTimestamp = time.time()
        tlog = str(msgRcvTimestamp) + ","
        writeLogsToFile(tlog)
        message.ack()
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


def writeLogsToFile(timestamp):
    filename = "TimeLogs.txt"
    with open( filename , "a") as f :
        f.write(timestamp)



def publish_messages(project_id: str, topic_id: str) -> None:
    project_id = project_id
    topic_id = topic_id
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    count = 0
    writeLogsToFile("\n")
    record = {"currentPrice": "22303",
              "Company": "Tesla"}
    for i in range(0):
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                      for j in range(i))
        record.update({str(i*20) : str(res)})
    writeLogsToFile(str(sys.getsizeof(record)) + ",")
    publishTimestamp = time.time()
    tlog = str(publishTimestamp) + ","
    writeLogsToFile(tlog)
    for data in range(1):
        record.update({"id" : str(count)})
        data_str = json.dumps(record)
        data = data_str.encode("utf-8")
        future = publisher.publish(topic_path, data)
        print()
        print(future.result())
        count += 1
    print(f"published message to {topic_path}")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    subparsers = parser.add_subparsers(dest="command")
    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("topic_id")
    subscribe_parser = subparsers.add_parser("subscribe")
    subscribe_parser.add_argument("subscription_id")
    list_topic_parser = subparsers.add_parser("list-topics")
    create_topic_parser = subparsers.add_parser("create-topic")
    create_topic_parser.add_argument("topic_id")
    list_subscription_parser = subparsers.add_parser("list-subscriptions")
    create_subscription_parser = subparsers.add_parser("create-subscription")
    create_subscription_parser.add_argument("topic_id")
    create_subscription_parser.add_argument("subscription_id")

    args = parser.parse_args()

    if args.command == "publish":
        publish_messages(args.project_id, args.topic_id)
    elif args.command == "subscribe":
        receive_messages(args.project_id, args.subscription_id)
    elif args.command == "list-topics":
        list_topics(args.project_id)
    elif args.command == "create-topic":
        create_topic(args.project_id, args.topic_id)
    elif args.command == "list-subscriptions":
        list_subscriptions(args.project_id)
    elif args.command == "create-subscription":
        create_subscription(args.project_id, args.topic_id, args.subscription_id)

