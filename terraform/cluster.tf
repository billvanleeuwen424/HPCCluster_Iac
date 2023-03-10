provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "my_ssh_key" {
  key_name   = "aws-cluster-key"
  public_key = file("~/.ssh/aws-cluster-key.pub")
}

resource "aws_vpc" "cluster_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "MyVPC"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.cluster_vpc.id
  cidr_block              = "10.0.0.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.cluster_vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "PrivateSubnet"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.cluster_vpc.id

  tags = {
    Name = "IGW"
  }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.cluster_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "PublicRouteTable"
  }
}

resource "aws_route_table_association" "public_route_table_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_security_group" "public_security_group" {
  name_prefix = "PublicSecurityGroup"
  vpc_id      = aws_vpc.cluster_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks = [aws_vpc.cluster_vpc.cidr_block]
  }
}

resource "aws_security_group" "private_security_group" {
  name_prefix = "PrivateSecurityGroup"
  vpc_id      = aws_vpc.cluster_vpc.id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.public_security_group.id]
  }
}

resource "aws_instance" "public_instance" {
  ami                    = "ami-0557a15b87f6559cf"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.public_security_group.id]
  key_name               = "aws-cluster-key"

  tags = {
    Name = "PublicInstance"
  }
}

resource "aws_instance" "private_instance" {
  count                  = 2
  ami                    = "ami-0557a15b87f6559cf"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private_subnet.id
  vpc_security_group_ids = [aws_security_group.private_security_group.id]
  key_name               = "aws-cluster-key"

  tags = {
    Name = "PrivateInstance-${count.index}"
  }
}

output "public_instance_public_ip" {
  value = aws_instance.public_instance.public_ip
}