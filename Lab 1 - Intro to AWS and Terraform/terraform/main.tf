# IAM Role Policy Document
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Lambda Function Role
resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Lambda Function code
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../code/index.py"
  output_path = "lambda_function.zip"
}

# Lambda Function
resource "aws_lambda_function" "lambda_function" {
  provider          = aws
  function_name     = var.function_name
  role              = aws_iam_role.iam_for_lambda.arn
  handler           = "index.handler"
  architectures     = ["x86_64"]
  timeout           = 30
  runtime           = "python3.13"
  filename          = "lambda_function.zip"
  source_code_hash  = data.archive_file.lambda.output_base64sha256

  lifecycle {
    ignore_changes  = [source_code_hash]
  }
}

# Lambda Function URL
resource "aws_lambda_function_url" "this" {
  function_name      = aws_lambda_function.lambda_function.function_name
  authorization_type = "NONE"
}
