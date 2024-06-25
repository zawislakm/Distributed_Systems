from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Client(_message.Message):
    __slots__ = ("firstname", "lastname", "email")
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    firstname: str
    lastname: str
    email: str
    def __init__(self, firstname: _Optional[str] = ..., lastname: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class DeliveryAddress(_message.Message):
    __slots__ = ("street", "house_number", "flat_number", "city", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    HOUSE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FLAT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    house_number: int
    flat_number: int
    city: str
    country: str
    def __init__(self, street: _Optional[str] = ..., house_number: _Optional[int] = ..., flat_number: _Optional[int] = ..., city: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class Basket(_message.Message):
    __slots__ = ("items", "amounts")
    class AmountsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    AMOUNTS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedScalarFieldContainer[str]
    amounts: _containers.ScalarMap[str, int]
    def __init__(self, items: _Optional[_Iterable[str]] = ..., amounts: _Optional[_Mapping[str, int]] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ("id", "basket", "client", "address")
    ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    id: int
    basket: Basket
    client: Client
    address: DeliveryAddress
    def __init__(self, id: _Optional[int] = ..., basket: _Optional[_Union[Basket, _Mapping]] = ..., client: _Optional[_Union[Client, _Mapping]] = ..., address: _Optional[_Union[DeliveryAddress, _Mapping]] = ...) -> None: ...

class GetOrderRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UpdateOrderRequest(_message.Message):
    __slots__ = ("id", "basket")
    ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_FIELD_NUMBER: _ClassVar[int]
    id: int
    basket: Basket
    def __init__(self, id: _Optional[int] = ..., basket: _Optional[_Union[Basket, _Mapping]] = ...) -> None: ...
