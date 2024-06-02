resource "aws_dynamodb_table" "user_accounts" {
  name           = "UserAccounts"
  hash_key       = "UserId"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "UserId"
    type = "S"
  }
}

resource "aws_dynamodb_table" "user_profiles" {
  name           = "UserProfiles"
  hash_key       = "UserId"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "UserId"
    type = "S"
  }
}

resource "aws_dynamodb_table" "user_configurations" {
  name           = "UserConfigurations"
  hash_key       = "UserId"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "UserId"
    type = "S"
  }
}

resource "aws_sns_topic" "admin_notifications" {
  name = "AdminNotifications"
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_policy" "lambda_policy" {
  name = "lambda_policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
        ],
        Effect   = "Allow",
        Resource = "*",
      },
      {
        Action = "ses:SendEmail",
        Effect = "Allow",
        Resource = "*",
      },
      {
        Action = [
          "s3:CreateBucket",
          "s3:DeleteBucket",
        ],
        Effect   = "Allow",
        Resource = "*",
      },
      {
        Action = "sns:Publish",
        Effect = "Allow",
        Resource = aws_sns_topic.admin_notifications.arn,
      },
      {
        Action = "logs:*",
        Effect = "Allow",
        Resource = "*",
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

locals {
  lambda_functions = {
    CreateUserAccount            = "create_user_account"
    SendVerificationEmail        = "send_verification_email"
    VerifyEmail                  = "verify_email"
    CreateUserProfile            = "create_user_profile"
    SendWelcomeEmail             = "send_welcome_email"
    ProvisionResources           = "provision_resources"
    DeleteUserAccount            = "delete_user_account"
    RevokeResources              = "revoke_resources"
    DeleteUserProfile            = "delete_user_profile"
  }
}

data "archive_file" "lambda_function_zips" {
  for_each = local.lambda_functions

  type        = "zip"
  source_dir  = "${path.module}/functions/${each.key}"
  output_path = "${path.module}/functions/${each.key}.zip"
}

resource "aws_lambda_function" "lambda_functions" {
  for_each = local.lambda_functions

  filename      = data.archive_file.lambda_function_zips[each.key].output_path
  function_name = each.value
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256(data.archive_file.lambda_function_zips[each.key].output_path)

  provisioner "local-exec" {
    command = "rm -f ${path.module}/functions/${each.key}.zip"
  }
}
data "local_file" "asl_definition" {
  filename = "state-machine/reservation.asl.json"
}

resource "aws_sfn_state_machine" "account_registration" {
  name     = "Account_Registration"
  role_arn = aws_iam_role.lambda_execution_role.arn

  definition = data.local_file.asl_definition.content
}

output "state_machine_arn" {
  value = aws_sfn_state_machine.account_registration.arn
}
