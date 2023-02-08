from typing     import TypedDict, Dict, List, Union

ID = str

UserInput = Dict[ID, Union[str, None]]

class UserContext(TypedDict):
    current_state_id    : ID 
    next_state_idx      : int
    state_history       : List[ID]

class Branch(TypedDict):
    req_user_input_ids  : List[ID] 
    resulting_state_id  : ID

StateBranches = List[Branch]

StatesBranchesStorage = Dict[ID, StateBranches]

class MainStorageContents(TypedDict):
    user_context        : UserContext
    user_input          : UserInput

MainStorage = Dict[ID, MainStorageContents]

class GeneralInfo(TypedDict):
    brahches            : StatesBranchesStorage
    start_id            : ID

