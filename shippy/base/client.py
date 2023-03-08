from abc import ABC, abstractmethod

from .config import BaseConfig
from .models import CreateShipmentResponseBase
from .schemas import Shipment


class BaseClient(ABC):
    config: BaseConfig

    def __init__(self, config: BaseConfig | None, config_model: type(BaseConfig)):
        if config is None:
            config = config_model()
        self.config = config
        super().__init__()

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        raise NotImplementedError()

    @abstractmethod
    def ship(self, shipment: Shipment, *args, **kwargs) -> CreateShipmentResponseBase:
        raise NotImplementedError()
