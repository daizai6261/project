from enum import Enum, unique


@unique
class GradeEnum(Enum):
    FIRST_GRADE_UP = 11  # 一年级上册
    FIRST_GRADE_DOWN = 12  # 一年级下册
    SECOND_GRADE_UP = 21  # 二年级上册
    SECOND_GRADE_DOWN = 22  # 二年级下册
    THIRD_GRADE_UP = 31  # 三年级上册
    THIRD_GRADE_DOWN = 32  # 三年级下册
    FOUR_GRADE_UP = 41  # 四年级上册
    FOUR_GRADE_DOWN = 42  # 四年级下册
    FIVE_GRADE_UP = 51  # 五年级上册
    FIVE_GRADE_DOWN = 52  # 五年级下册
    SIX_GRADE_UP = 61  # 六年级上册
    SIX_GRADE_DOWN = 62  # 六年级下册
    SEVEN_GRADE_UP = 71  # 七年级上册
    SEVEN_GRADE_DOWN = 72  # 七年级下册
    EIGHT_GRADE_UP = 81  # 八年级上册
    EIGHT_GRADE_DOWN = 82  # 八年级下册
    NINE_GRADE_UP = 91  # 九年级上册
    NINE_GRADE_DOWN = 92  # 九年级下册
