from marshmallow import Schema, fields, validate


class UpdateUserNameSchema(Schema):
    """
    Schema for updating the user's name. It validates that the name is a non-empty string with a
    maximum length of 64 characters and does not consist solely of whitespace.
    """

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
    """
    Schema for updating the user's email. It validates that the email is a valid email format.
    """

    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email é obrigatório.",
            "invalid": "Email inválido.",
        },
    )


class UpdateUserPasswordSchema(Schema):
    """
    Schema for updating the user's password. It validates that the current password is provided and
    that the new password meets specific criteria, including length, character types, and allowed
    characters.
    """

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
    """
    Schema for deleting the user's account. It validates that the user provides their password for
    confirmation before account deletion.
    """

    password = fields.String(
        required=True,
        error_messages={"required": "Senha é obrigatória."},
    )
