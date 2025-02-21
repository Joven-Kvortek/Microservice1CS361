To request data, create your own Weatherrpc in your main program. Run rabbitmq locally on your computer. Weatherrpc will connect to the queue, I named weather, but you can name it anything you like. You can also include whatever parameters you want in your weatherrpc, mine were just a guess. After you create your weatherRPC class, an example call could be: 
if __name__ == '__main__':
    weather_client = WeatherRPC()
Receiving data is also a part of your WeatherRPC class. You can do what I did and create a function named onResponse(), so that when a respone is received from my rabbitmq server, your WeatherRPC class displays the data. For example:
def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

