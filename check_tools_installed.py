import subprocess


def check_tool(name: str, check_cmd: list[str], success_msg: str, fail_msg: str):
    try:
        print(
            (
                "please install these tools using this cmd:"
                "uv pip install --system ruff pytest pylint mypy"
            )
        )
        result = subprocess.run(
            check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            print(f"✅ {success_msg}")
        else:
            print(f"⚠️ {fail_msg}")
    except FileNotFoundError:
        print(f"❌ {name} not found. Please install it.")


# Check uv
check_tool(
    "uv",
    ["uv", "--version"],
    "uv is installed.",
    "uv is installed but returned an error.",
)

# Check ruff
check_tool(
    "ruff",
    ["ruff", "--version"],
    "ruff is installed.",
    "ruff is installed but returned an error.",
)

# Check pytest
check_tool(
    "pytest",
    ["pytest", "--version"],
    "pytest is installed.",
    "pytest is installed but returned an error.",
)

# Check pylint
check_tool(
    "pylint",
    ["pylint", "--version"],
    "pylint is installed.",
    "pylint is installed but returned an error.",
)


# Check mypy strict mode
def check_mypy_strict():
    try:
        result = subprocess.run(
            ["mypy", "--strict", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print("✅ mypy is installed and --strict mode is supported.")
        else:
            print("⚠️ mypy is installed but --strict mode may not be configured correctly.")
    except FileNotFoundError:
        print("❌ mypy not found. Please install it.")


check_mypy_strict()
