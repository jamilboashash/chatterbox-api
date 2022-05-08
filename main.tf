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

resource "aws_instance" "chatterbox-api" {
  ami = "ami-0a8b4cd432b1c3063"
  instance_type = "t2.micro"

  tags = {
    Name = "chatterbox"
  }
}

resource "local_file" "url" {
  content = aws_instance.chatterbox-api.public_ip
  filename = "./api.txt"
}

#resource "random_string" "chatterbox-s3-bucket" {
#  length = 16
#  special = false
#  upper = false
#}
#
#resource "aws_s3_bucket" "bucket" {
#  bucket = "my-bucket-${random_string.chatterbox-s3-bucket.result}"
#}