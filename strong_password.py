def get_info(s):
    """
    Get the number of lowercase letters, uppercase letters, digits and groups of reapeating characters of string.
    :param s:
    :return: no_lowercase - no of lowercase letters
             no_uppercase - no of uppercase letters
             no_digit - no of digits
             repeats - array of no of repeating groups of characters
    """
    no_lowercase = 0  # no of lowercase letters existing in the string
    no_uppercase = 0  # no of uppercase letters existing in string
    no_digit = 0  # no of digits existing in string

    r_begin = 0  # beginning index of a repeating sequence
    r_end = 0  # end of a repeating sequence
    repeats = []    # array with the lengths of groups of characters

    for i in range(len(s)):
        # count the number of lowercase, uppercase and digits present in string
        if s[i].islower():
            no_lowercase += 1
        elif s[i].isupper():
            no_uppercase += 1
        elif s[i].isdigit():
            no_digit += 1

        # compute length of repeating sequence
        if i < len(s) - 1 and s[i] == s[i + 1]:
            r_end = i + 1
        else:
            repeats.append(r_end - r_begin + 1)
            r_begin = i + 1
            r_end = i + 1

    return no_lowercase, no_uppercase, no_digit, repeats


def check_password(s):
    """
    Determinate the minimum number of changes for a given password in order for it to be strong.
    A password is considered strong if:
        1. it has at least 6 characters and at most 20 characters
        2. it has at least one lowercase letter, one uppercase letter and one digit
        3. it doesn't contain 3 repeating characters in a row
    :param s: string
    :return: no_changes: integer
             no_changes = minimum number of changes required for the password to become strong
    """
    '''
    Assume that s is a string only containing lowercase letters, uppercase letters and digits.
    
    Cases:
        1. len(s) < 6: insertion
        2. len(s) > 20: deletion
        3. missing lowercase/uppercase/digit: insert/replace
        4. repeating characters: insert/delete/replace (replacing gives the minimum)
    '''

    no_changes = 0  # no of changes needed to transform given string into strong password
    no_lower, no_upper, no_digit, repeats = get_info(s)

    no_missing = 0  # no of missing required characters (0 <= no_missing <= 3)
    if no_lower == 0:
        no_missing += 1
    if no_upper == 0:
        no_missing += 1
    if no_digit == 0:
        no_missing += 1

    if len(s) < 6:
        # add up characters, either by adding up to 6 or by adding all missing characters
        no_changes = max(6 - len(s), no_changes)
    elif len(s) <= 20:
        # the length of the string is fine but we can have repeating characters or missing types
        no_changes = max(sum([x // 3 for x in repeats]), no_missing)
    else:
        # the length of the string is over 20 and we need to remove characters from the string
        no_over = len(s) - 20
        # remove repeats of the strings
        for i in range(len(repeats)):
            # case where one delete break a repetition of 3 characters
            # (ex: aaa -> delete: aa)
            if repeats[i] % 3 == 0 and no_over > 1:
                repeats[i] -= 1
                no_over -= 1

        for i in range(len(repeats)):
            # case where 2 deletes break a repetition of 3 characters
            # because the no of repeating characters is M3 + 1 (ex: aaaa -> delete1: aaa, delete2: aa)
            if repeats[i] % 3 == 1 and repeats[i] > 3 and no_over > 2:
                repeats[i] -= 2
                no_over -= 2

        for i in range(len(repeats)):
            # case where we delete characters, if we have any repetitions left
            # or if we have remaining characters
            if no_over > 0 and repeats[i] > 2:
                repeats[i] -= min(no_over, repeats[i] - 2)
                no_over -= min(no_over, repeats[i] - 2)

        # we add up any remaining missing types of characters or groups of repeating characters
        no_changes = max(sum([x // 3 for x in repeats]), no_missing) + len(s) - 20

    return no_changes


def test_check_password():
    assert check_password("") == 6
    assert check_password("abcdef") == 2
    assert check_password("aB5cD6") == 0
    assert check_password("aBCdefgh") == 1
    assert check_password("aaaaaa") == 2
    assert check_password("aaaBCD") == 1
    assert check_password("aaa") == 3
    assert check_password("abcDDDefff6") == 2
    assert check_password("1234567890abcgefdrstBBCFDREH") == 8
    assert check_password("111222333444ghfbretuoingGHYU") == 8


def main():
    test_check_password()


main()
