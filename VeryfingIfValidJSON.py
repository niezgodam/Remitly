import json
import re
import argparse

class VeryfingIfValidJSON:

    def __init__(self,path) -> None:
        self.path = path
        self.json_data = None

    def loading_file(self):
        """
            Load the file and check that the file has been loaded and that the JSON format is correct.
        """
        try:
            # Attempt to open the file in read mode with UTF-8 encoding
            with open(self.path,'r',encoding='UTF-8') as file:
                try:
                    # Attempt to load JSON data from the file
                    self.json_data = json.load(file)     
                except ValueError as err:
                    # If JSON is not valid format, raise an exception
                    raise Exception("JSON is not valid format")

        except (FileNotFoundError): 
            # If the file is not found, raise an exception
            raise Exception("File loading error")
        
    def check_required_policy_properties(self):
        """
            Check if required properties 'PolicyName' and 'PolicyDocument' are present in the JSON data,
            and validate their formats.

            Requirements according to: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html
        """
        # Check if 'PolicyName' and 'PolicyDocument' are present in the JSON data
        if "PolicyName" not in self.json_data or "PolicyDocument" not in self.json_data:
            raise Exception("PolicyName or PolicyDocument not found in JSON")
        
        try: 
            # Attempt to load and dump 'PolicyDocument' to validate its JSON format
            json.loads(json.dumps(self.json_data["PolicyDocument"]))
        except (json.JSONDecodeError,TypeError):
            # If 'PolicyDocument' is not in JSON format, raise an exception
            raise Exception("PolicyDocument is not in JSON")

        policy_name = self.json_data["PolicyName"]

        # Checking if "PolicyName" is string
        if not isinstance(policy_name, str):
            raise Exception("PolicyName must be a string")
        
        # Setting pattern accoording to requirements
        pattern = r'[\w+=,.@-]+'
        match = re.fullmatch(pattern, policy_name)
        if not match or not (len(policy_name) >= 1 or not len(policy_name) <= 128):
            # If 'PolicyName' if it does not meet the requirements
            raise Exception("PolicyName is not string or it requirements not met")
        

    # Version check
    def check_validate_version(self):
        """
            Check if the 'Version' key is present in the 'PolicyDocument' and validates its presence.
        """

        self.check_required_policy_properties()
        # Check if 'Version' is present in 'PolicyDocument'
        if 'Version' not in self.json_data['PolicyDocument']:
            # If 'Version' is missing in 'PolicyDocument', raise an exception
            raise Exception('Version not in Policy Document')
        
    # Statement Check
    # Statement is required according to https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_statement.html
    def check_validate_statement(self):
        """
            Check if the 'Statement' key is present in the 'PolicyDocument'.
        """

        self.check_required_policy_properties()
        # Check if 'Statement' is present in 'PolicyDocument'
        if 'Statement' not in self.json_data['PolicyDocument']: 
            # If 'Statement' is missing in 'PolicyDocument', raise an exception
            raise Exception('Statement not in Policy Document')


    # Sid check
    def check_validate_sid(self):
        """
            Check if the 'Sid' keys in 'Statement' elements are valid according to AWS IAM specifications.
        """

        self.check_required_policy_properties()
        self.check_validate_statement()

        # Define pattern for 'Sid' validation according to https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_sid.html
        sid_pattern =re.compile(r'^[A-Za-z0-9]+$')

        # Check if 'Statement' is a list (multiple statements)
        if isinstance(self.json_data['PolicyDocument']['Statement'], list):
            # Iterate over each statement in the list
            for statement in self.json_data['PolicyDocument']['Statement']:
                if "Sid" in statement:
                    sid = statement['Sid']
                    # Validate 'Sid' format
                    if not sid_pattern.match(sid):
                        raise Exception("Invalid SID: The Sid element supports ASCII uppercase letters (A-Z), lowercase letters (a-z), and numbers (0-9)")
        else:
            # If 'Statement' is not a list (single statement), directly access it
            statement = self.json_data['PolicyDocument']['Statement']
            if "Sid" in statement:
                sid = statement['Sid']
                # Validate 'Sid' format
                if sid_pattern.match(sid) is None:
                    raise Exception("Invalid SID: The Sid element supports ASCII uppercase letters (A-Z), lowercase letters (a-z), and numbers (0-9)")

    # Effect check
    # Effect is required according to https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_effect.html
    def check_validate_effect(self):
        """
            Check if the 'Effect' key in the first 'Statement' element is valid according to AWS IAM specifications.
        """
        self.check_required_policy_properties()
        self.check_validate_statement()

        # Check if 'Effect' is present in the first 'Statement' element
        if 'Effect' in self.json_data['PolicyDocument']['Statement'][0]:
            effect = self.json_data['PolicyDocument']['Statement'][0]['Effect']
            # Validate 'Effect' value
            if effect != ("Allow" or "Deny"):
                raise Exception("Valid values for Effect are only: Allow and Deny")
        else:
            # If 'Effect' is not present in the first 'Statement' element, raise an exception
            raise Exception('Effect not in JSON')
    
    # Action check
    # Action is required according to https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_action.html
    def check_validate_action(self):
        """
            Check if the 'Action' or 'NotAction' keys are included in the first 'Statement' element,
            as required by AWS IAM specifications.
        """
        self.check_required_policy_properties()
        self.check_validate_statement()

        # Check if 'Action' or 'NotAction' is included in the first 'Statement' element
        if 'Action' not in self.json_data['PolicyDocument']['Statement'][0] and 'NotAction' not in self.json_data['PolicyDocument']['Statement'][0]:
            raise Exception("Action or NotAction must be included in Statement")
    
    # Resource check
    # Resource is required according to https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html
    def check_validate_resource(self):
        """
            Check if the 'Resource' or 'NotResource' keys are included in the first 'Statement' element,
            as required by AWS IAM specifications.
        """
        self.check_required_policy_properties()
        self.check_validate_statement()

        # Check if 'Resource' or 'NotResource' is included in the first 'Statement' element
        if 'Resource' in self.json_data['PolicyDocument']['Statement'][0] or 'NotResource' in self.json_data['PolicyDocument']['Statement'][0]:
            resource = self.json_data['PolicyDocument']['Statement'][0]['Resource']
            # Check if 'Resource' is not set to "*"
            if resource == "*":
                return False
            else:
                return True
        else:
            raise Exception("Resource or NotResource must be included in Statement")

    def main(self):
        try:
            self.loading_file()
            self.check_required_policy_properties()
            self.check_validate_version()
            self.check_validate_statement()
            self.check_validate_sid()
            self.check_validate_effect()
            self.check_validate_action()
            return self.check_validate_resource()
        except Exception as error:
            print(f"Error: {error}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Verify if a JSON file contains a valid IAM policy.")
    parser.add_argument("file_path", help="Path to the JSON file containing the IAM policy.")
    args = parser.parse_args()
    verifier = VeryfingIfValidJSON(args.file_path)
    print(verifier.main())
