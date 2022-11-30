## 1.2.0 (2022-10-03)

### Feat

- restructure `presign_post` response to be a list of dictionaries, move key as `name` field of the dictionary

### Refactor

- **services.s3.presigner**: get value by key with method `get()` instead of doing it directly

## 1.1.0 (2022-08-25)

### Feat

- **events**: configure `__all__` in `__init__.py`
- add SqsEvent model

### Tests

- add test suite for SqsEvent models

### Chore

- **gitignore**: exclude coverage report folder
- **task**: add commands for tests

## 1.0.0 (2022-08-19)

### Feat

- reset semver to 0.0.0
- add GHA workflows to check code quality and bump semver
- init
- init Taskfile

### Fix

- **events.api_gateway**: handle `JSONDecodeError` when `body` is not json

### Refactor

- **events**: add `__init__.py` file
- move `models.events` to `events`

### Build

- remove `package` field from `pyproject.toml`
- rename `src` to `aws_lambda_powerlib`
- update `packages` property in `pyproject.toml`
- specify `src` folder as package

### Tests

- **events**: add simple test as a placeholder

### Docs

- **readme**: add installation instruction from private repository

### Chore

- add package `__version__.py` and link it to `commitizen` configuration
- **task**: add `build` command
- update gitignore
