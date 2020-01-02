from datetime import datetime, timedelta, timezone
import json
import os

import pytest

from livestyled import schemas
from livestyled.client import LiveStyledAPIClient
from livestyled.tests.utils import configure_mock_responses

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
TEST_API_DOMAIN = 'test.livestyled.com'
CONTENT_TYPE = 'application/ld+json'


def test_deserialize_device():
    serialized_data = json.loads(open(os.path.join(FIXTURES_DIR, 'device_6.json'), 'r').read())
    deserialized_data = schemas.DeviceSchema().load(serialized_data)
    assert deserialized_data
    print(deserialized_data)
    assert deserialized_data['id'] == 6
    assert deserialized_data['token'] == '002332C86002'
    assert deserialized_data['consent'] == {
        'id': 2,
        'location_capture': True,
        'location_granular': None,
        'camera': True,
        'calendar': False,
        'photo_sharing': True,
        'push_notification': True,
        'created_at': datetime(2018, 12, 5, 17, 15, 3, tzinfo=timezone(timedelta(0), '+0000')),
        'updated_at': datetime(2018, 12, 5, 17, 15, 3, tzinfo=timezone(timedelta(0), '+0000'))
    }
    assert deserialized_data['push_consents'] == []
    assert deserialized_data['type'] == 'IOS'
    assert deserialized_data['status'] == 'ACTIVE'
    assert deserialized_data['app_version'] == '7.1'
    assert deserialized_data['os_version'] is None
    assert deserialized_data['model'] == 'Simulator'
    assert deserialized_data['manufacturer'] == 'Apple'
    assert deserialized_data['bluetooth_on'] is None
    assert deserialized_data['wifi_connected'] is None
    assert deserialized_data['created_at'] is None
    assert deserialized_data['updated_at'] is None


@pytest.fixture(scope='session')
def test_client():
    return LiveStyledAPIClient(
        api_domain=TEST_API_DOMAIN,
        api_key='thisisjustatest'
    )


def test_client_can_get_device_by_id(requests_mock, test_client):

    mock_responses = (
        ('GET', 'https://' + TEST_API_DOMAIN + '/v4/devices/1', 'mock_responses/ls_api/device_1.json', 200),
    )
    configure_mock_responses(requests_mock, mock_responses, FIXTURES_DIR, CONTENT_TYPE)

    device = test_client.get_device(1)
    assert device == {
        'id': 1,
        'token': '002332C86002',
        'consent': {
            'id': 2,
            'location_capture': True,
            'location_granular': None,
            'camera': True,
            'calendar': False,
            'photo_sharing': True,
            'push_notification': True,
            'created_at': datetime(2018, 12, 5, 17, 15, 3, tzinfo=timezone(timedelta(0), '+0000')),
            'updated_at': datetime(2018, 12, 5, 17, 15, 3, tzinfo=timezone(timedelta(0), '+0000'))
        },
        'push_consents': [],
        'type': 'IOS',
        'status': 'ACTIVE',
        'app_version': '7.1',
        'os_version': None,
        'model': 'Simulator',
        'manufacturer': 'Apple',
        'bluetooth_on': None,
        'wifi_connected': None,
        'created_at': None,
        'updated_at': None,
    }


def test_client_can_get_list_of_devices(requests_mock, test_client):

    mock_responses = (
        ('GET', 'https://' + TEST_API_DOMAIN + '/v4/devices', 'mock_responses/ls_api/devices_list_page_1.json', 200),
        ('GET', 'https://' + TEST_API_DOMAIN + '/v4/devices?page=2', 'mock_responses/ls_api/devices_list_page_2.json', 200),
    )
    configure_mock_responses(requests_mock, mock_responses, FIXTURES_DIR, CONTENT_TYPE)

    devices = test_client.get_devices()
    assert sum(1 for _ in devices) == 3