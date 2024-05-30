data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "dynamo_db_delete" {
  statement {
    actions   = ["dynamodb:DeleteItem"]
    resources = ["arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}", "arn:aws:dynamodb:*:*:table/${var.table_name}/*"]
  }
}

data "aws_iam_policy_document" "dynamo_db_write" {
  statement {
    actions   = ["dynamodb:PutItem"]
    resources = ["arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}", "arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}/*"]
  }
}

data "aws_iam_policy_document" "dynamo_db_update" {
  statement {
    actions   = ["dynamodb:UpdateItem"]
    resources = ["arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}", "arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}/*"]
  }
}

data "aws_iam_policy_document" "dynamo_db_read" {
  statement {
    actions = ["dynamodb:GetItem"]
    resources = ["arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}", "arn:aws:dynamodb:*:${data.aws_caller_identity.current.account_id}:table/${var.table_name}/*"]
  }
}
