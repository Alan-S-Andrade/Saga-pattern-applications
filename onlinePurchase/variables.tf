variable "regions" {
  type    = list(string)
  default = ["us-east-1", "us-west-1"]
}

variable "users_db_name" {
  type    = string
  default = "UserInformation"
}