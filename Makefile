PYTHON_CMD_PREFIX := `bash ./get_env_command_prefix.sh`

.PHONY: black-check
black-check:
	${PYTHON_CMD_PREFIX} black --check src tests
	@echo ""

.PHONY: black
black:
	${PYTHON_CMD_PREFIX} black src tests
	@echo ""

.PHONY: flake8
flake8:
	${PYTHON_CMD_PREFIX} flake8 src tests
	@echo ""

.PHONY: isort-check
isort-check:
	${PYTHON_CMD_PREFIX} isort --check-only src tests
	@echo ""

.PHONY: isort
isort:
	${PYTHON_CMD_PREFIX} isort src tests
	@echo ""

.PHONY: mypy
mypy:
	${PYTHON_CMD_PREFIX} mypy src
	@echo ""

.PHONY: test
test:
	${PYTHON_CMD_PREFIX} pytest tests --cov=src --cov-report term-missing --durations 5
	@echo ""

.PHONY: format
format:
	@echo "[black]"
	$(MAKE) black
	@echo "[isort]"
	$(MAKE) isort

.PHONY: lint
lint:
	@echo "[black-check]"
	$(MAKE) black-check
	@echo "[isort-check]"
	$(MAKE) isort-check
	@echo "[flake8]"
	$(MAKE) flake8
	@echo "[mypy]"
	$(MAKE) mypy

.PHONY: test-all
test-all:
	@echo "########"
	@echo "# lint #"
	@echo "########"
	$(MAKE) lint
	@echo "########"
	@echo "# test #"
	@echo "########"
	$(MAKE) test
