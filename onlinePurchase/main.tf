# DynamoDB User Table
resource "aws_dynamodb_table" "user_info" {
  provider = aws.east

  name           = "UserInformation"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "username"

  attribute {
    name = "username"
    type = "S"
  }

  attribute {
    name = "password"
    type = "S"
  }

  attribute {
    name = "funds"
    type = "N"
  }

  global_secondary_index {
    name            = "PasswordIndex"
    hash_key        = "username"
    range_key       = "password"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "FundsIndex"
    hash_key        = "username"
    range_key       = "funds"
    projection_type = "ALL"
  }
}

resource "null_resource" "populate_dynamodb_credentials" {
  provisioner "local-exec" {
    command = <<EOF
      aws dynamodb put-item --table-name UserInformation --item '{ "username": { "S": "user1" }, "password": { "S": "password1" }, "funds": {"N": "0"}}'
      aws dynamodb put-item --table-name UserInformation --item '{ "username": { "S": "user2" }, "password": { "S": "password2" }, "funds": {"N": "100"}}'
      aws dynamodb put-item --table-name UserInformation --item '{ "username": { "S": "user3" }, "password": { "S": "password3" }, "funds": {"N": "200"}}'
    EOF
  }
}

# All store items
resource "aws_dynamodb_table" "items" {
  provider = aws.east

  name           = "Items"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product"

  attribute {
    name = "ID"
    type = "N"
  }

  attribute {
    name = "product"
    type = "S"
  }

  attribute {
    name = "cost"
    type = "N"
  }

  global_secondary_index {
    name            = "IDIndex"
    hash_key        = "product"
    range_key       = "ID"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "CostIndex"
    hash_key        = "product"
    range_key       = "cost"
    projection_type = "ALL"
  }
}

resource "null_resource" "populate_dynamodb_items" {
  provisioner "local-exec" {
    command = <<EOF
      aws dynamodb put-item --table-name Items --item '{ "ID": { "N": "1" }, "product": { "S": "Red Shoes" }, "cost": {"N": "20"} }'
      aws dynamodb put-item --table-name Items --item '{ "ID": { "N": "2" }, "product": { "S": "White Hat" }, "cost": {"N": "10"} }'
      aws dynamodb put-item --table-name Items --item '{ "ID": { "N": "3" }, "product": { "S": "Blue Shirt" }, "cost": {"N": "5"}}'
      aws dynamodb put-item --table-name Items --item '{ "ID": { "N": "4" }, "product": { "S": "Black Pants" }, "cost": {"N": "300"}}'
      aws dynamodb put-item --table-name Items --item '{ "ID": { "N": "5" }, "product": { "S": "Gray Jacket" }, "cost": {"N": "150"}}'
      aws dynamodb put-item --table-name Items --item '{ "ID": { "N": "6" }, "product": { "S": "Green Tie" }, "cost": {"N": "40"}}'
    EOF
  }
}

# Retail table for region 1
resource "aws_dynamodb_table" "stock_east" {
  provider = aws.east

  name           = "Stock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product"

  attribute {
    name = "product"
    type = "S"
  }

  attribute {
    name = "availabililty"
    type = "N"
  }

  global_secondary_index {
    name            = "AvailabilityIndex"
    hash_key        = "product"
    range_key       = "availabililty"
    projection_type = "ALL"
  }
}

# Retail table for region 2
resource "aws_dynamodb_table" "stock_west" {
  provider = aws.west

  name           = "Stock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product"

  attribute {
    name = "product"
    type = "S"
  }

  attribute {
    name = "availabililty"
    type = "N"
  }

  global_secondary_index {
    name            = "AvailabilityIndex"
    hash_key        = "product"
    range_key       = "availabililty"
    projection_type = "ALL"
  }
}

# Populate DynamoDB table in us-east-1
resource "null_resource" "populate_dynamodb_stock_us_east_1" {
  depends_on = [aws_dynamodb_table.stock_east]

  provisioner "local-exec" {
    command = <<EOF
      aws dynamodb put-item --region us-east-1 --table-name Stock --item '{ "product": { "S": "Red Shoes" }, "availability": { "N": "10" } }'
      aws dynamodb put-item --region us-east-1 --table-name Stock --item '{ "product": { "S": "White Hat" }, "availability": { "N": "0" } }'
      aws dynamodb put-item --region us-east-1 --table-name Stock --item '{ "product": { "S": "Green Tie" }, "availability": { "N": "5" } }'
    EOF
  }
}

# Populate DynamoDB table in us-west-1
resource "null_resource" "populate_dynamodb_stock_us_west_1" {
  depends_on = [aws_dynamodb_table.stock_west]

  provisioner "local-exec" {
    command = <<EOF
      aws dynamodb put-item --region us-west-1 --table-name Stock --item '{ "product": { "S": "Blue Shirt" }, "availability": { "N": "20" } }'
      aws dynamodb put-item --region us-west-1 --table-name Stock --item '{ "product": { "S": "Black Pants" }, "availability": { "N": "8" } }'
      aws dynamodb put-item --region us-west-1 --table-name Stock --item '{ "product": { "S": "Gray Jacket" }, "availability": { "N": "3" } }'
      aws dynamodb put-item --region us-west-1 --table-name Stock --item '{ "product": { "S": "Green Tie" }, "availability": { "N": "105" } }'
    EOF
  }
}

# user orders
resource "aws_dynamodb_table" "user_orders" {
  provider = aws.west

  name           = "Orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user"

  attribute {
    name = "user"
    type = "S"
  }

  attribute {
    name = "product"
    type = "S"
  }

  attribute {
    name = "availabililty"
    type = "N"
  }

  global_secondary_index {
    name            = "AvailabilityIndex"
    hash_key        = "user"
    range_key       = "availabililty"
    projection_type = "ALL"
  }
  
  global_secondary_index {
    name            = "ProductIndex"
    hash_key        = "user"
    range_key       = "product"
    projection_type = "ALL"
  }
}

# Login function
module "login_lambda" {
  source         = "./modules/lambda"
  function_name  = "Login"
  lambda_handler = "login.lambda_handler"
}

module "user_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "user_dynamo_db"
  table_name = "UserInformation"
}

resource "aws_iam_role_policy_attachment" "login_lambda_dynamo_db_read" {
  role       = module.login_lambda.function_role_name
  policy_arn = module.user_iam_policies.dynamo_db_read
}

# Check Item ID Function
module "check_item_id_lambda" {
  source         = "./modules/lambda"
  function_name  = "CheckItemId"
  lambda_handler = "checkitemid.lambda_handler"
}

module "items_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "items_dynamo_db"
  table_name = "Items"
}

resource "aws_iam_role_policy_attachment" "check_item_id_lambda_dynamo_db_read" {
  role       = module.check_item_id_lambda.function_role_name
  policy_arn = module.items_iam_policies.dynamo_db_read
}

# Get Item ID Function
module "get_item_id_lambda" {
  source         = "./modules/lambda"
  function_name  = "GetItemId"
  lambda_handler = "getitemid.lambda_handler"
}

resource "aws_iam_role_policy_attachment" "get_item_id_lambda_dynamo_db_read" {
  role       = module.get_item_id_lambda.function_role_name
  policy_arn = module.items_iam_policies.dynamo_db_read
}

# Get Close RG Function
module "get_close_rg_lambda" {
  source         = "./modules/lambda"
  function_name  = "GetCloseRG"
  lambda_handler = "getcloserg.lambda_handler"
}

# Region East Function
module "region_east_lambda" {
  source         = "./modules/lambda"
  function_name  = "RegionEast"
  lambda_handler = "regioneast.lambda_handler"
}

# Region West Function
module "region_west_lambda" {
  source         = "./modules/lambda"
  function_name  = "RegionWest"
  lambda_handler = "regionwest.lambda_handler"
}

# Check Availability Function
module "check_availability_lambda" {
  source         = "./modules/lambda"
  function_name  = "CheckAvailability"
  lambda_handler = "checkavailability.lambda_handler"
}

module "stock_east_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "stock_east_iam_policies"
  table_name = "Stock"
}

module "stock_west_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "stock_west_iam_policies"
  table_name = "Stock"
}

resource "aws_iam_role_policy_attachment" "check_availability_east_lambda_dynamo_db_read" {
  role       = module.check_availability_lambda.function_role_name
  policy_arn = module.stock_east_iam_policies.dynamo_db_read
}

resource "aws_iam_role_policy_attachment" "check_availability_west_lambda_dynamo_db_read" {
  role       = module.check_availability_lambda.function_role_name
  policy_arn = module.stock_west_iam_policies.dynamo_db_read
}

# Reserve Item Function
module "reserve_item_lambda" {
  source         = "./modules/lambda"
  function_name  = "ReserveItem"
  lambda_handler = "reserveitem.lambda_handler"
}

resource "aws_iam_role_policy_attachment" "reserve_item_east_lambda_dynamo_db_read" {
  role       = module.reserve_item_lambda.function_role_name
  policy_arn = module.stock_east_iam_policies.dynamo_db_read
}

resource "aws_iam_role_policy_attachment" "reserve_item_west_lambda_dynamo_db_read" {
  role       = module.reserve_item_lambda.function_role_name
  policy_arn = module.stock_west_iam_policies.dynamo_db_read
}

resource "aws_iam_role_policy_attachment" "reserve_item_east_lambda_dynamo_db_update" {
  role       = module.reserve_item_lambda.function_role_name
  policy_arn = module.stock_east_iam_policies.dynamo_db_update
}

resource "aws_iam_role_policy_attachment" "reserve_item_west_lambda_dynamo_db_update" {
  role       = module.reserve_item_lambda.function_role_name
  policy_arn = module.stock_west_iam_policies.dynamo_db_update
}

module "orders_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "orders_dynamo_db"
  table_name = "Orders"
}

resource "aws_iam_role_policy_attachment" "reserve_item_orders_dynamo_db_write" {
  role       = module.reserve_item_lambda.function_role_name
  policy_arn = module.orders_iam_policies.dynamo_db_write
}

# Check Money Function
module "check_money_lambda" {
  source         = "./modules/lambda"
  function_name  = "CheckMoney"
  lambda_handler = "checkmoney.lambda_handler"
}

resource "aws_iam_role_policy_attachment" "check_money_lambda_dynamo_db_read" {
  role       = module.check_money_lambda.function_role_name
  policy_arn = module.user_iam_policies.dynamo_db_read
}

# Return Item Function
module "return_item_lambda" {
  source         = "./modules/lambda"
  function_name  = "ReturnItem"
  lambda_handler = "returnitem.lambda_handler"
}

resource "aws_iam_role_policy_attachment" "return_item_east_lambda_dynamo_db_read" {
  role       = module.return_item_lambda.function_role_name
  policy_arn = module.stock_east_iam_policies.dynamo_db_read
}

resource "aws_iam_role_policy_attachment" "return_item_west_lambda_dynamo_db_read" {
  role       = module.return_item_lambda.function_role_name
  policy_arn = module.stock_west_iam_policies.dynamo_db_read
}

resource "aws_iam_role_policy_attachment" "return_item_east_lambda_dynamo_db_update" {
  role       = module.return_item_lambda.function_role_name
  policy_arn = module.stock_east_iam_policies.dynamo_db_update
}

resource "aws_iam_role_policy_attachment" "return_item_west_lambda_dynamo_db_update" {
  role       = module.return_item_lambda.function_role_name
  policy_arn = module.stock_west_iam_policies.dynamo_db_update
}

resource "aws_iam_role_policy_attachment" "return_item_orders_dynamo_db_delete" {
  role       = module.return_item_lambda.function_role_name
  policy_arn = module.orders_iam_policies.dynamo_db_delete
}

# Pay Function
module "pay_lambda" {
  source         = "./modules/lambda"
  function_name  = "Pay"
  lambda_handler = "pay.lambda_handler"
}

resource "aws_iam_role_policy_attachment" "pay_lambda_dynamo_db_read" {
  role       = module.pay_lambda.function_role_name
  policy_arn = module.user_iam_policies.dynamo_db_read
}

resource "aws_iam_role_policy_attachment" "update_lambda_dynamo_db_update" {
  role       = module.pay_lambda.function_role_name
  policy_arn = module.user_iam_policies.dynamo_db_update
}

# Step Function
module "step_function" {
  source = "terraform-aws-modules/step-functions/aws"

  name = "Online_Purchase"

  definition = templatefile("${path.module}/state-machine/reservation.asl.json", {
    CHECK_AVAILABILITY_FUNCTION_ARN   = module.check_availability_lambda.function_arn,
    CHECK_ITEM_ID_FUNCTION_ARN    = module.check_item_id_lambda.function_arn,
    CHECK_MONEY_FUNCTION_ARN       = module.check_money_lambda.function_arn,
    GET_CLOSE_RG_FUNCTION_ARN   = module.get_close_rg_lambda.function_arn,
    GET_ITEM_ID_FUNCTION_ARN    = module.get_item_id_lambda.function_arn,
    LOGIN_FUNCTION_ARN        = module.login_lambda.function_arn,
    PAY_FUNCTION_ARN          =  module.pay_lambda.function_arn,
    REGION_EAST_FUNCTION_ARN  = module.region_east_lambda.function_arn,
    REGION_WEST_FUNCTION_ARN  = module.region_west_lambda.function_arn,
    RESERVE_ITEM_FUNCTION_ARN  = module.reserve_item_lambda.function_arn,
    RETURN_ITEM_FUNCTION_ARN  = module.return_item_lambda.function_arn,
  })

  service_integrations = {
    lambda = {
      lambda = [
        module.check_availability_lambda.function_arn,
        module.check_item_id_lambda.function_arn,
        module.check_money_lambda.function_arn,
        module.get_close_rg_lambda.function_arn,
        module.get_item_id_lambda.function_arn,
        module.login_lambda.function_arn,
        module.pay_lambda.function_arn,
        module.region_east_lambda.function_arn,
        module.region_west_lambda.function_arn,
        module.reserve_item_lambda.function_arn,
        module.return_item_lambda.function_arn,
      ]
    }
  }
  type = "STANDARD"
}