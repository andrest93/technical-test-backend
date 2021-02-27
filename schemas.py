from marshmallow import Schema, fields


class UserSchema(Schema):
    user = fields.Str(required=True)
    password = fields.Str(required=True)


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    user = UserSchema

    class Meta:
        dump_only_pk = True


note_schema = NoteSchema()
user_schema = UserSchema()
