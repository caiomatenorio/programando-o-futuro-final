from marshmallow import Schema, fields, validate


class UpdateUserNameRequest(Schema):
    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=64),
            validate.Regexp(
                r"^(?=.*\S).+$",
                error="Nome não pode estar vazio ou conter apenas espaços em branco.",
            ),
        ],
        error_messages={"required": "Nome é obrigatório."},
    )


class UpdateUserEmailRequest(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email é obrigatório.",
            "invalid": "Email inválido.",
        },
    )
