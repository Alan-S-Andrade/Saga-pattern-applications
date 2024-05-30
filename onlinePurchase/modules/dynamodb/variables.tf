variable "table_name" {
  type = string
}

variable "hash_key" {
  type = string
}

variable "hash_key_type" {
  type    = string
  default = "S"
}

variable "additional_tags" {
  type        = map(string)
  description = "Additional resource tags"
  default     = {}
}
