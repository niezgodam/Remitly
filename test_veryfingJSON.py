import unittest
from VeryfingIfValidJSON import VeryfingIfValidJSON

class TestVeryfingJSON(unittest.TestCase):

    def test_loading_correct_file(self):
        path = "Test/checkingIfValidJsonFormat.json"
        obj = VeryfingIfValidJSON(path)

        try:
            obj.loading_file()
        except Exception as e:
            self.fail(f"Failed to load valid JSON file: {e}")

    def test_loading_missing_file(self):
        path = "non_existent_file.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
        self.assertEqual(str(context.exception), "File loading error")

    def test_checking_wrong_JSON_format_1(self):
        path = "Test/wrongJsonFormat1.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
        self.assertEqual(str(context.exception), "JSON is not valid format")

    def test_checking_wrong_JSON_format_2(self):
        path = "Test/wrongJsonFormat2.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
        self.assertEqual(str(context.exception), "JSON is not valid format")

    def test_checking_wrong_JSON_format_3(self):
        path = "Test/wrongJsonFormat3.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
        self.assertEqual(str(context.exception), "JSON is not valid format")

    def test_correct_Json_Format(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)

        try:
            obj.loading_file()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
    
    def test_checking_if_policynameAndPolicydocument_in_file(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_checking_if_PolicyName_not_in_file(self):
        path = "Test/missingPolicyName.json"
        obj = VeryfingIfValidJSON(path)
        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
        self.assertEqual(str(context.exception), "PolicyName or PolicyDocument not found in JSON")

    def test_checking_if_PolicyDocument_not_in_file(self):
        path = "Test/missingPolicyDocument.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
        self.assertEqual(str(context.exception), "PolicyName or PolicyDocument not found in JSON")

    def test_checking_valid_PolicyName_format_length(self):
        path = "Test/wrongPolicyNameLength1.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
        self.assertEqual(str(context.exception), "PolicyName is not string or it requirements not met")

    def test_checking_valid_PolicyName_format_pattern(self):
        path = "Test/wrongPolicyNamePattern.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
        self.assertEqual(str(context.exception), "PolicyName is not string or it requirements not met")
    
    def test_checking_valid_PolicyName_format_type(self):
        path = "Test/wrongPolicyNameType.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
        self.assertEqual(str(context.exception), "PolicyName must be a string")

    
    def test_checking_if_version_in_file(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_version()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_checking_if_version_not_in_file(self):
        path = "Test/wrongVersionInFile.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_version()
        self.assertEqual(str(context.exception), 'Version not in Policy Document')

    def test_checking_if_statement_in_file(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_version()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
    
    def test_checking_if_statement_not_in_file(self):
        path = "Test/wrongStatementInFile.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_statement()
        self.assertEqual(str(context.exception), 'Statement not in Policy Document')

    def test_checking_if_sid_is_correct(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_sid()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_checking_if_sid_valid_pattern1(self):
        path = "Test/wrongSIDpattern1.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_sid()
        self.assertEqual(str(context.exception), 'Invalid SID: The Sid element supports ASCII uppercase letters (A-Z), lowercase letters (a-z), and numbers (0-9)')

    def test_checking_if_sid_valid_pattern2(self):
        path = "Test/wrongSIDpattern2.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_sid()
        self.assertEqual(str(context.exception), 'Invalid SID: The Sid element supports ASCII uppercase letters (A-Z), lowercase letters (a-z), and numbers (0-9)')
    
    def test_checking_if_effect_in_json_file(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)

        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_effect()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
    
    def test_checking_if_effect_not_in_json_file(self):
        path = "Test/effectNotInFile.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_statement()
            obj.check_validate_effect()
        self.assertEqual(str(context.exception), "Effect not in JSON")

    def test_checking_if_effect_valid_allow(self):
        path = "Test/correctEffectWithAllow.json"
        obj = VeryfingIfValidJSON(path)

        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_effect()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_checking_if_effect_not_valid_allow(self):
        path = "Test/wrongEffectProperties.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_statement()
            obj.check_validate_effect()
        self.assertEqual(str(context.exception), "Valid values for Effect are only: Allow and Deny")

    def test_checking_if_action_in_Json_file(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)

        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_action()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_checking_if_action_not_in_Json_file(self):
        path = "Test/missingAction.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_action()
        self.assertEqual(str(context.exception), "Action or NotAction must be included in Statement")

    def test_checking_if_resource_in_Json_file(self):
        path = "Test/correctJsonFormat.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_resource()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_checking_if_resource_not_in_Json_file(self):
        path = "Test/missingResource.json"
        obj = VeryfingIfValidJSON(path)

        with self.assertRaises(Exception) as context:
            obj.loading_file()
            obj.check_required_policy_properties()
            obj.check_validate_resource()
        self.assertEqual(str(context.exception), "Resource or NotResource must be included in Statement")

    def test_checking_resource_diffrent_input1(self):
        path = "Test/resourceInput1.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            result = obj.check_validate_resource()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
        self.assertEqual(False, result)

    def test_checking_resource_diffrent_input2(self):
        path = "Test/resourceInput2.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            result = obj.check_validate_resource()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
        self.assertEqual(True, result)

    def test_checking_resource_diffrent_input3(self):
        path = "Test/resourceInput3.json"
        obj = VeryfingIfValidJSON(path)
        try:
            obj.loading_file()
            obj.check_required_policy_properties()
            result = obj.check_validate_resource()
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")
        self.assertEqual(True, result)

if __name__ == '__main__':
    unittest.main()