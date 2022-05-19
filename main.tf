terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  shared_credentials_file = "./credentials"
}


module "chatterbox-api" {
  # changed module from container to template which gives us an aws_launch_template
  source = "git::https://github.com/CSSE6400/terraform//template"

  image = "ghcr.io/csse6400/scalability-jamilboashash:main"
  instance_type = "c4.large"

  environment = {}
  ports = {
    "80" = "5000"
  }

  github_user = var.github_user
  github_pat = var.github_pat

  storage_size = 40

  # changed .name to .id as the launch_template needs ids
  security_groups = [aws_security_group.chatterbox-api.id]

  tags = {
    Name = "chatterbox-api"
  }
}

resource "aws_instance" "chatterbox-api" {
#  ami = "ami-0a8b4cd432b1c3063"
  instance_type = "c4.large"
  security_groups = [aws_security_group.chatterbox-api.name]

  launch_template {
    id = module.chatterbox-api.id
    version = "$Latest"
  }

  tags = {
    Name = "chatterbox"
  }
}

# generates the api.txt with the APIs URL
resource "local_file" "url" {
  content = aws_instance.chatterbox-api.public_ip
  filename = "./api.txt"
}


resource "aws_security_group" "chatterbox-api" {
  name = "chatterbox-api"
  description = "Chatterbox server SSH access and API endpoint HTTP access"
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

