import re


# Skriv in använda
def get_pickable(used: set) -> set:

    characters = set("abcdefghijklmnopqrstuvwxyz")
    pickable = characters.difference(used)
    return pickable


def get_unique(my_dict: dict) -> set:
    """Input is a dictionary with keys 1-5 to strings. This returns all chars used in string values"""
    string_chars = ""
    for val in my_dict.values():
        string_chars += val
    return set(string_chars)


def get_possibly_there(not_there: dict, included_chars: set) -> dict:
    """Returns inverse of not_there, a set of where certain char may be"""
    POSSIBLY_THERE = {}
    for c in included_chars:
        for i in range(1, 6):  # Bokstav i ordet
            POSSIBLY_THERE.setdefault(i, [])
            if c not in not_there[i]:
                POSSIBLY_THERE[i].append(c)
    return POSSIBLY_THERE


def only_possible_here(
    char: str,
    char_num: int,
    POSSIBLY_THERE: dict[int, list[str]],
    set_chars: dict[int, str | None],
):
    """Checks if char can only be placed on char_num"""

    # Checks if it is already somewhere else
    for i in range(1, char_num):
        if set_chars[i] == char:
            return False

    # Checks if it has somewhere else to go
    for i in range(char_num + 1, 6):
        if char in POSSIBLY_THERE[i]:
            return False
    return True


def iter_set_there_BFS(
    char_num: int,  # Eg djup
    POSSIBLY_THERE: dict[int, list[str]],
    PICKABLE: set[str],
    set_chars: dict[int, str | None],
    word_list: list,
    SURE_CHARS: set[str],
):
    if char_num == 6:  # Vi har satt alla värden
        # Lägger ihop alla chars i set_chars och lägger till i word_list
        word_list.append("".join(v for v in set_chars.values() if v is not None))
        return
        # {1: 'm', 2: 'e', 3: None, 4: None, 5: None}
    # Hantera risk att bokstav måste vara här!
    # Lista med bokstäver som måste vara här
    only_possible_here_list = []
    for possible_char in POSSIBLY_THERE[char_num]:
        if only_possible_here(possible_char, char_num, POSSIBLY_THERE, set_chars):
            only_possible_here_list.append(possible_char)
    if len(only_possible_here_list) == 1:
        new_set_chars = set_chars.copy()
        new_set_chars[char_num] = only_possible_here_list[0]  # Måste vara här
        iter_set_there_BFS(
            char_num + 1, POSSIBLY_THERE, PICKABLE, new_set_chars, word_list, SURE_CHARS
        )
        return
    elif len(only_possible_here_list) > 1:  # Omöjligt då någon bokstav säkert förloras
        return

    for char in PICKABLE:
        # Skippa om vi har en bokstav som definitivt inte är valbar här.
        if char in SURE_CHARS and char not in POSSIBLY_THERE[char_num]:
            continue
        new_set_chars = set_chars.copy()
        new_set_chars[char_num] = char  # Måste vara här
        iter_set_there_BFS(
            char_num + 1, POSSIBLY_THERE, PICKABLE, new_set_chars, word_list, SURE_CHARS
        )


def Solve(pickable: set, POSSIBLY_THERE: dict, SURE_CHARS: set):
    possible_words = []
    iter_set_there_BFS(
        1,
        POSSIBLY_THERE,
        pickable,
        {1: None, 2: None, 3: None, 4: None, 5: None},
        possible_words,
        SURE_CHARS,
    )
    return possible_words


def format_regex(lista, mode="uncommon"):
    # Rensa och sortera
    mid_seperated = "|".join(sorted(set(lista)))

    if mode == "start":
        return f"r'^({mid_seperated})'"
    elif mode == "end":
        return f"r'({mid_seperated})$'"
    else:
        return f"r'({mid_seperated})'"


def is_unlikely(w: str, UNCOMMON_NEIGHBOURS, UNCOMMON_START, UNCOMMON_END) -> bool:

    if re.search(UNCOMMON_START, w):
        return True
    # 2. Ogiltigt slut
    if re.search(UNCOMMON_END, w):
        return True
    # Q-regeln (q ej följt av u)
    if "q" in w and "qu" not in w:
        return True

    # Vokal-kluster (3+ i rad)
    if re.search(r"[aeiouy]{3,}", w):
        return True

    # Konsonant-kluster (3+ i rad, förenklat)
    if re.search(r"[^aeiouy]{3,}", w):
        return True

    # 4. osannolika i rad
    if re.search(UNCOMMON_NEIGHBOURS, w):
        return True
    return False


def rank_and_remove_uncommon(word_list):
    # Remove uncommon pairs
    with open("uncommon_neighbours.txt", "r", encoding="utf-8") as f:
        UNCOMMON_NEIGHBOURS = [line.strip() for line in f]
    UNCOMMON_NEIGHBOURS = format_regex(UNCOMMON_NEIGHBOURS)

    UNCOMMON_START = r"^(jb|jc|jd|jf|jg|jh|jj|jk|jl|jm|jn|jp|jq|jr|js|jt|jv|jw|jx|jy|jz|kz|qb|qc|qd|qe|qf|qg|qh|qj|qk|ql|qm|qn|qo|qp|qr|qs|qt|qv|qw|qx|qy|qz|vb|vc|vd|vf|vg|vh|vj|vk|vl|vm|vn|vp|vq|vr|vs|vt|vw|vx|vy|vz|xb|xc|xd|xf|xg|xh|xj|xk|xl|xm|xn|xp|xq|xr|xs|xt|xv|xw|xy|xz|zb|zc|zd|zeo|zf|zg|zh|zj|zk|zl|zm|zn|zp|zq|zr|zs|zt|zv|zw|zx|zy)"
    UNCOMMON_END = r"(aa|ii|uu|uo|eo|bk|cb|cx|dx|fv|hg|iy|jh|vj|vk|vl|vm|vn|vp|vq|vr|vs|vt|vw|vx|vy|vz|wj|wm|wn|wp|wq|wx|wy|wz|xj|zk|zl|zm|zn|zp|zq|zr|zs|zt|zv|zw|zx|q|j|v|b|c)$"
    likely_words = []
    for word in word_list:
        if not is_unlikely(word, UNCOMMON_NEIGHBOURS, UNCOMMON_START, UNCOMMON_END):
            likely_words.append(word)
    return likely_words


def solve_wordle(used_str: str, yellow_dict: dict):
    # 1. Formatera rådata från GUI
    used = set(used_str.lower())
    pickable = get_pickable(used)
    included_chars = get_unique(yellow_dict)
    pos_there = get_possibly_there(yellow_dict, included_chars)

    # 2. Anropa din befintliga Solve-funktion
    word_list = Solve(pickable, pos_there, included_chars)

    likely_words = rank_and_remove_uncommon(word_list)

    return likely_words


if __name__ == "__main__":
    # INPUT
    used = set("spirathwdml")
    pickable = get_pickable(used)
    not_there = {1: "no", 2: "oe", 3: "on", 4: "e", 5: "oe"}
    included_chars = get_unique(not_there)
    POSSIBLY_THERE = get_possibly_there(not_there, included_chars)

    word_list = Solve(pickable, POSSIBLY_THERE, included_chars)
    likely_words = rank_and_remove_uncommon(word_list)
    cols = 8

    rows = [likely_words[i : i + cols] for i in range(0, len(likely_words), cols)]

    # 2. Printa med formatering
    for row in rows:
        print("".join(f"{item:<12}" for item in row))
