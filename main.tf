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
  region = "us-west-2"
  shared_credentials_file = "./credentials"
}

locals {
  login = var.github_pat != "" ? "echo ${var.github_pat} | docker login ghcr.io -u ${var.github_user} --password-stdin" : ""
  user_data = <<-EOT
#!/bin/bash
yum update -y
yum install -y docker
service docker start
systemctl enable docker
usermod -a -G docker ec2-user
${local.login}
docker run --hostname $(ec2-metadata -p | cut -f 2 -d' ') ${local.environment} ${local.ports} ${local.image}
  EOT
}

resource "aws_launch_template" "template" {
  image_id = local.ami
  instance_type = local.instance_type
  user_data = base64encode(local.user_data)
  vpc_security_group_ids = local.security_groups

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      delete_on_termination = true
      volume_size = var.storage_size
    }
  }

  iam_instance_profile {
    name = var.iam_role
  }

  tag_specifications {
    resource_type = "instance"

    tags = local.tags
  }

#  tags = {
#    Name = "chatterbox-api"
#  }
}




# attempt 2 --------------------------------------------------------------
#module "chatterbox-api" {
#
#  source = "git::https://github.com/CSSE6400/scalability-jamilboashash"
#
#  image = "ghcr.io/csse6400/scalability-jamilboashash:main"
#  instance_type = "t2.large"
#
##  environment = {
##    ENV_VAR="value"
##  }
#
#  ports = {
#    "80" = "5000"
#  }
#
##  security_groups = [aws_security_group.chatterbox-api.name]
#
#  tags = {
#    Name = "chatterbox-api"
#  }
#}
#
#
#resource "local_file" "url" {
#  content = module.chatterbox-api.public_ip
#  filename = "./api.txt"
#}


# attempt 1 -----------------------------------------------------------
#terraform {
#  required_providers {
#    aws = {
#      source = "hashicorp/aws"
#      version = "~> 3.0"
#    }
#    github = {
#
#    }
#  }
#}
#
## Configure the AWS Provider
#provider "aws" {
#  region = "us-west-2"
#  shared_credentials_file = "./credentials"
#}
#
#resource "aws_instance" "chatterbox-api" {
#  ami = "ami-0a8b4cd432b1c3063"
#  instance_type = "t2.large"
#  security_groups = [aws_security_group.chatterbox-api.name]
#
#  tags = {
#    Name = "chatterbox"
#  }
#}
#
## generates the api.txt with the APIs URL
#resource "local_file" "url" {
#  content = aws_instance.chatterbox-api.public_ip
#  filename = "./api.txt"
#}
#
#resource "random_string" "s3-bucket" {
#  length = 16
#  special = false
#  upper = false
#}
#
#resource "aws_s3_bucket" "bucket" {
#  bucket = "my-bucket-${random_string.s3-bucket.result}"
#}
#
#
#variable "github_pat" {
#  description = "A personal access token with read:packages permissions"
#  type = string
#}
#
#
#resource "aws_security_group" "chatterbox-api" {
#  name = "chatterbox-api"
#  description = "Chatterbox server SSH access and API endpoint HTTP access"
#  ingress {
#    from_port = 80
#    to_port = 80
#    protocol = "tcp"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#  ingress {
#    from_port = 22
#    to_port = 22
#    protocol = "tcp"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#  egress {
#    from_port = 0
#    to_port = 0
#    protocol = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#}
#
#
#resource "aws_db_instance" "chatterbox-database" {
#  allocated_storage = 20
#  max_allocated_storage = 1000
#  engine = "mysql"
#  engine_version = "8.0.27"
#  instance_class = "db.t2.micro"
#  name = "todoapp"
#  username = "todoapp"
##  password = local.password
#  parameter_group_name = "default.mysql8.0"
#  skip_final_snapshot = true
#  vpc_security_group_ids = [aws_security_group.chatterbox-api.name]
#  publicly_accessible = true
#  tags = {
#    Name = "chatterbox-database"
#  }
#}