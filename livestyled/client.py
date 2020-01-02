import json
from typing import Dict, Generator, List

from marshmallow import Schema
import requests

from livestyled.schemas import (
    AppSchema,
    DeviceConsentSchema,
    DeviceSchema,
    DeviceTokenSchema,
    EventCategorySchema,
    EventIntegrationSchema,
    EventSchema,
    EventStageSchema,
    PushConsentSchema,
    UserSchema,
    VenueSchema,
)

CONTENT_TYPE = 'application/ld+json'


class LiveStyledAPIClient:
    def __init__(
            self,
            api_domain: str,
            api_key: str
    ):
        self._api_domain = api_domain
        self._api_key = api_key

    def _api_get(
            self,
            endpoint: str,
            params: Dict or None = None
    ) -> Dict:
        if not params:
            params = {}
        response = requests.get(
            'https://{}/{}'.format(
                self._api_domain,
                endpoint,
            ),
            params=params,
            headers={
                'Content-Type': CONTENT_TYPE,
                'x-api-key': self._api_key
            }
        )
        return response.json()

    def _api_get_paginated(
            self,
            endpoint: str,
            params: Dict or None = None,
    ) -> Generator[Dict, None, None]:
        if params:
            response = self._api_get(endpoint, params)
        else:
            response = self._api_get(endpoint)
        resources = response['hydra:member']
        next_page_url = response['hydra:view'].get('hydra:next', False)
        for resource in resources:
            yield resource
        while next_page_url:
            next_page_url = next_page_url.replace('//', '/').lstrip('/')
            response = self._api_get(next_page_url)
            resources = response['hydra:member']
            next_page_url = response['hydra:view'].get('hydra:next', False)
            for resource in resources:
                yield resource

    def _api_patch(
            self,
            endpoint: str,
            data: dict
    ) -> Dict:
        response = requests.get(
            'https://{}/{}'.format(
                self._api_domain,
                endpoint,
            ),
            headers={
                'Content-Type': CONTENT_TYPE,
                'x-api-key': self._api_key
            },
            data=json.dumps(data)
        )
        return response.json()

    def _get_resource(
            self,
            resource_id: int or str,
            schema: Schema
    ):
        resource_data = self._api_get(
            '{}/{}'.format(
                schema.Meta.url,
                resource_id
            )
        )
        resource = schema().load(resource_data)
        return resource

    def _get_resources(
            self,
            schema: Schema,
            params: Dict or None = None,
    ) -> Generator[Dict, None, None]:
        data_generator = self._api_get_paginated(
            schema.Meta.url,
            params
        )
        for resource_data in data_generator:
            yield schema().load(resource_data)

    def get_app(
            self,
            app_id: int or str,
    ) -> Dict:
        return self._get_resource(
            app_id,
            AppSchema,
        )

    def get_apps(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(AppSchema)

    def get_device(
            self,
            device_id: int or str,
    ) -> Dict:
        return self._get_resource(
            device_id,
            DeviceSchema,
        )

    def get_devices(
            self,
            token: str or None = None,
            tokens: List[str] or None = None,
            status: str or None = None,
            statuses: List[str] or None = None
    ) -> Generator[Dict, None, None]:
        filter_params = {}
        if token:
            filter_params['token'] = token
        if tokens:
            filter_params['token[]'] = tokens
        if token and tokens:
            # TODO error as mutually exclusive
            pass
        if status:
            filter_params['status'] = status
        if statuses:
            filter_params['status[]'] = statuses
        if status and statuses:
            # TODO error as mutually exclusive
            pass

        return self._get_resources(
            DeviceSchema,
            params=filter_params
        )

    def update_device(
            self,
            device_id: str,
            attributes: Dict,
    ) -> Dict:
        updated_device = self._api_patch(
            '{}/{}'.format(DeviceSchema.Meta.url, device_id),
            attributes
        )
        return DeviceSchema().load(updated_device)

    def get_device_consent(
            self,
            consent_id: int or str,
    ) -> Dict:
        return self._get_resource(
            consent_id,
            DeviceConsentSchema,
        )

    def get_device_consents(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(
            DeviceConsentSchema,
        )

    def get_device_token(
            self,
            token_id: int or str,
    ) -> Dict:
        return self._get_resource(
            token_id,
            DeviceTokenSchema,
        )

    def get_device_tokens(
            self,
            provider: str or None = None,
            providers: List[str] or None = None,
            device: str or None = None,
            devices: List[str] or None = None
    ) -> Generator[Dict, None, None]:
        filter_params = {}
        if provider:
            filter_params['provider'] = provider
        if providers:
            filter_params['provider[]'] = providers
        if provider and providers:
            # TODO error as mutually exclusive
            pass
        if device:
            filter_params['device'] = device
        if devices:
            filter_params['device[]'] = device
        if device and devices:
            # TODO error as mutually exclusive
            pass
        return self._get_resources(
            DeviceTokenSchema,
            params=filter_params,
        )

    def get_event(
            self,
            event_id: int or str,
    ) -> Dict:
        return self._get_resource(
            event_id,
            EventSchema,
        )

    def get_events(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(EventSchema)

    def get_event_category(
            self,
            category_id: int or str,
    ) -> Dict:
        return self._get_resource(
            category_id,
            EventCategorySchema,
        )

    def get_event_categories(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(EventCategorySchema)

    def get_event_integration(
            self,
            integration_id: int or str,
    ) -> Dict:
        return self._get_resource(
            integration_id,
            EventIntegrationSchema,
        )

    def get_event_integrations(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(EventIntegrationSchema)

    def get_event_stage(
            self,
            stage_id: int or str,
    ) -> Dict:
        return self._get_resource(
            stage_id,
            EventStageSchema,
        )

    def get_event_stages(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(EventStageSchema)

    def get_push_consent(
            self,
            consent_id: int or str,
    ) -> Dict:
        return self._get_resource(
            consent_id,
            PushConsentSchema,
        )

    def get_push_consents(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(PushConsentSchema)

    def get_user(
            self,
            user_id: int or str,
    ) -> Dict:
        return self._get_resource(
            user_id,
            UserSchema,
        )

    def get_users(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(UserSchema)

    def get_venue(
            self,
            venue_id: int or str,
    ) -> Dict:
        return self._get_resource(
            venue_id,
            VenueSchema,
        )

    def get_venues(
            self,
    ) -> Generator[Dict, None, None]:
        return self._get_resources(VenueSchema)