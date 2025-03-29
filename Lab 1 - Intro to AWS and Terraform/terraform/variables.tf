variable "aws_region" {
  description = "The AWS region to use"
  type        = string
  default     = "us-west-2"
}

variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
  default     = "lambda-lab-function"
}


