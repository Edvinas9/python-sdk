from datetime import datetime
from typing import Dict, List


class Device:
    def __init__(
            self,
            id: int,
            token: str,
            consent: str,
            push_consents: List[Dict],
            type: str,
            status: str,
            app_version: str,
            os_version: str,
            model: str,
            manufacturer: str,
            bluetooth_on: bool,
            wifi_connected: bool,
            updated_at: datetime,
            created_at: datetime,
    ):
        self._id = id
        self.token = token
        self.consent = consent
        self.push_consents = push_consents
        self.type = type
        self.status = status
        self.app_version = app_version
        self.os_version = os_version
        self.model = model
        self.manufacturer = manufacturer
        self.bluetooth_on = bluetooth_on
        self.wifi_connected = wifi_connected
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return '<Device(id={self.id!r})>'.format(self=self)