import boto3
import zipfile
# Initialize the Lambda client
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='LabRole')

# Specify the function name, handler, and role
function_name = 'process_chunk_layer'
handler = 'lambda_function.lambda_handler'

# Specify the path to your lambda_function.py file
with zipfile.ZipFile('lambda_function.zip', 'w') as z:
    z.write('lambda_function.py')

with open('lambda_function.zip', 'rb') as file:
    code = file.read()

# Create the Lambda function
try:
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.9',
        Role=role['Role']['Arn'],
        Handler=handler,
        Code=dict(ZipFile=code),
        Timeout=300
    )
except lambda_client.exceptions.ResourceConflictException:
    # If function already exists, update it based on zip
    # file contents
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=code
    )
import time

while True:
    function_state = lambda_client.get_function(FunctionName=function_name)['Configuration']['State']
    if function_state == 'Active':
        break
    else:
        print("Function is still creating, waiting for 10 seconds...")
        time.sleep(3)

layer_arns = ['arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-transformers:12',
              'arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-numpy:17']

# Update the Lambda function configuration to add layers
response = lambda_client.update_function_configuration(
    FunctionName=function_name,
    Layers=layer_arns
)
print(response)
