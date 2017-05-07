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
            chars[i] = '9';
        else:
            # If any other digit is encountered, change that to 9, for example, 195->199, or with both rules: 150->199
            chars[i] = '9';
            break;
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

def num_to_cutoffs(start, end):
    start_res = []
    end_res = []
    while start < 1000:
        start_res.append(start)
        start = next_num(start)
        start_res.append(start)
        start = start + 1
    while end >= 0:
        end_res.append(end)
        end = prev_num(end)
        end_res.append(end)
        end = end - 1
    print(start_res, sorted(end_res))
    return start_res, sorted(end_res)

def get_merged_cutoffs(start, end):
    start_res, end_res = num_to_cutoffs(start, end)
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
    print(reg)
    return reg



def run(start, end):
    startIntPart = str(start).split('.')[0]
    endIntPart = str(end).split('.')[0]
    res_list = get_merged_cutoffs(int(startIntPart), int(endIntPart))
    print(res_list)
    reg = merged_cutoffs_to_reg(res_list)

    

run(0.00, 381.00)