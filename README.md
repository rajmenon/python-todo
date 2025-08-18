
# Python Todo App - A Learning Project

This is a personal project to build a command-line todo application. The main goal is to practice and hone skills in modern Python development, including project structure, typing, testing, and tooling.

## Tech Stack & Concepts

This project is an exercise in using a modern Python stack:

*   **CLI Framework:** Typer is used for creating a clean, user-friendly command-line interface.
*   **Static Typing:** The codebase is fully typed and checked with Mypy in strict mode to catch errors before runtime.
*   **Code Quality:** Ruff handles both linting and formatting to ensure the code is consistent and readable.
*   **Testing:** Pytest is used for writing and running the test suite.
*   **Packaging:** The project is structured as an installable package using `pyproject.toml` and the `src` layout, which is a current best practice.

## Getting Started

## TODO:

## Usage

Once installed, you can use the `todo` command directly from your terminal, thanks to the entry script defined in `pyproject.toml`.

```bash
# See all available commands and options
todo --help
```

## Development

This project uses a suite of tools to ensure code quality.

*   **Run tests:**
    `pytest`
*   **Check for linting errors and format code:**
    `ruff check . && ruff format .`
*   **Run static type checking:**
    `mypy src`

## License

This project is licensed under the MIT License.
