from pytest import raises

from my_django_rest_project.registry import Registry
from my_django_rest_project.types import DjangoObjectType
from my_django_rest_project.models import Reporter
import graphene
from graphene.test import Client
from django.contrib.auth.models import Group
from rbac.models import User


def test_should_raise_if_no_model():
    with raises(Exception) as exc_info:
        pass

    assert "valid Django Model" in str(exc_info.value)


def test_should_raise_if_model_is_invalid():
    with raises(Exception) as exc_info:
        class Character2(DjangoObjectType):
            pass
    assert "valid Django Model" in str(exc_info.value)


def test_should_map_fields_correctly():
    class ReporterType2(DjangoObjectType):
        class Meta:
            model = Reporter
            registry = Registry()
            fields = "__all__"

    fields = list(ReporterType2._meta.fields.keys())
    assert fields[:-3] == [
        "id",
        "first_name",
        "last_name",
        "email",
        "pets",
        "a_choice",
        "fans",
        "reporter_type",
    ]

    assert sorted(fields[-3:]) == ["apnewsreporter", "articles", "films"]


def test_should_map_only_few_fields():
    class Reporter2(DjangoObjectType):
        class Meta:
            model = Reporter
            fields = ("id", "email")

    fields = list(Reporter2._meta.fields.keys())
    assert sorted(fields[-3:]) == ["ap_news_reporter", "articles", "films"]
    assert list(Reporter2._meta.fields.keys()) == ["id", "email"]

    from my_django_rest_project.schema import (
        create_django_object_type,
        UserQuery,
        CreateUser,
        CreateUserInput,
        Mutation
    )
    assert UserType._meta.fields == "__all__"

    schema = graphene.Schema(query=UserQuery)
    client = Client(schema)

    mutation = '''
        mutation createUser($input: CreateUserInput!) {
            createUser(input: $input) {
                user {
                    username
                    email
                    groups {
                        name
                    }
                }
            }
        }
    '''
    variables = {
        "input": {
            "username": "newuser",
            "email": "newuser@example.com",
            "is_active": True,
            "groups": [999]  # Invalid group ID
        }
    }
    executed = client.execute(mutation, variables=variables)
    assert 'errors' in executed
    assert 'One or more group IDs are invalid.' in executed['errors'][0]['message']
