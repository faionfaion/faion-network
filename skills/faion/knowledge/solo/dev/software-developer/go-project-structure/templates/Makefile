# Makefile — standard Go project build automation
# Usage: make build | run | test | lint | clean

BINARY_NAME := api
BUILD_DIR   := ./build
MAIN_PATH   := ./cmd/api

.PHONY: build build-linux run dev test test-coverage lint fmt tidy clean docker-build docker-run

build:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)

build-linux:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/$(BINARY_NAME)-linux $(MAIN_PATH)

run:
	go run $(MAIN_PATH)

dev:
	air -c .air.toml

test:
	go test -v ./...

test-coverage:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

lint:
	golangci-lint run ./...

fmt:
	gofmt -s -w .
	goimports -w . 2>/dev/null || true

tidy:
	go mod tidy
	go mod verify

clean:
	rm -rf $(BUILD_DIR) coverage.out coverage.html

docker-build:
	docker build -t $(BINARY_NAME):latest .

docker-run:
	docker run -p 8080:8080 $(BINARY_NAME):latest
