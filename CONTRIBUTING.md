# Contributing to OSINT Agent Network

Thank you for your interest in contributing to the OSINT Agent Network (OAN)! We welcome contributions from the community to improve the multi-agent framework, enhance data collection sources, and optimize our LLM reasoning pipelines.

## Getting Started

1. **Fork the Repository**: Click the 'Fork' button at the top right of this page.
2. **Clone your Fork**: `git clone https://github.com/YOUR_USERNAME/osint-agent-network.git`
3. **Set up the Environment**: Create a virtual environment and install dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Create a Branch**: Create a new branch for your feature or bugfix.
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

- We follow **PEP 8** standards.
- Use **Type Hints** for all function arguments and return values.
- Ensure asynchronous code uses `async`/`await` properly.
- Write docstrings for all classes and complex methods.

## Testing

Before submitting a Pull Request, ensure all tests pass:

```bash
pytest tests/
```

If you are adding a new feature, please include corresponding unit tests in the `tests/` directory.

## Pull Request Process

1. Commit your changes with descriptive messages (we recommend Conventional Commits format).
2. Push your branch to your fork.
3. Open a Pull Request against the `main` branch of this repository.
4. Provide a clear description of the problem solved or feature added.
5. Wait for review from the maintainers.

## Issues and Feature Requests

If you find a bug or have an idea for a new feature, please open an issue in the GitHub issue tracker. Use the provided templates if available.

Thank you for making OAN better!
