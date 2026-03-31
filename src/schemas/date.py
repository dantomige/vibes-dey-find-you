import calendar
from typing import Optional
from pydantic import BaseModel, model_validator

class Date(BaseModel):
    year: int
    month: Optional[int] = None
    day: Optional[int] = None

        
    @classmethod
    def from_string(cls, date_str: Optional[str]):
        
        if date_str is None:
            return None
        
        parts = date_str.split("-")
        date_params = [int(param) for param in parts]

        # print(date_params)
        
        if len(date_params) == 1:
            year, = date_params
            return cls(year=year)
        elif len(date_params) == 2:
            year, month = date_params
            return cls(year=year, month=month)
        elif len(date_params) == 3:
            year, month, day = date_params
            return cls(year=year, month=month, day=day)
        else:
            raise ValueError(f"Invalid date format: {date_str}")

    @model_validator(mode="after")
    def validate_date(self):

        if self.day is not None and self.month is None:
            raise ValueError("If 'day' is provided, 'month' must also be provided")
        
        if self.month is not None and not (1 <= self.month <= 12):
            raise ValueError("Month must be between 1 and 12")
        
        if self.day is not None:
            _, max_day = calendar.monthrange(self.year, self.month)

            if not (1 <= self.day <= max_day):
                raise ValueError("Invalid day for the given month/year")
            
        return self