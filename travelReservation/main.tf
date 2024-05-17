# DynamoDB Tables
module "hotels_db" {
  source          = "./modules/dynamodb"
  table_name      = var.hotels_db_name
  hash_key        = var.hotels_hash_key
  hash_key_type   = var.hash_key_type
  additional_tags = var.hotels_db_additional_tags
}

module "flights_db" {
  source          = "./modules/dynamodb"
  table_name      = var.flights_db_name
  hash_key        = var.flights_hash_key
  hash_key_type   = var.hash_key_type
  additional_tags = var.flights_db_additional_tags
}

module "cars_db" {
  source          = "./modules/dynamodb"
  table_name      = var.cars_db_name
  hash_key        = var.cars_hash_key
  hash_key_type   = var.hash_key_type
  additional_tags = var.cars_db_additional_tags
}

# Reserve Hotel function
module "reserve_hotel_lambda" {
  source         = "./modules/lambda"
  function_name  = "ReserveHotel"
  lambda_handler = "reservehotel.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = module.hotels_db.name
  }
}

module "hotel_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "hotel_dynamo_db"
  table_name = module.hotels_db.name
  available_table = var.available_hotels_db_name
}

resource "aws_iam_role_policy_attachment" "reserve_hotel_lambda_dynamo_db_write" {
  role       = module.reserve_hotel_lambda.function_role_name
  policy_arn = module.hotel_iam_policies.dynamo_db_write
}

resource "aws_iam_role_policy_attachment" "reserve_hotel_lambda_dynamo_db_update" {
  role       = module.reserve_hotel_lambda.function_role_name
  policy_arn = module.hotel_iam_policies.dynamo_db_update
}

# Reserve Flight Function
module "reserve_flight_lambda" {
  source         = "./modules/lambda"
  function_name  = "ReserveFlight"
  lambda_handler = "reserveflight.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = module.flights_db.name
  }
}

module "flight_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "flight_dynamo_db"
  table_name = module.flights_db.name
  available_table = var.available_flights_db_name
}

resource "aws_iam_role_policy_attachment" "reserve_flight_lambda_dynamo_db_write" {
  role       = module.reserve_flight_lambda.function_role_name
  policy_arn = module.flight_iam_policies.dynamo_db_write
}

resource "aws_iam_role_policy_attachment" "reserve_flight_lambda_dynamo_db_update" {
  role       = module.reserve_flight_lambda.function_role_name
  policy_arn = module.flight_iam_policies.dynamo_db_update
}

# Reserve Car Function
module "reserve_car_lambda" {
  source         = "./modules/lambda"
  function_name  = "ReserveCar"
  lambda_handler = "reservecar.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = module.cars_db.name
  }
}

module "car_iam_policies" {
  source     = "./modules/iam-policies"
  name       = "car_dynamo_db"
  table_name = module.cars_db.name
  available_table = var.available_cars_db_name
}

resource "aws_iam_role_policy_attachment" "reserve_car_lambda_dynamo_db_write" {
  role       = module.reserve_car_lambda.function_role_name
  policy_arn = module.car_iam_policies.dynamo_db_write
}

resource "aws_iam_role_policy_attachment" "reserve_car_lambda_dynamo_db_update" {
  role       = module.reserve_car_lambda.function_role_name
  policy_arn = module.car_iam_policies.dynamo_db_update
}

# Check Hotel Function
module "check_hotel_lambda" {
  source         = "./modules/lambda"
  function_name  = "CheckHotel"
  lambda_handler = "checkhotel.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = "AvailableHotels"
  }
}

resource "aws_iam_role_policy_attachment" "check_hotel_lambda_dynamo_db_read" {
  role       = module.check_hotel_lambda.function_role_name
  policy_arn = module.hotel_iam_policies.dynamo_db_read
}

# Check Car Function
module "check_car_lambda" {
  source         = "./modules/lambda"
  function_name  = "CheckCar"
  lambda_handler = "checkcar.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = "AvailableCars"
  }
}

resource "aws_iam_role_policy_attachment" "check_car_lambda_dynamo_db_read" {
  role       = module.check_car_lambda.function_role_name
  policy_arn = module.car_iam_policies.dynamo_db_read
}

# Check Flight Function
module "check_flight_lambda" {
  source         = "./modules/lambda"
  function_name  = "CheckFlight"
  lambda_handler = "checkflight.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = "AvailableFlights"
  }
}

resource "aws_iam_role_policy_attachment" "check_flight_lambda_dynamo_db_read" {
  role       = module.check_flight_lambda.function_role_name
  policy_arn = module.flight_iam_policies.dynamo_db_read
}

# Cancel Hotel Function
module "cancel_hotel_lambda" {
  source         = "./modules/lambda"
  function_name  = "CancelHotel"
  lambda_handler = "cancelhotel.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = module.hotels_db.name
  }
}

resource "aws_iam_role_policy_attachment" "cancel_hotel_lambda_dynamo_db_write" {
  role       = module.cancel_hotel_lambda.function_role_name
  policy_arn = module.hotel_iam_policies.dynamo_db_write
}

resource "aws_iam_role_policy_attachment" "cancel_hotel_lambda_dynamo_db_delete" {
  role       = module.cancel_hotel_lambda.function_role_name
  policy_arn = module.hotel_iam_policies.dynamo_db_delete
}

# Cancel Flight Function
module "cancel_flight_lambda" {
  source         = "./modules/lambda"
  function_name  = "CancelFlight"
  lambda_handler = "cancelflight.lambda_handler"
  environment_variables = {
    "TABLE_NAME" = module.flights_db.name
  }
}

resource "aws_iam_role_policy_attachment" "cancel_flight_lambda_dynamo_db_delete" {
  role       = module.cancel_flight_lambda.function_role_name
  policy_arn = module.flight_iam_policies.dynamo_db_delete
}

resource "aws_iam_role_policy_attachment" "cancel_flight_lambda_dynamo_db_write" {
  role       = module.cancel_flight_lambda.function_role_name
  policy_arn = module.flight_iam_policies.dynamo_db_write
}

# Step Function
module "step_function" {
  source = "terraform-aws-modules/step-functions/aws"

  name = "Travel_Reservation"

  definition = templatefile("${path.module}/state-machine/reservation.asl.json", {
    CHECK_FLIGHT_FUNCTION_ARN   = module.check_flight_lambda.function_arn,
    CHECK_HOTEL_FUNCTION_ARN    = module.check_hotel_lambda.function_arn,
    CHECK_CAR_FUNCTION_ARN      = module.check_car_lambda.function_arn,
    RESERVE_HOTEL_FUNCTION_ARN  = module.reserve_hotel_lambda.function_arn,
    RESERVE_FLIGHT_FUNCTION_ARN = module.reserve_flight_lambda.function_arn,
    CANCEL_HOTEL_FUNCTION_ARN   = module.cancel_hotel_lambda.function_arn,
    RESERVE_CAR_FUNCTION_ARN    = module.reserve_car_lambda.function_arn,
    CANCEL_FLIGHT_FUNCTION_ARN  = module.cancel_flight_lambda.function_arn,
  })

  service_integrations = {
    lambda = {
      lambda = [
        module.reserve_hotel_lambda.function_arn,
        module.reserve_flight_lambda.function_arn,
        module.reserve_car_lambda.function_arn,
        module.check_hotel_lambda.function_arn,
        module.check_flight_lambda.function_arn,
        module.check_car_lambda.function_arn,
        module.cancel_hotel_lambda.function_arn,
        module.cancel_flight_lambda.function_arn,
      ]
    }
  }
  type = "STANDARD"
}