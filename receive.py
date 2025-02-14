import uuid
from ast import main
import json
import pika, sys, os

class WeatherRPC:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True
                                    )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def request(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='weather',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body = ''
                                   )
        while self.response is None:
            self.connection.process_data_events()

        return json.loads(self.response.decode())

if __name__ == '__main__':
    weather_client = WeatherRPC()

    while True:
        user_input = input(
    "Enter a zip code to get weather data for that area, or press Enter to get weather in your current area.\n"
    "Type 'exit' to exit the program: "
)


        if user_input == 'exit':
            print("Exiting program...")
            sys.exit()

        if user_input.strip() == '':
            print("Getting weather for your current area...")
            weather_data = weather_client.request()
            for (key, value) in weather_data.items():
                print(f"{key}: {value}")
        else:
            try:
                weather_data = weather_client.request()
                zip_code = int(user_input)
                print(f"Getting weather for {zip_code} zip code...")
                for (key, value) in weather_data.items():
                    print(f"{key}: {value}")
            except ValueError:
                print("Invalid zip code. Please enter a valid zip code.")





