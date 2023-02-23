from typing     import TypedDict, Dict, List, Union
from ..Types    import BranchTypes

ID = str

UserInput = Dict[ID, Union[str, None]]

class UserContext(TypedDict):
    current_state_idx   : int 
    state_history       : List[ID]
    rejected_states     : List[ID] 

class Branch(TypedDict):
    type                : BranchTypes
    req_user_input_ids  : List[ID] 
    resulting_state_id  : ID

StateBranches = List[Branch]

StatesBranchesStorage = Dict[ID, StateBranches]

class MainStorageContents(TypedDict):
    user_context        : UserContext
    user_input          : UserInput

MainStorage = Dict[ID, MainStorageContents]

PossibleInpIds = Dict[ID, List[ID]]

class GeneralInfo(TypedDict):
    branches            : StatesBranchesStorage
    start_id            : ID
    end_ids             : ID
    always_open_ids     : ID
    possible_inp_ids    : PossibleInpIds

