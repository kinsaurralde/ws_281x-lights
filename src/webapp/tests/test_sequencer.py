def resetActive(sequencer):
    sequencer.active = {}


def test_getsequences(client):
    response = client.get("/getsequences")
    data = response.get_json()
    assert isinstance(data, dict)


def test_add(sequencer):
    sequencer.add([{}])


def test_checkactive_false(sequencer):
    response = sequencer.checkActive("invalid")
    assert not response


def test_run_invalid_sequence(sequencer):
    assert not sequencer.run("", "")


def test_run_invalid_function(sequencer):
    assert not sequencer.run("test", "")


def test_run(sequencer):
    assert sequencer.run("test", "test_a")
    active = sequencer.active
    assert "test-test_a" in active
    assert sequencer.checkActive("test-test_a")
    resetActive(sequencer)


def test_stop_invalid_sequence(sequencer):
    assert not sequencer.stop("", "")


def test_stop_invalid_function(sequencer):
    assert not sequencer.stop("test", "")


def test_stop_no_start(sequencer):
    assert not sequencer.stop("test", "test_a")


def test_stop(sequencer):
    sequencer.run("test", "test_a")
    assert sequencer.stop("test", "test_a")
    assert sequencer.active["test-test_a"]["start_time"] == 0
    resetActive(sequencer)


def test_stopall(sequencer):
    sequencer.run("test", "test_a")
    sequencer.run("test", "test_b")
    sequencer.run("test", "test_c")
    sequencer.stopAll()
    for i in sequencer.active:
        assert sequencer.active[i]["start_time"] == 0
