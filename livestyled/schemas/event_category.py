from marshmallow import EXCLUDE, fields, Schema

from livestyled.schemas.utils import get_id_from_url


class EventCategorySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    title = fields.String()
    resource = fields.String()
    force_show = fields.Boolean(data_key='forceShow')
    updated_at = fields.AwareDateTime(data_key='updatedAt', allow_none=True)
    created_at = fields.AwareDateTime(data_key='createdAt', allow_none=True)
    app = fields.Function(get_id_from_url)
    venue = fields.Function(get_id_from_url)
    sort_id = fields.Boolean(data_key='sortId')
    translations = fields.List(fields.Inferred, allow_none=True)