from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    name = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=1,
                max=64,
                error="Nome deve ter entre 1 e 64 caracteres.",
            ),
            validate.Regexp(
                r"^(?=.*\S).+$",
                error="Nome não pode estar vazio ou conter apenas espaços em branco.",
            ),
        ],
        error_messages={"required": "Nome é obrigatório."},
    )

    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email é obrigatório.",
            "invalid": "Email inválido.",
        },
    )

    password = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=8, max=128, error="Senha deve ter entre 8 e 128 caracteres."
            ),
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
                r"^(?=.*[@$!%*?&#^~.,:;+=_\-\(\)\[\]\{\}<>|\\/\"\'\`]).*$",
                error="Senha deve conter pelo menos um caractere especial (@, $, !, %, *, ?, &).",
            ),
            validate.Regexp(
                r"^[A-Za-z\d@$!%*?&#^~.,:;+=_\-\(\)\[\]\{\}<>|\\/\"\'\`]+$",
                error="Senha deve conter apenas letras, números e caracteres especiais.",
            ),
        ],
        error_messages={"required": "Senha é obrigatória."},
    )


class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email é obrigatório.",
            "invalid": "Email inválido.",
        },
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Senha é obrigatória."),
        error_messages={"required": "Senha é obrigatória."},
    )
