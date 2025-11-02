from strategies.console_output import ConsoleOutputStrategy
from strategies.kafka_output import KafkaOutputStrategy
from strategies.redis_output import RedisOutputStrategy
from data_reader import read_data_from_url
import json


class DataOutputContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def execute_strategy(self, data):
        self._strategy.output(data)


def get_output_strategy_from_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    strategy = config.get("output_strategy", "console")

    if strategy == "console":
        return ConsoleOutputStrategy()
    elif strategy == "kafka":
        return KafkaOutputStrategy()
    elif strategy == "redis":
        return RedisOutputStrategy()
    else:
        raise ValueError(f"Unsupported strategy: {strategy}")


def main():
    output_strategy = get_output_strategy_from_config('config.json')

    context = DataOutputContext(output_strategy)

    url = "https://www.dallasopendata.com/api/views/qv6i-rri7/rows.csv?accessType=DOWNLOAD"
    data = read_data_from_url(url)

    context.execute_strategy(data)

    for i, row in enumerate(data):
        if i >= 50:
            break
        context.execute_strategy(row)


if __name__ == "__main__":
    main()
