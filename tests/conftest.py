from pytest import fixture


@fixture(scope="function")
def my_fixture_function():
    return "this is the fixture"
