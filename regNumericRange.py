import re


numericRangeList = ['0.00~1.00', '0.00~5.00', '0.00~10.00', '0.000~10.000', '0.00~15.00', '0.0~20.0', '0.00~20.00', '0.00~23.00', '0.00~25.00', '0.0~30.0', '0.00~35.00', '0.00~40.00', '0.00~45.00', '0.0~50.0', '0.00~50.00', '0.00~70.00', '0.00~90.00', '0~100', '0.0~100.0', '0.00~100.00', '0.000~100.000', '0.00~150.00', '0.00~200.00', '0~250', '0.0~250.0', '0.00~250.00', '0.0~300.0', '0.00~300.00', '0.00~500.00', '0.00~540.00', '0.00~600.00', '0.00~650.00', '0.00~900.00', '0.00~1000.00', '0.00~1200.00', '0.0~1500.0', '0.00~1500.00', '0.00~2000.00', '0.00~2500.00', '0.0~2700.0', '0.00~3000.00', '0.00~3300.00', '0.00~4500.00', '0.00~5000.00', '0.00~6500.00', '0.00~10000.00', '0.00~20000.00', '0.00~30000.00', '0.00~200000.00']


def next_num(num):
    # Convert to String for easier operations
    chars = list(str(num))
    # Go through all digits backwards
    for j in range(len(chars)):
        i = len(chars) - j - 1
        if i < 0:
            break
        # Skip the 0 changing it to 9. For example, for 190->199
        if chars[i]=='0':
            chars[i] = '9'
        else:
            # If any other digit is encountered, change that to 9, for example, 195->199, or with both rules: 150->199
            chars[i] = '9'
            break
    chars = ''.join(chars)
    return int(chars)

# Same thing, but reversed. 387 -> 380, 379 -> 300, etc
def prev_num(num):
    chars = list(str(num))
    for j in range(len(chars)):
        i = len(chars) - j - 1
        if chars[i] == '9':
            chars[i] = '0'
        else:
            chars[i] = '0'
            break
    chars = ''.join(chars)
    return int(chars)

def num_range_to_cutoffs(start, end):
    start_res = []
    end_res = []
    while start < end:
        start_res.append(start)
        start = next_num(start)
        start_res.append(start)
        start = start + 1
    while end >= 0:
        end_res.append(end)
        end = prev_num(end)
        end_res.append(end)
        end = end - 1
    #print(start_res, sorted(end_res))
    return start_res, sorted(end_res)

def get_merged_cutoffs(start, end):
    start_res, end_res = num_range_to_cutoffs(start, end)
    i = 0
    j = 0
    res_list = []
    while True:
        s1, s2 = start_res[i], start_res[i+1]
        e1, e2 = end_res[j], end_res[j+1]
        if s1 >= e1 and s2 >= e2:
            res_list = start_res[:i+1]
            res_list.extend(end_res[j+1:])
            break
        elif s1 >= e1 and s2 < e2:
            i = i + 2
        else:
            j = j + 2
        if i >= len(start_res)-1 or j >= len(end_res)-1:
            break
    return res_list



def merged_cutoffs_to_reg(res_list):
    reg = ''
    i = 0
    while True:
        start = res_list[i]
        end = res_list[i+1]
        start_str = str(start)
        end_str = str(end)
        str_len = len(start_str)
        reg0 = ''
        for idx in range(str_len):
            if start_str[idx] == end_str[idx]:
                reg0 = reg0 + start_str[idx]
            else:
                reg0 = reg0 + '[{}-{}]'.format(start_str[idx], end_str[idx])
        if reg == '':
            reg = reg0
        else:
            reg = reg + '|' + reg0
        i = i + 2
        if i >= len(res_list) - 1:
            break
    #print(reg)
    return reg


def num_range_to_reg(startIntPart, endIntPart, to_fixed):
    
    res_list = get_merged_cutoffs(startIntPart, endIntPart)
    #print(res_list)
    reg = merged_cutoffs_to_reg(res_list)
    #print(reg)
    _reg = []
    if res_list[-1]%10 == 0:
        _reg = merged_cutoffs_to_reg(res_list[0:-2])
    else:
        _res_list = res_list.copy()
        _res_list[-1] = _res_list[-1] - 1
        _reg = merged_cutoffs_to_reg(_res_list)
    if to_fixed == 0:
        _reg = '^((%s)|%d)$'%(_reg, res_list[-1])
    else:
        _reg = '^((%s)(.\d{1,%d})?|%d(.0{1,%d})?)$'%(_reg, to_fixed, res_list[-1], to_fixed)
    # print(_reg)

    return _reg

def run_test():
    right_case_num = [0, 0]
    error_case_num = [0, 0]
    for numeric_range in numericRangeList:
        start = numeric_range.split('~')[0]
        end = numeric_range.split('~')[1]
        if start > end:
            print('input error')
        startIntPart = start.split('.')[0]
        endIntPart = end.split('.')[0]
        to_fixed = 0
        if '.' in start:
            to_fixed = len(start.split('.')[1])
        _pow = pow(10, to_fixed)
        reg = num_range_to_reg(int(startIntPart), int(endIntPart), to_fixed)
        i = 0
        j = float(end) *_pow +1
        # <Right Case>
        while True:
            valStr = None
            if to_fixed == 0:
                valStr = int(i/_pow)
            else:
                valStr = round((i/_pow), to_fixed)
            res = re.match(reg, str(valStr))
            right_case_num[0] = right_case_num[0] +1
            if res == None:
                print(('<Right Case>reg error: numeric_range = {}, reg = {}, valStr = {}'.format(numeric_range, reg, valStr)))
                right_case_num[1] = right_case_num[1] +1
            i = i + 3
            if i > float(end) * _pow:
                break
        # <Error Case>
        while True:
            valStr = round((j/_pow), to_fixed)
            res = re.match(reg, str(valStr))
            error_case_num[0] = error_case_num[0] + 1
            if res != None:
                print(('<Error Case>reg error: numeric_range = {}, reg = {}, valStr = {}'.format(numeric_range, reg, valStr)))
                error_case_num[1] = error_case_num[1] + 1
            j = j + 3
            if j > float(end) * _pow + 1000:
                break
    print('total right cases:{}, success: {}, faile: {}'.format(right_case_num[0], right_case_num[0]- right_case_num[1], right_case_num[1]))
    print('total error cases:{}, success: {}, faile: {}'.format(error_case_num[0], error_case_num[0]- error_case_num[1], error_case_num[1]))

if __name__ == '__main__':

    run_test()