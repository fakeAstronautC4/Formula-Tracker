from model import User, Formula, Material


def find_formula(param1):
    try: 
        formula = Formula.query.filter_by(formula_code = param1).first()
        return (formula)
    except: 
        formula = Formula.query.filter_by(formula_name = param1).first()
        return (formula)

def find_user(param1):
    user = User.query.filter_by(email = param1).first()
    return(user)    

def find_material(param1):
    try:    
        r_material = Material.query.filter_by(rm_code = param1).first()
        return(r_material)
    except:
        r_material = Material.query.filter_by(inci = param1).first()
        return(r_material)

