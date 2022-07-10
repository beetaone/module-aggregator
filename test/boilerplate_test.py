from pytest import fixture, raises
from subprocess import run
from os import path, remove
from requests import post, exceptions
from json import load
from time import sleep

post_address = "http://0.0.0.0:80/"

input_file_path = "test/assets/input.json"

expected_output_file_path = "test/assets/expected_output.json"

listener1_output_file_path = "test/artifacts/listener1_output.json"
listener2_output_file_path = "test/artifacts/listener2_output.json"

input_file = open(input_file_path)
input_data = load(input_file)

expected_output_file = open(expected_output_file_path)
expected_data = load(expected_output_file)


@fixture
def start_stop_containers():
    run(["docker-compose", "-f", "test/docker-compose.test.yml", "up", "-d", "--build"])

    # sleep is required here as there is a delay between the execution of the command and the containers actually being responsive
    sleep(1)

    yield
    run(["docker-compose", "-f", "test/docker-compose.test.yml", "down"])


def test_container_pipeline(start_stop_containers):

    response = post(url=post_address, json=input_data)
    sleep(1)

    assert response.status_code == 200

    listener1_output_file = open(listener1_output_file_path)
    listener1_output_data = load(listener1_output_file)

    listener2_output_file = open(listener2_output_file_path)
    listener2_output_data = load(listener2_output_file)

    assert listener1_output_data == listener2_output_data == expected_data


def test_wrong_address(start_stop_containers):
    with raises(exceptions.ConnectionError):
        post(url="http://boilerplate_test_container", json=input_data)


def test_wrong_port(start_stop_containers):
    with raises(exceptions.ConnectionError):
        post(url="http://0.0.0.0:9090/", json=input_data)
