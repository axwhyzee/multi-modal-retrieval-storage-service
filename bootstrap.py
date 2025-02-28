from dependency_injector import containers, providers
from event_core.adapters.pubsub import RedisPublisher
from event_core.config import get_deployment_env

from repository import LocalRepository, S3Repository

MODULES = ("handlers",)


class DIContainer(containers.DeclarativeContainer):
    repo = providers.Singleton(
        LocalRepository if get_deployment_env() == "DEV" else S3Repository
    )
    pub = providers.Singleton(RedisPublisher)


def bootstrap() -> None:
    container = DIContainer()
    container.wire(modules=MODULES)
    container.wire(modules=MODULES)
