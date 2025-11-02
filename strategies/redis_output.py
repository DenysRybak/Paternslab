#redis-server, redis-cli, KEYS *, GET line_0
import redis
from strategies.output_strategy_interface import OutputStrategy


class RedisOutputStrategy(OutputStrategy):
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def output(self, data):
        for i, line in enumerate(data):
            line_str = ','.join(map(str, line))
            self.client.set(f"line_{i}", line_str)
