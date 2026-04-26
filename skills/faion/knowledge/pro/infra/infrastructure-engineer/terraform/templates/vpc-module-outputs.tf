output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.this.cidr_block
}

output "public_subnet_ids" {
  description = "Map of AZ → public subnet ID"
  value       = { for az, s in aws_subnet.public : az => s.id }
}

output "private_subnet_ids" {
  description = "Map of AZ → private subnet ID"
  value       = { for az, s in aws_subnet.private : az => s.id }
}

output "data_subnet_ids" {
  description = "Map of AZ → data subnet ID"
  value       = { for az, s in aws_subnet.data : az => s.id }
}

output "public_subnet_ids_list" {
  description = "List of public subnet IDs (order matches var.azs)"
  value       = [for az in var.azs : aws_subnet.public[az].id]
}

output "private_subnet_ids_list" {
  description = "List of private subnet IDs (order matches var.azs)"
  value       = [for az in var.azs : aws_subnet.private[az].id]
}

output "data_subnet_ids_list" {
  description = "List of data subnet IDs (order matches var.azs)"
  value       = [for az in var.azs : aws_subnet.data[az].id]
}

output "nat_gateway_ids" {
  description = "Map of AZ → NAT Gateway ID"
  value       = { for az, ng in aws_nat_gateway.this : az => ng.id }
}

output "nat_public_ips" {
  description = "Map of AZ → NAT Gateway public IP"
  value       = { for az, eip in aws_eip.nat : az => eip.public_ip }
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.this.id
}
