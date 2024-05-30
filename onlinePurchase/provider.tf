terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider - West
provider "aws" {
  region = "us-east-1"
  alias  = "east"

  default_tags {
    tags = {
      Environment = "Test"
      Owner       = "Terraform"
      Pattern     = "SAGA"
    }
  }
}

# Configure the AWS Provider - East
provider "aws" {
  region = "us-west-1"
  alias  = "west"

  default_tags {
    tags = {
      Environment = "Test"
      Owner       = "Terraform"
      Pattern     = "SAGA"
    }
  }
}


