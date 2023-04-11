from abc import ABC, abstractmethod
from enum import Enum

from .config import BaseConfig
from .models import CancelShipmentResponseBase, CreateShipmentResponseBase
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
    def ship(self, shipment: Shipment, service: Enum) -> CreateShipmentResponseBase:
        raise NotImplementedError()

    @abstractmethod
    def cancel_shipment(self, tracking_id: str) -> CancelShipmentResponseBase:
        raise NotImplementedError()
