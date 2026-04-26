#!/usr/bin/env bash
# Scaffold handler/service/repository/model for a new resource.
# Usage: bash scripts/new-resource.sh users
set -euo pipefail

N="$1"
T="$(echo "${N}" | sed 's/.*/\u&/' | sed 's/s$//')"  # users -> User

mkdir -p internal/{model,repository,service,handler}

cat > "internal/model/${N}.go" <<EOF
package model

import "time"

type ${T} struct {
    ID        string    \`db:"id" json:"id"\`
    Name      string    \`db:"name" json:"name"\`
    CreatedAt time.Time \`db:"created_at" json:"createdAt"\`
}
EOF

cat > "internal/repository/${N}.go" <<EOF
package repository

import (
    "context"
    "github.com/jmoiron/sqlx"
    m "yourmod/internal/model"
)

type ${T}Repo interface {
    Create(context.Context, *m.${T}) error
    FindByID(context.Context, string) (*m.${T}, error)
}

type ${N}Repo struct{ db *sqlx.DB }

func New${T}Repo(db *sqlx.DB) ${T}Repo { return &${N}Repo{db} }

func (r *${N}Repo) Create(ctx context.Context, x *m.${T}) error {
    return nil // TODO
}

func (r *${N}Repo) FindByID(ctx context.Context, id string) (*m.${T}, error) {
    return nil, nil // TODO
}
EOF

cat > "internal/service/${N}.go" <<EOF
package service

import (
    "context"
    m "yourmod/internal/model"
)

type ${T}Repository interface {
    Create(context.Context, *m.${T}) error
    FindByID(context.Context, string) (*m.${T}, error)
}

type ${T}Service struct{ repo ${T}Repository }

func New${T}Service(repo ${T}Repository) *${T}Service {
    return &${T}Service{repo: repo}
}

func (s *${T}Service) Create(ctx context.Context, x *m.${T}) error {
    return s.repo.Create(ctx, x)
}
EOF

echo "Scaffolded ${N} across model/repository/service. Add handler + routes manually."
