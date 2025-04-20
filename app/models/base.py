import abc

class BaseRunner(abc.ABC):
    """
    Runner 抽象基类。
    """

    def __init__(self):
        self.model = None

    @abc.abstractmethod
    async def init_model(self, repo: str | None):
        ...

    @abc.abstractmethod
    async def infer(self, request_body):
        ...