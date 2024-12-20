import decimal
def cont_zero(num):
    if num == 0:
        return 0  
    str_num = f"{num:.16f}".rstrip('0')
    decimal_part = str_num.split(".")[1] if '.' in str_num else ''
    zeros = 0
    for char in decimal_part:
        if char == '0':
            zeros += 1
        else:
            break
    return zeros + 1

def create_num_witg_zero(num):
    zeros = cont_zero(num)
    return 10 ** zeros



def truncate_to_first_significant_digit(num):
    d_num = decimal.Decimal(str(num))
    num_str = str(d_num)
    
    if '.' in num_str:
        decimal_part = num_str.split('.')[1]
        first_significant_digit_index = next((i for i, char in enumerate(decimal_part) if char != '0'), len(decimal_part))
        truncated_str = "0." + decimal_part[:first_significant_digit_index+2]
        return truncated_str
    else:
        return num