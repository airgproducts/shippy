from datetime import datetime

from pydantic import BaseModel

from shippy.base.utils import get_date_after_n_workdays


class RateShipmentResponseData(BaseModel):
    NumberOfWorkDays: int


class RateShipmentResponse(BaseModel):
    data: RateShipmentResponseData
    requested_at: datetime

    @property
    def delivery_date(self) -> datetime:
        return get_date_after_n_workdays(
            days=self.data.NumberOfWorkDays, start_datetime=self.requested_at
        )
