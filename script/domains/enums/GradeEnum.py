from enum import Enum, unique


@unique
class GradeEnum(Enum):
    FIRST_GRADE_UP = ["一年级上册", 11]
    FIRST_GRADE_DOWN = ["一年级下册", 12]
    SECOND_GRADE_UP = ["二年级上册", 21]
    SECOND_GRADE_DOWN = ["二年级下册", 22]
    THIRD_GRADE_UP = ["三年级上册", 31]
    THIRD_GRADE_DOWN = ["三年级下册", 32]
    FOUR_GRADE_UP = ["四年级上册", 41]
    FOUR_GRADE_DOWN = ["四年级下册", 42]
    FIVE_GRADE_UP = ["五年级上册", 51]
    FIVE_GRADE_DOWN = ["五年级下册", 52]
    SIX_GRADE_UP = ["六年级上册", 61]
    SIX_GRADE_DOWN = ["六年级下册", 62]
    SEVEN_GRADE_UP = ["七年级上册", 71]
    SEVEN_GRADE_DOWN = ["七年级下册", 72]
    EIGHT_GRADE_UP = ["八年级上册", 81]
    EIGHT_GRADE_DOWN = ["八年级下册", 82]
    NINE_GRADE_UP = ["九年级上册", 91]
    NINE_GRADE_DOWN = ["九年级下册", 92]
