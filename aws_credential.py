import os

def rewrite_aws_credentials(local_file_path, aws_credentials_path):
    try:
        # Read credentials from the local file
        with open(local_file_path, 'r') as local_file:
            credentials_content = local_file.read()

        # Write credentials to the AWS credentials file
        with open(aws_credentials_path, 'w') as aws_credentials_file:
            aws_credentials_file.write(credentials_content)

        print("AWS credentials updated successfully.")

    except FileNotFoundError:
        print("Error: Local file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Path to the local file containing credentials
    local_credentials_file = "credentials"

    # Path to the AWS credentials file
    aws_credentials_file = os.path.expanduser("~/.aws/credentials")

    # Rewrite AWS credentials
    rewrite_aws_credentials(local_credentials_file, aws_credentials_file)
