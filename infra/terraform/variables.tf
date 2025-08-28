variable "location" {
  description = "Azure region"
  type        = string
  default     = "Australia Southeast"
}

variable "db_password" {
  description = "PostgreSQL admin password"
  type        = string
  sensitive   = true
}