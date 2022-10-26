from __future__ import annotations

import typing
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, TypeVar, List, Tuple
import time
import pydantic
from fastapi import UploadFile

from app.pkg.models import types

__all__ = ["BaseApiModel", "Model"]

Model = TypeVar("Model", bound="BaseApiModel")


class BaseApiModel(pydantic.BaseModel):
    def __cast_value(self, v, show_secrets, to_mongo, **kwargs):
        if isinstance(v, List):
            return [
                self.__cast_value(
                    v=ve, show_secrets=show_secrets, to_mongo=to_mongo, **kwargs
                )
                for ve in v
            ]
        elif isinstance(v, Tuple):
            return (
                self.__cast_value(
                    v=ve, show_secrets=show_secrets, to_mongo=to_mongo, **kwargs
                )
                for ve in v
            )
        elif isinstance(v, pydantic.SecretBytes):
            return v.get_secret_value().decode() if show_secrets else str(v)
        elif isinstance(v, pydantic.SecretStr):
            return v.get_secret_value() if show_secrets else str(v)
        elif isinstance(v, Dict) and v:
            return self.to_dict(
                show_secrets=show_secrets, values=v, to_mongo=to_mongo, **kwargs
            )
        elif to_mongo and isinstance(v, Decimal):
            return Decimal(str(float(v)))
        elif to_mongo and type(v) == date:
            return datetime.combine(v, datetime.min.time())
        elif to_mongo and (isinstance(v, typing.IO) or isinstance(v, UploadFile)):
            return None

        return v

    def to_dict(
        self,
        show_secrets: bool = False,
        values: Dict[Any, Any] = None,
        to_mongo=False,
        **kwargs,
    ) -> Dict[Any, Any]:
        """Make transfer model to Dict object.

        Returns: Dict object with reveal password filed.
        """
        values = self.dict(**kwargs).items() if not values else values.items()
        r = {}
        for k, v in values:
            if to_mongo and not isinstance(k, str):
                k = str(k)

            r[k] = self.__cast_value(
                v=v, show_secrets=show_secrets, to_mongo=to_mongo, **kwargs
            )

        return r

    def delete_attribute(self, attr: str) -> BaseApiModel:
        """Delete `attr` field from model.

        Args:
            attr: str value, implements name of field.
        Returns: self object.
        """
        delattr(self, attr)
        return self

    class Config:
        use_enum_values = True
        json_encoders = {
            pydantic.SecretStr: lambda v: v.get_secret_value() if v else None,
            pydantic.SecretBytes: lambda v: v.get_secret_value() if v else None,
            types.EncryptedSecretBytes: lambda v: v.get_secret_value() if v else None,
            bytes: lambda v: v.decode() if v else None,
            datetime: lambda v: int(v.timestamp()) if v else None,
            date: lambda v: int(time.mktime(v.timetuple())) if v else None,
            Decimal: lambda v: str(v) if v else None,
        }
        orm_mode = True
        allow_population_by_field_name = True
