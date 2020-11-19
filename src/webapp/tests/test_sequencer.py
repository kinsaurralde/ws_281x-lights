def resetActive(sequencer):
    sequencer.stopAll()
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
    assert not sequencer.run("sample", "")


def test_run(sequencer):
    assert sequencer.run("sample", "test_a")
    active = sequencer.active
    assert "sample-test_a" in active
    assert sequencer.checkActive("sample-test_a")
    resetActive(sequencer)


def test_stop_invalid_sequence(sequencer):
    assert not sequencer.stop("", "")


def test_stop_invalid_function(sequencer):
    assert not sequencer.stop("sample", "")


def test_stop_no_start(sequencer):
    assert not sequencer.stop("sample", "test_a")


def test_stop(sequencer):
    sequencer.run("sample", "test_a")
    assert sequencer.stop("sample", "test_a")
    assert sequencer.active["sample-test_a"]["start_time"] == 0
    resetActive(sequencer)


def test_stopall(sequencer):
    sequencer.run("sample", "test_a")
    sequencer.run("sample", "test_b")
    sequencer.run("sample", "test_c")
    sequencer.stopAll()
    for i in sequencer.active:
        assert sequencer.active[i]["start_time"] == 0
