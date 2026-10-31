# L6_L7_41 - Laundry Service

## Lab 6: Code and Branch Coverage

### Application

`laundry_service.py` provides extra-weight pricing, order acceptance checks, and drop-off cutoff status. The Lab 6 test suites are separate from the starter `test_laundry_service.py` file.

### Test suites

| File | Focus | Verified result |
|------|-------|-----------------|
| `CodeCoverageTest_PES2UG24CS107_application.py` | Statement coverage and input validation | 18 passed; 100% statement coverage |
| `BranchCoverageTest_PES2UG24CS107_application.py` | Decision branches and boundaries | 32 passed; 100% statement coverage and 100% branch coverage |

Coverage is measured for `laundry_service.py` only. The branch run recorded 37 statements and 26 branches, with 0 missing statements and 0 partial branches.

### Run the code coverage suite

From this `Lab 6` directory, install the test tools if needed and run:

```shell
python -m pip install pytest coverage
python -m coverage erase
python -m coverage run --source=laundry_service -m pytest -q CodeCoverageTest_PES2UG24CS107_application.py
python -m coverage report -m
```

Verified output: 18 passed; `laundry_service.py` 37/37 statements, 100% coverage.

### Run the branch coverage suite

```shell
python -m coverage erase
python -m coverage run --branch --source=laundry_service -m pytest -q BranchCoverageTest_PES2UG24CS107_application.py
python -m coverage report -m
```

Verified output: 32 passed; `laundry_service.py` 37/37 statements and 26/26 branches, 100% coverage.

The two commands are independent; each starts with `coverage erase` so the report reflects only the selected suite.

### Screenshot and PDF status

The verified results are included as text in `Lab6_Output_Screenshots_PES2UG24CS107.pdf`. The `screenshots` folder is reserved for the two terminal captures requested by the handout, but genuine terminal screenshots were not available from this execution environment. No simulated screenshots are included.
