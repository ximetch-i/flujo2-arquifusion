#!/usr/bin/env bash
set -euo pipefail
EXPECTED_ACCOUNT="107681881936"
ACTUAL_ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
if [[ "$ACTUAL_ACCOUNT" != "$EXPECTED_ACCOUNT" ]]; then
  echo "ERROR: credenciales apuntan a la cuenta $ACTUAL_ACCOUNT, se esperaba $EXPECTED_ACCOUNT" >&2
  exit 1
fi
aws configure set region us-east-1
serverless deploy --stage dev
