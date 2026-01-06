# check the input from user valid or not
def check_match_goals(home,away,result): 
        return (
        (home > away and result == "H") or
        (home < away and result == "A") or
        (home == away and result == "D")
    )

# find # of input cols from users that is null
def find_missing_fields(data:dict): 
        return [key for key, value in data.items() if value is None or (isinstance(value,str) and value.strip == "")]