PORT_REGEX := ^[0-9]+([.][0-9]+)?$
EXT_NAME:=com.github.zakuciael.ulauncher-jetbrains-reloaded
EXT_DIR:=$(shell pwd)

.PHONY: help link unlink deps start dev
.DEFAULT_GOAL := help

link: ## Symlink the project source directory with Ulauncher extensions dir.
	@ln -s ${EXT_DIR} ~/.local/share/ulauncher/extensions/${EXT_NAME}

unlink: ## Unlink extension from Ulauncher
	@rm -r ~/.local/share/ulauncher/extensions/${EXT_NAME}

deps: ## Install Python Dependencies
	@pip install -r requirements.txt

dev: ## Runs ulauncher on development mode
	ulauncher -v --dev --no-extensions  |& grep "${EXT_NAME}"

start: ## Starts extension backend for development
ifeq ($(shell echo ${PORT} | egrep "${PORT_REGEX}"),)
	@echo "Port is not an number"
else
	VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:${PORT}/${EXT_NAME} python3 ~/.local/share/ulauncher/extensions/${EXT_NAME}/main.py
endif

help: ## Show help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
