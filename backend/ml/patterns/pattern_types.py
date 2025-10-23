from enum import Enum


class PatternCategory(Enum):
    """Pattern categories"""
    REVERSAL = "reversal"
    CONTINUATION = "continuation"
    NEUTRAL = "neutral"


class PatternType(Enum):
    """All supported trading patterns"""

    DOUBLE_BOTTOM = ("double_bottom", PatternCategory.REVERSAL, "Bullish")
    DOUBLE_TOP = ("double_top", PatternCategory.REVERSAL, "Bearish")
    INVERTED_HEAD_SHOULDERS = ("inverted_head_shoulders", PatternCategory.REVERSAL, "Bullish")
    HEAD_SHOULDERS = ("head_shoulders", PatternCategory.REVERSAL, "Bearish")
    FALLING_WEDGE = ("falling_wedge", PatternCategory.REVERSAL, "Bullish")
    BEARISH_DIAMOND = ("bearish_diamond", PatternCategory.REVERSAL, "Bearish")
    BULLISH_DIAMOND = ("bullish_diamond", PatternCategory.REVERSAL, "Bullish")
    ROUNDING_TRIANGLE = ("rounding_triangle", PatternCategory.REVERSAL, "Variable")

    BULL_FLAG = ("bull_flag", PatternCategory.CONTINUATION, "Bullish")
    BEAR_FLAG = ("bear_flag", PatternCategory.CONTINUATION, "Bearish")
    BULLISH_PENNANT = ("bullish_pennant", PatternCategory.CONTINUATION, "Bullish")
    BEARISH_PENNANT = ("bearish_pennant", PatternCategory.CONTINUATION, "Bearish")
    BULLISH_RECTANGLE = ("bullish_rectangle", PatternCategory.CONTINUATION, "Bullish")
    RISING_WEDGE = ("rising_wedge", PatternCategory.CONTINUATION, "Bearish")
    ASCENDING_TRIANGLE = ("ascending_triangle", PatternCategory.CONTINUATION, "Bullish")
    ROUNDING_TOP = ("rounding_top", PatternCategory.CONTINUATION, "Bearish")

    TEA_CUP = ("tea_cup", PatternCategory.REVERSAL, "Bullish")
    INVERSE_TEA_CUP = ("inverse_tea_cup", PatternCategory.REVERSAL, "Bearish")

    def __init__(self, pattern_id, category, bias):
        self.pattern_id = pattern_id
        self.category = category
        self.bias = bias

    @property
    def display_name(self):
        """Get display name for the pattern"""
        return self.name.replace('_', ' ').title()

    @property
    def is_bullish(self):
        """Check if pattern is bullish"""
        return self.bias == "Bullish"

    @property
    def is_bearish(self):
        """Check if pattern is bearish"""
        return self.bias == "Bearish"

    @property
    def is_reversal(self):
        """Check if pattern is a reversal pattern"""
        return self.category == PatternCategory.REVERSAL

    @property
    def is_continuation(self):
        """Check if pattern is a continuation pattern"""
        return self.category == PatternCategory.CONTINUATION
