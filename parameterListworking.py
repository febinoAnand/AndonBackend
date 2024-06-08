data_list = [
    {
        'operator': '>=',
        'fixed_value': 10,
        'logical_operator': 'and'
    },
    {
        'operator': '<',
        'fixed_value': 20,
        'logical_operator': 'or'
    },
    {
        'operator': '==',
        'fixed_value': 5,
        'logical_operator': 'and'
    },
    {
        'operator': '!=',
        'fixed_value': 0,
        'logical_operator': 'and'
    },
    {
        'operator': '<=',
        'fixed_value': 8,
        'logical_operator': 'and'
    },
    {
        'operator': 'exists',
        'fixed_value': 2,
        'logical_operator': 'or'
    }
]
def check_conditions(conditions, input_number):
    import operator

    # Define a mapping of operators
    ops = {
        '>=': operator.ge,
        '<': operator.lt,
        '==': operator.eq,
        '!=': operator.ne,
        '<=': operator.le,
        'exists': lambda x, y: x == y  # Assuming 'exists' means equals for simplicity
    }

    # Initialize the result
    final_result = None

    for i, cond in enumerate(conditions):
        op = ops[cond['operator']]
        value = cond['fixed_value']

        # Evaluate the current condition
        current_result = op(input_number, value)

        if i == 0:
            # For the first condition, initialize the final_result
            final_result = current_result
        else:
            # For subsequent conditions, compare with the previous result
            logical_op = cond['logical_operator']
            if logical_op == 'and':
                final_result = final_result and current_result
            elif logical_op == 'or':
                final_result = final_result or current_result

        # If at any point final_result becomes False, continue to next dictionary
        if not final_result:
            continue

    return final_result


input_number = 7
result = check_conditions(data_list, input_number)
print(result)
