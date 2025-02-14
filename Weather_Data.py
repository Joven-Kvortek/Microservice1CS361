import json
import random
import datetime
import pika




def random_weather():
    random_temp = random.randint(0,100)

    random_humidity = random.randint(0,100)

    conditions = ["Clear skies", "Cloudy", "Thunderstorm", "Rain", "Snow"]
    random_condition = random.choice(conditions)

    random_precipitation = 0
    if random_condition == "Thunderstorm" or random_condition == "Rain" or random_condition == "Snow":
        random_precipitation = random.randint(50,100)
    else:
        random_precipitation = random.randint(0, 15)

    random_windspeed = random.randint(0,50)
    wind_direction = ["North", "South", "East", "West", "Northeast", "Southeast", "Northwest", "Southwest"]

    todays_date = datetime.datetime.now()
    todays_date_ISO = todays_date.isoformat("#", "seconds")
    print(todays_date_ISO)


    weather_data = {
        "Time and Date": f"{todays_date_ISO}",
        "Temperature": f"{random_temp} degrees",
        "Condition": f"{random_condition}",
        "Humidity": f"{random_humidity}%",
        "Precipitation": f"{random_precipitation}%",
        "WindSpeed": f"{random_windspeed}mph",
        "WindDirection": f"{random.choice(wind_direction)}"
    }
    return weather_data

def on_request(ch, method, props, body):
    print("Weather request received")
    weather_data = random_weather()
    response_body = json.dumps(weather_data)
    print(response_body)
    print("Weather request received, sending response: ", response_body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=response_body

                     )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='weather')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='weather', on_message_callback=on_request)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    start_server()