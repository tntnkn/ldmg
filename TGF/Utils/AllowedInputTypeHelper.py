class AllowedInputTypeHelper():
    @staticmethod
    def CheckIfInputIsAllowed(input_type, allowed_input_types):
        return input_type & allowed_input_types

    @staticmethod
    def SetAllowedInputTypes(*input_types):
        allowed = 0
        for t in input_types:
            allowed = AllowedInputTypeHelper.AddAllowedInput(t, allowed)
        return allowed

    @staticmethod
    def AddAllowedInput(input_type, allowed_input_types):
        allowed_input_types |= input_type 
        return allowed_input_types

    @staticmethod
    def DeleteAllowedInput(input_type, allowed_input_types):
        allowed_input_types &= ~input_type
        return allowed_input_types

