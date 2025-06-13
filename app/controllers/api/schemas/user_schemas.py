from marshmallow import Schema, fields, validate


class UpdateUserNameSchema(Schema):
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


class UpdateUserEmailSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email é obrigatório.",
            "invalid": "Email inválido.",
        },
    )


class UpdateUserPasswordSchema(Schema):
    current_password = fields.String(
        required=True,
        error_messages={"required": "Senha é obrigatória."},
    )

    new_password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=128),
            validate.Regexp(
                r"^(?=.*[A-Z]).*$",
                error="Senha deve conter pelo menos uma letra maiúscula.",
            ),
            validate.Regexp(
                r"^(?=.*[a-z]).*$",
                error="Senha deve conter pelo menos uma letra minúscula.",
            ),
            validate.Regexp(
                r"^(?=.*\d).*$",
                error="Senha deve conter pelo menos um dígito.",
            ),
            validate.Regexp(
                r"^(?=.*[@$!%*?&]).*$",
                error="Senha deve conter pelo menos um caractere especial (@, $, !, %, *, ?, &).",
            ),
            validate.Regexp(
                r"^[A-Za-z\d@$!%*?&]{8,128}$",
                error="Senha deve conter apenas letras, números e caracteres especiais (@, $, !, %, *, ?, &).",
            ),
        ],
        error_messages={"required": "Senha é obrigatória."},
    )


class DeleteUserAccountSchema(Schema):
    password = fields.String(
        required=True,
        error_messages={"required": "Senha é obrigatória."},
    )
