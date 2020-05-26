
def pytest_addoption(parser):
    parser.addoption(
        "--address",
        action="append",
        default=[],
        help="list of tools addresses to pass to test functions",
    )

def pytest_generate_tests(metafunc):
    if "address" in metafunc.fixturenames:
        metafunc.parametrize("address", metafunc.config.getoption("address"))