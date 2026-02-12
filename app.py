def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    print("Test Passed!")

if __name__ == "__main__":
    print(f"Result: {add(10, 5)}")
    test_add()
