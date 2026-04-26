.PHONY: build run test lint fmt tidy clean docker-build

BINARY_NAME ?= api
BUILD_DIR   := ./build
MAIN_PATH   := ./cmd/api

build:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)

build-linux:
	GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/$(BINARY_NAME)-linux $(MAIN_PATH)

run:
	go run $(MAIN_PATH)

dev:
	air -c .air.toml

test:
	go test -race -shuffle=on ./...

test-coverage:
	go test -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

lint:
	golangci-lint run ./...

fmt:
	gofmt -s -w .
	goimports -w .

tidy:
	go mod tidy
	go mod verify

clean:
	rm -rf $(BUILD_DIR) coverage.out coverage.html

docker-build:
	docker build -t $(BINARY_NAME):latest .

docker-run:
	docker run --rm -p 8080:8080 $(BINARY_NAME):latest
