from functools import wraps
from typing import Callable, Type

from flask import g
from pydantic import BaseModel

from flask_reqcheck.request_validation import (
    BodyDataValidator,
    FormDataValidator,
    PathParameterValidator,
    QueryParameterValidator,
)
from flask_reqcheck.valid_request import get_valid_request


def validate(
    body: Type[BaseModel] | None = None,
    query: Type[BaseModel] | None = None,
    path: Type[BaseModel] | None = None,
    form: Type[BaseModel] | None = None,
) -> Callable:
    """
    A decorator to validate Flask request data against Pydantic models.

    This decorator validates the request data against the provided Pydantic models for
    body, query, path, and form data. Inside a Flask route function that is decoarted
    with this function, we can access the validated request instance using the
    :func:`~valid_request.get_valid_request` helper function.

    :param body: The Pydantic model to validate the request body against.
    :type body: Type[BaseModel] | None
    :param query: The Pydantic model to validate the request query parameters against.
    :type query: Type[BaseModel] | None
    :param path: The Pydantic model to validate the request path parameters against.
    :type path: Type[BaseModel] | None
    :param form: The Pydantic model to validate the request form data against.
    :type form: Type[BaseModel] | None
    :return: A decorator function that validates the request data.
    :rtype: Callable
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validated = get_valid_request()
            validated.path_params = PathParameterValidator(path).validate(f)
            validated.query_params = QueryParameterValidator(query).validate()
            validated.body = BodyDataValidator(body).validate()
            validated.form = FormDataValidator(form).validate()

            g.valid_request = validated

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_path(path: Type[BaseModel] | None = None) -> Callable:
    """
    A decorator to validate Flask request path parameters against a Pydantic model.

    :param path: The Pydantic model to validate the request path parameters against.
    :type path: Type[BaseModel] | None
    :return: A decorator function that validates the request path parameters.
    :rtype: Callable
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validated = get_valid_request()
            validated.path_params = PathParameterValidator(path).validate(f)
            g.valid_request = validated
            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_query(query: Type[BaseModel] | None = None) -> Callable:
    """
    A decorator to validate Flask request query parameters against a Pydantic model.

    :param query: The Pydantic model to validate the request query parameters against.
    :type query: Type[BaseModel] | None
    :return: A decorator function that validates the request query parameters.
    :rtype: Callable
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validated = get_valid_request()
            validated.query_params = QueryParameterValidator(query).validate()
            g.valid_request = validated
            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_body(body: Type[BaseModel] | None = None) -> Callable:
    """
    A decorator to validate Flask request body against a Pydantic model.

    :param body: The Pydantic model to validate the request body against.
    :type body: Type[BaseModel] | None
    :return: A decorator function that validates the request body.
    :rtype: Callable
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validated = get_valid_request()
            validated.body = BodyDataValidator(body).validate()
            g.valid_request = validated
            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_form(form: Type[BaseModel] | None = None) -> Callable:
    """
    A decorator to validate Flask request form data against a Pydantic model.

    :param form: The Pydantic model to validate the request form data against.
    :type form: Type[BaseModel] | None
    :return: A decorator function that validates the request form data.
    :rtype: Callable
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validated = get_valid_request()
            validated.form = FormDataValidator(form).validate()
            g.valid_request = validated
            return f(*args, **kwargs)

        return wrapper

    return decorator
