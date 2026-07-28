.PHONY: help

# ROOT_DIR is the path of the makefile (including trailing slash)
ROOT_DIR := $(patsubst %/,%,$(dir $(realpath $(lastword $(MAKEFILE_LIST)))))
PROJECT_NAME := $(notdir $(ROOT_DIR))
BADGE_SIM_DIR := ~/code/badge-2024-software/sim/apps
DEST_DIR := $(BADGE_SIM_DIR)/$(PROJECT_NAME)

help: ## Display this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ General
run: ## Run this app on the badge simulator
	@echo "Syncing app to $(DEST_DIR)"
	@mkdir -p $(DEST_DIR)
	@rsync -a --delete --exclude='.git' --exclude='makefile' $(ROOT_DIR)/ $(DEST_DIR)/ 
	@cd $(BADGE_SIM_DIR)/.. && pipenv run python run.py
	
