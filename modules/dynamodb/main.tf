resource "aws_dynamodb_table" "dynamodb" {
  name           = var.table_name
  hash_key       = var.hash_key
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = var.hash_key
    type = var.hash_key_type
  }

  tags = merge(
    var.additional_tags,
    {
      Deployer = "terraform"
    }
  )
}