from tests.conftest import add_test_problem

def test_get_problems_returns_empty_list(client):
    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_problems_returns_correct_data(client, test_problem):
    add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topics=test_problem["topics"],
        test_cases=test_problem["test_cases"]
    )

    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    problem = data[0]
    assert problem["title"] == test_problem["title"]
    assert problem["description"] == test_problem["description"]
    assert problem["constraints"] == test_problem["constraints"]
    assert problem["difficulty"] == test_problem["difficulty"]
    assert problem["time_limit"] == test_problem["time_limit"]
    assert problem["memory_limit"] == test_problem["memory_limit"]
    assert problem["topics"] == test_problem["topics"]
    assert problem["test_cases"] == test_problem["test_cases"]

def test_get_problems_with_multiple_problems(client, test_problem, test_problem2):
    add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topics=test_problem["topics"],
        test_cases=test_problem["test_cases"]
    )

    add_test_problem(
        title=test_problem2["title"],
        description=test_problem2["description"],
        constraints=test_problem2["constraints"],
        difficulty=test_problem2["difficulty"],
        time_limit=test_problem2["time_limit"],
        memory_limit=test_problem2["memory_limit"],
        topics=test_problem2["topics"],
        test_cases=test_problem2["test_cases"]
    )

    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    problem1 = data[0]
    assert problem1["title"] == test_problem["title"]
    assert problem1["description"] == test_problem["description"]
    assert problem1["constraints"] == test_problem["constraints"]
    assert problem1["difficulty"] == test_problem["difficulty"]
    assert problem1["time_limit"] == test_problem["time_limit"]
    assert problem1["memory_limit"] == test_problem["memory_limit"]
    assert problem1["topics"] == test_problem["topics"]
    assert problem1["test_cases"] == test_problem["test_cases"]

    problem2 = data[1]
    assert problem2["title"] == test_problem2["title"]
    assert problem2["description"] == test_problem2["description"]
    assert problem2["constraints"] == test_problem2["constraints"]
    assert problem2["difficulty"] == test_problem2["difficulty"]
    assert problem2["time_limit"] == test_problem2["time_limit"]
    assert problem2["memory_limit"] == test_problem2["memory_limit"]
    assert problem2["topics"] == test_problem2["topics"]
    assert problem2["test_cases"] == test_problem2["test_cases"]

def test_get_problems_returns_right_topic_values(client, test_problem):
    add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topics=test_problem["topics"],
        test_cases=test_problem["test_cases"]
    )

    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    problem = data[0]
    assert problem["topics"] == test_problem["topics"]
    assert isinstance(problem["topics"], list)

def test_get_problems_id_returns_correct_problem(client, test_problem):
    problem_id = add_test_problem(
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topics=test_problem["topics"],
        test_cases=test_problem["test_cases"]
    )

    response = client.get(f"/api/problems/{problem_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_problem["title"]
    assert data["description"] == test_problem["description"]
    assert data["constraints"] == test_problem["constraints"]
    assert data["difficulty"] == test_problem["difficulty"]
    assert data["time_limit"] == test_problem["time_limit"]
    assert data["memory_limit"] == test_problem["memory_limit"]
    assert data["topics"] == test_problem["topics"]
    assert data["test_cases"] == test_problem["test_cases"]

def test_get_problems_id_returns_404_for_nonexistent_problem(client):
    response = client.get("/api/problems/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Problem not found"
