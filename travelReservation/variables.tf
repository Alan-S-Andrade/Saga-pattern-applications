variable "hotels_db_name" {
  type    = string
  default = "Hotels"
}

variable "flights_db_name" {
  type    = string
  default = "Flights"
}

variable "cars_db_name" {
  type    = string
  default = "Cars"
}

variable "available_cars_db_name" {
  type    = string
  default = "AvailableCars"
}

variable "available_hotels_db_name" {
  type    = string
  default = "AvailableHotels"
}

variable "available_flights_db_name" {
  type    = string
  default = "AvailableFlights"
}

variable "cars_hash_key" {
  type    = string
  default = "Model"
}

variable "hotels_hash_key" {
  type    = string
  default = "Name"
}

variable "flights_hash_key" {
  type    = string
  default = "Airline"
}

variable "hash_key_type" {
  type    = string
  default = "S"
}

variable "hotels_db_additional_tags" {
  type = map(string)
  default = {
    Name = "Hotels"
    AvailableTable = "AvailableHotels"
  }
}

variable "flights_db_additional_tags" {
  type = map(string)
  default = {
    Name = "Flights"
    AvailableTable = "AvailableFlights"
  }
}

variable "cars_db_additional_tags" {
  type = map(string)
  default = {
    Name = "Cars"
    AvailableCars = "AvailableCars"
  }
}