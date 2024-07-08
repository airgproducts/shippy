import base64
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

DataType = TypeVar("DataType")


class CreateShipmentResponseBase(BaseModel, Generic[DataType], ABC):
    data: DataType

    @property
    @abstractmethod
    def tracking_id(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def _label(self) -> str:
        raise NotImplementedError()

    @property
    def label_as_bytes(self) -> bytes:
        return base64.b64decode(self._label)

    @property
    def label_as_string(self) -> str:
        return self._label


class CancelShipmentResponseBase(BaseModel, Generic[DataType], ABC):
    data: DataType

    @property
    @abstractmethod
    def cancellation_successful(self) -> bool:
        raise NotImplementedError()
