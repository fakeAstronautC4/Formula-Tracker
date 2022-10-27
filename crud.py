from model import User, Formula, Material


def find_formula(param1):
    str(param1)
    results = []
    formula = Formula.query.filter_by(formula_code = param1).first()
    if formula == None:
        formula = Formula.query.filter_by(name = param1).first()        
        if formula == None:
            formula = Formula.query.filter_by(customer = param1).all()
            return(formula)
        else:
            results.append(formula)  
            return(results)  
    else:
        results.append(formula)
        return (results)    

def find_user(param1):
    user = User.query.filter_by(email = param1).first()
    return(user)    

def find_material(param1):  
    r_material = Material.query.filter_by(rm_code = param1).first()
    if r_material == None:
        r_material = Material.query.filter_by(inci = param1).first()
        return(r_material)
    else:
        return(None)

