terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  shared_credentials_file = "./credentials"
}

#resource "local_file" "url" {
#  content = # some resource output here
#  filename = "./api.txt"
#}
