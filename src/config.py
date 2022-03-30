import os


def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)
    return os.environ[variable]


class Config(object):
    user = setenv("POSTGRES_USER", "postgres")
    password = setenv("POSTGRES_PASSWORD", "password")
    hostname = setenv("POSTGRES_HOSTNAME", "0.0.0.0")
    port = setenv("POSTGRES_PORT", "5432")
    database = setenv("APPLICATION_DB", "my_db")
