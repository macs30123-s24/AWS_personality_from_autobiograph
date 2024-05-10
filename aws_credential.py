import os

def rewrite_aws_credentials(input_string):
    # Path to the AWS credentials file
    aws_credentials_path = os.path.expanduser("~/.aws/credentials")

    # Check if the credentials file exists
    if os.path.exists(aws_credentials_path):
        # Open the file in write mode to overwrite its contents
        with open(aws_credentials_path, 'w') as file:
            # Write the input string to the file
            file.write(input_string)
        print("AWS credentials have been updated.")
    else:
        print("AWS credentials file not found.")

def main():
    # Prompt the user for input
    input_string = input("Enter the content to write to ~/.aws/credentials:\n")

    # Rewrite the AWS credentials file
    rewrite_aws_credentials(input_string)

if __name__ == "__main__":
    main()
