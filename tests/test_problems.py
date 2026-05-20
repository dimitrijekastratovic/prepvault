from tests.conftest import add_test_problem

def test_get_problems_returns_empty_list(client):
    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert "problems" in data
    assert isinstance(data["problems"], list)
    assert len(data["problems"]) == 0

def test_get_problems_returns_correct_data(client, test_problem):
    add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topic=test_problem["topic"]
    )

    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 1
    problem = data["problems"][0]
    assert problem["title"] == test_problem["title"]
    assert problem["description"] == test_problem["description"]
    assert problem["constraints"] == test_problem["constraints"]
    assert problem["difficulty"] == test_problem["difficulty"]
    assert problem["time_limit"] == test_problem["time_limit"]
    assert problem["memory_limit"] == test_problem["memory_limit"]
    assert problem["topic"] == [test_problem["topic"]]

def test_get_problems_with_multiple_problems(client, test_problem, test_problem2):
    add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topic=test_problem["topic"]
    )

    add_test_problem(
        title=test_problem2["title"],
        description=test_problem2["description"],
        constraints=test_problem2["constraints"],
        difficulty=test_problem2["difficulty"],
        time_limit=test_problem2["time_limit"],
        memory_limit=test_problem2["memory_limit"],
        topic=test_problem2["topic"]
    )

    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 2

def test_get_problems_returns_right_topic_values(client, test_problem):
    add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topic=test_problem["topic"]
    )

    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert "problems" in data
    assert len(data["problems"]) == 1
    problem = data["problems"][0]
    assert problem["topic"] == [test_problem["topic"]]
    assert isinstance(problem["topic"], list)