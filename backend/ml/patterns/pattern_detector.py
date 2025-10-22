import numpy as np
import pandas as pd
from scipy.signal import argrelextrema, find_peaks
from scipy.stats import linregress
import logging
from typing import List, Dict, Optional, Tuple
from .pattern_types import PatternType, PatternCategory

logger = logging.getLogger(__name__)


class PatternDetector:
    """
    Comprehensive pattern recognition for trading charts
    Detects 18+ chart patterns including reversals and continuations
    """

    def __init__(self, lookback_window=100, min_pattern_bars=10):
        self.lookback_window = lookback_window
        self.min_pattern_bars = min_pattern_bars

        self.pattern_detectors = {
            PatternType.DOUBLE_BOTTOM: self._detect_double_bottom,
            PatternType.DOUBLE_TOP: self._detect_double_top,
            PatternType.HEAD_SHOULDERS: self._detect_head_shoulders,
            PatternType.INVERTED_HEAD_SHOULDERS: self._detect_inverted_head_shoulders,
            PatternType.BULL_FLAG: self._detect_bull_flag,
            PatternType.BEAR_FLAG: self._detect_bear_flag,
            PatternType.BULLISH_PENNANT: self._detect_pennant,
            PatternType.BEARISH_PENNANT: self._detect_pennant,
            PatternType.ASCENDING_TRIANGLE: self._detect_ascending_triangle,
            PatternType.RISING_WEDGE: self._detect_wedge,
            PatternType.FALLING_WEDGE: self._detect_wedge,
            PatternType.BULLISH_RECTANGLE: self._detect_rectangle,
            PatternType.ROUNDING_TOP: self._detect_rounding_top,
            PatternType.ROUNDING_TRIANGLE: self._detect_rounding_triangle,
            PatternType.BULLISH_DIAMOND: self._detect_diamond,
            PatternType.BEARISH_DIAMOND: self._detect_diamond,
            PatternType.TEA_CUP: self._detect_tea_cup,
            PatternType.INVERSE_TEA_CUP: self._detect_inverse_tea_cup,
        }

        logger.info('PatternDetector initialized with 18+ pattern algorithms')

    def detect_all_patterns(self, price_data):
        """
        Detect all patterns in price data

        Args:
            price_data: DataFrame or dict with OHLC data

        Returns:
            List of detected patterns with confidence scores
        """
        if isinstance(price_data, dict):
            df = pd.DataFrame(price_data)
        else:
            df = price_data.copy()

        if len(df) < self.min_pattern_bars:
            logger.warning(f'Insufficient data: need at least {self.min_pattern_bars} bars')
            return []

        recent_data = df.tail(self.lookback_window)

        detected_patterns = []

        for pattern_type in PatternType:
            detector_func = self.pattern_detectors.get(pattern_type)
            if detector_func:
                try:
                    result = detector_func(recent_data, pattern_type)
                    if result:
                        detected_patterns.append(result)
                except Exception as e:
                    logger.error(f'Error detecting {pattern_type.name}: {e}')

        detected_patterns.sort(key=lambda x: x['confidence'], reverse=True)

        return detected_patterns

    def _find_peaks_and_troughs(self, prices, order=5):
        """Find local maxima (peaks) and minima (troughs)"""
        peaks_idx = argrelextrema(prices, np.greater, order=order)[0]
        troughs_idx = argrelextrema(prices, np.less, order=order)[0]

        return peaks_idx, troughs_idx

    def _detect_double_bottom(self, df, pattern_type):
        """Detect double bottom pattern (bullish reversal)"""
        closes = df['close'].values
        lows = df['low'].values

        _, troughs_idx = self._find_peaks_and_troughs(closes, order=5)

        if len(troughs_idx) < 2:
            return None

        for i in range(len(troughs_idx) - 1):
            trough1_idx = troughs_idx[i]
            trough2_idx = troughs_idx[i + 1]

            if trough2_idx - trough1_idx < 10 or trough2_idx - trough1_idx > 60:
                continue

            trough1_price = lows[trough1_idx]
            trough2_price = lows[trough2_idx]

            price_diff = abs(trough1_price - trough2_price) / trough1_price

            if price_diff < 0.03:
                peak_between = closes[trough1_idx:trough2_idx].max()
                peak_height = (peak_between - min(trough1_price, trough2_price)) / min(trough1_price, trough2_price)

                if peak_height > 0.02:
                    confidence = self._calculate_pattern_confidence(
                        price_diff,
                        peak_height,
                        trough2_idx - trough1_idx
                    )

                    return {
                        'pattern': pattern_type,
                        'type': pattern_type.display_name,
                        'category': pattern_type.category.value,
                        'bias': pattern_type.bias,
                        'confidence': confidence,
                        'start_idx': trough1_idx,
                        'end_idx': trough2_idx,
                        'target_price': closes[-1] * (1 + peak_height),
                        'probability': min(confidence / 100 * 1.2, 0.85)
                    }

        return None

    def _detect_double_top(self, df, pattern_type):
        """Detect double top pattern (bearish reversal)"""
        closes = df['close'].values
        highs = df['high'].values

        peaks_idx, _ = self._find_peaks_and_troughs(closes, order=5)

        if len(peaks_idx) < 2:
            return None

        for i in range(len(peaks_idx) - 1):
            peak1_idx = peaks_idx[i]
            peak2_idx = peaks_idx[i + 1]

            if peak2_idx - peak1_idx < 10 or peak2_idx - peak1_idx > 60:
                continue

            peak1_price = highs[peak1_idx]
            peak2_price = highs[peak2_idx]

            price_diff = abs(peak1_price - peak2_price) / peak1_price

            if price_diff < 0.03:
                trough_between = closes[peak1_idx:peak2_idx].min()
                trough_depth = (max(peak1_price, peak2_price) - trough_between) / max(peak1_price, peak2_price)

                if trough_depth > 0.02:
                    confidence = self._calculate_pattern_confidence(
                        price_diff,
                        trough_depth,
                        peak2_idx - peak1_idx
                    )

                    return {
                        'pattern': pattern_type,
                        'type': pattern_type.display_name,
                        'category': pattern_type.category.value,
                        'bias': pattern_type.bias,
                        'confidence': confidence,
                        'start_idx': peak1_idx,
                        'end_idx': peak2_idx,
                        'target_price': closes[-1] * (1 - trough_depth),
                        'probability': min(confidence / 100 * 1.2, 0.85)
                    }

        return None

    def _detect_head_shoulders(self, df, pattern_type):
        """Detect head and shoulders pattern (bearish reversal)"""
        closes = df['close'].values
        highs = df['high'].values

        peaks_idx, _ = self._find_peaks_and_troughs(closes, order=5)

        if len(peaks_idx) < 3:
            return None

        for i in range(len(peaks_idx) - 2):
            left_shoulder_idx = peaks_idx[i]
            head_idx = peaks_idx[i + 1]
            right_shoulder_idx = peaks_idx[i + 2]

            left_shoulder = highs[left_shoulder_idx]
            head = highs[head_idx]
            right_shoulder = highs[right_shoulder_idx]

            if head > left_shoulder and head > right_shoulder:
                shoulder_symmetry = abs(left_shoulder - right_shoulder) / head

                if shoulder_symmetry < 0.05:
                    head_prominence = (head - max(left_shoulder, right_shoulder)) / head

                    if head_prominence > 0.03:
                        confidence = self._calculate_pattern_confidence(
                            shoulder_symmetry,
                            head_prominence,
                            right_shoulder_idx - left_shoulder_idx
                        )

                        neckline = (left_shoulder + right_shoulder) / 2
                        target_decline = head - neckline

                        return {
                            'pattern': pattern_type,
                            'type': pattern_type.display_name,
                            'category': pattern_type.category.value,
                            'bias': pattern_type.bias,
                            'confidence': confidence,
                            'start_idx': left_shoulder_idx,
                            'end_idx': right_shoulder_idx,
                            'neckline': neckline,
                            'target_price': neckline - target_decline,
                            'probability': min(confidence / 100 * 1.3, 0.90)
                        }

        return None

    def _detect_inverted_head_shoulders(self, df, pattern_type):
        """Detect inverted head and shoulders (bullish reversal)"""
        closes = df['close'].values
        lows = df['low'].values

        _, troughs_idx = self._find_peaks_and_troughs(closes, order=5)

        if len(troughs_idx) < 3:
            return None

        for i in range(len(troughs_idx) - 2):
            left_shoulder_idx = troughs_idx[i]
            head_idx = troughs_idx[i + 1]
            right_shoulder_idx = troughs_idx[i + 2]

            left_shoulder = lows[left_shoulder_idx]
            head = lows[head_idx]
            right_shoulder = lows[right_shoulder_idx]

            if head < left_shoulder and head < right_shoulder:
                shoulder_symmetry = abs(left_shoulder - right_shoulder) / head

                if shoulder_symmetry < 0.05:
                    head_depth = (min(left_shoulder, right_shoulder) - head) / head

                    if head_depth > 0.03:
                        confidence = self._calculate_pattern_confidence(
                            shoulder_symmetry,
                            head_depth,
                            right_shoulder_idx - left_shoulder_idx
                        )

                        neckline = (left_shoulder + right_shoulder) / 2
                        target_rise = neckline - head

                        return {
                            'pattern': pattern_type,
                            'type': pattern_type.display_name,
                            'category': pattern_type.category.value,
                            'bias': pattern_type.bias,
                            'confidence': confidence,
                            'start_idx': left_shoulder_idx,
                            'end_idx': right_shoulder_idx,
                            'neckline': neckline,
                            'target_price': neckline + target_rise,
                            'probability': min(confidence / 100 * 1.3, 0.90)
                        }

        return None

    def _detect_bull_flag(self, df, pattern_type):
        """Detect bull flag pattern (bullish continuation)"""
        closes = df['close'].values

        if len(closes) < 20:
            return None

        pole_start = closes[:len(closes)//2]
        flag_part = closes[len(closes)//2:]

        pole_slope, _, pole_r_value, _, _ = linregress(range(len(pole_start)), pole_start)

        if pole_slope <= 0 or pole_r_value**2 < 0.7:
            return None

        flag_slope, _, flag_r_value, _, _ = linregress(range(len(flag_part)), flag_part)

        if flag_slope >= 0 or abs(flag_slope) > abs(pole_slope) * 0.5:
            return None

        pole_strength = abs(pole_slope / pole_start[0])
        flag_consolidation = abs(flag_slope / flag_part[0])

        if pole_strength > 0.01 and flag_consolidation < pole_strength * 0.3:
            confidence = min(70 + pole_r_value**2 * 25, 95)

            return {
                'pattern': pattern_type,
                'type': pattern_type.display_name,
                'category': pattern_type.category.value,
                'bias': pattern_type.bias,
                'confidence': confidence,
                'start_idx': 0,
                'end_idx': len(closes) - 1,
                'target_price': closes[-1] * (1 + pole_strength),
                'probability': min(confidence / 100 * 1.1, 0.80)
            }

        return None

    def _detect_bear_flag(self, df, pattern_type):
        """Detect bear flag pattern (bearish continuation)"""
        closes = df['close'].values

        if len(closes) < 20:
            return None

        pole_start = closes[:len(closes)//2]
        flag_part = closes[len(closes)//2:]

        pole_slope, _, pole_r_value, _, _ = linregress(range(len(pole_start)), pole_start)

        if pole_slope >= 0 or pole_r_value**2 < 0.7:
            return None

        flag_slope, _, flag_r_value, _, _ = linregress(range(len(flag_part)), flag_part)

        if flag_slope <= 0 or abs(flag_slope) > abs(pole_slope) * 0.5:
            return None

        pole_strength = abs(pole_slope / pole_start[0])
        flag_consolidation = abs(flag_slope / flag_part[0])

        if pole_strength > 0.01 and flag_consolidation < pole_strength * 0.3:
            confidence = min(70 + pole_r_value**2 * 25, 95)

            return {
                'pattern': pattern_type,
                'type': pattern_type.display_name,
                'category': pattern_type.category.value,
                'bias': pattern_type.bias,
                'confidence': confidence,
                'start_idx': 0,
                'end_idx': len(closes) - 1,
                'target_price': closes[-1] * (1 - pole_strength),
                'probability': min(confidence / 100 * 1.1, 0.80)
            }

        return None

    def _detect_pennant(self, df, pattern_type):
        """Detect pennant patterns (both bullish and bearish)"""
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values

        if len(closes) < 15:
            return None

        recent = closes[-15:]
        highs_recent = highs[-15:]
        lows_recent = lows[-15:]

        upper_slope, _, upper_r, _, _ = linregress(range(len(highs_recent)), highs_recent)
        lower_slope, _, lower_r, _, _ = linregress(range(len(lows_recent)), lows_recent)

        slopes_converging = (upper_slope < 0 and lower_slope > 0)

        if slopes_converging and upper_r**2 > 0.6 and lower_r**2 > 0.6:
            avg_range = np.mean(highs_recent - lows_recent)
            current_range = highs_recent[-1] - lows_recent[-1]

            if current_range < avg_range * 0.5:
                prior_trend = (closes[-15] - closes[0]) / closes[0]

                if abs(prior_trend) > 0.02:
                    is_bullish = prior_trend > 0
                    bias = "Bullish" if is_bullish else "Bearish"

                    confidence = min(65 + (upper_r**2 + lower_r**2) * 15, 90)

                    return {
                        'pattern': pattern_type,
                        'type': f'{bias} Pennant',
                        'category': pattern_type.category.value,
                        'bias': bias,
                        'confidence': confidence,
                        'start_idx': len(closes) - 15,
                        'end_idx': len(closes) - 1,
                        'target_price': closes[-1] * (1 + prior_trend if is_bullish else 1 + prior_trend),
                        'probability': min(confidence / 100, 0.75)
                    }

        return None

    def _detect_wedge(self, df, pattern_type):
        """Detect wedge patterns (rising/falling)"""
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values

        if len(closes) < 20:
            return None

        upper_slope, _, upper_r, _, _ = linregress(range(len(highs)), highs)
        lower_slope, _, lower_r, _, _ = linregress(range(len(lows)), lows)

        if upper_r**2 < 0.7 or lower_r**2 < 0.7:
            return None

        is_rising = upper_slope > 0 and lower_slope > 0
        is_falling = upper_slope < 0 and lower_slope < 0

        if is_rising and abs(upper_slope) < abs(lower_slope):
            confidence = min(70 + (upper_r**2 + lower_r**2) * 12, 90)
            return {
                'pattern': PatternType.RISING_WEDGE,
                'type': 'Rising Wedge',
                'category': PatternCategory.CONTINUATION.value,
                'bias': 'Bearish',
                'confidence': confidence,
                'start_idx': 0,
                'end_idx': len(closes) - 1,
                'target_price': closes[-1] * 0.95,
                'probability': min(confidence / 100, 0.75)
            }

        elif is_falling and abs(lower_slope) < abs(upper_slope):
            confidence = min(70 + (upper_r**2 + lower_r**2) * 12, 90)
            return {
                'pattern': PatternType.FALLING_WEDGE,
                'type': 'Falling Wedge',
                'category': PatternCategory.REVERSAL.value,
                'bias': 'Bullish',
                'confidence': confidence,
                'start_idx': 0,
                'end_idx': len(closes) - 1,
                'target_price': closes[-1] * 1.05,
                'probability': min(confidence / 100, 0.75)
            }

        return None

    def _detect_ascending_triangle(self, df, pattern_type):
        """Detect ascending triangle (bullish continuation)"""
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values

        if len(closes) < 20:
            return None

        peaks_idx, troughs_idx = self._find_peaks_and_troughs(closes, order=3)

        if len(peaks_idx) < 2 or len(troughs_idx) < 2:
            return None

        peak_prices = highs[peaks_idx]
        peak_variation = np.std(peak_prices) / np.mean(peak_prices)

        if peak_variation < 0.01:
            trough_prices = lows[troughs_idx]
            trough_slope, _, trough_r, _, _ = linregress(troughs_idx, trough_prices)

            if trough_slope > 0 and trough_r**2 > 0.6:
                confidence = min(70 + trough_r**2 * 20, 90)

                resistance_level = np.mean(peak_prices)
                breakout_target = resistance_level * 1.05

                return {
                    'pattern': pattern_type,
                    'type': pattern_type.display_name,
                    'category': pattern_type.category.value,
                    'bias': pattern_type.bias,
                    'confidence': confidence,
                    'start_idx': min(peaks_idx[0], troughs_idx[0]),
                    'end_idx': len(closes) - 1,
                    'resistance': resistance_level,
                    'target_price': breakout_target,
                    'probability': min(confidence / 100, 0.80)
                }

        return None

    def _detect_rectangle(self, df, pattern_type):
        """Detect rectangle pattern (consolidation)"""
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values

        if len(closes) < 20:
            return None

        peaks_idx, troughs_idx = self._find_peaks_and_troughs(closes, order=3)

        if len(peaks_idx) >= 2 and len(troughs_idx) >= 2:
            peak_variation = np.std(highs[peaks_idx]) / np.mean(highs[peaks_idx])
            trough_variation = np.std(lows[troughs_idx]) / np.mean(lows[troughs_idx])

            if peak_variation < 0.02 and trough_variation < 0.02:
                resistance = np.mean(highs[peaks_idx])
                support = np.mean(lows[troughs_idx])

                range_size = (resistance - support) / support

                if 0.02 < range_size < 0.10:
                    confidence = 75

                    return {
                        'pattern': pattern_type,
                        'type': 'Bullish Rectangle',
                        'category': pattern_type.category.value,
                        'bias': 'Bullish',
                        'confidence': confidence,
                        'start_idx': 0,
                        'end_idx': len(closes) - 1,
                        'support': support,
                        'resistance': resistance,
                        'target_price': resistance * 1.03,
                        'probability': 0.70
                    }

        return None

    def _detect_rounding_top(self, df, pattern_type):
        """Detect rounding top (bearish reversal/continuation)"""
        closes = df['close'].values

        if len(closes) < 30:
            return None

        x = np.arange(len(closes))
        coeffs = np.polyfit(x, closes, 2)

        if coeffs[0] < 0:
            fitted = np.polyval(coeffs, x)
            r_squared = 1 - (np.sum((closes - fitted)**2) / np.sum((closes - np.mean(closes))**2))

            if r_squared > 0.75:
                confidence = min(65 + r_squared * 25, 88)

                return {
                    'pattern': pattern_type,
                    'type': pattern_type.display_name,
                    'category': pattern_type.category.value,
                    'bias': 'Bearish',
                    'confidence': confidence,
                    'start_idx': 0,
                    'end_idx': len(closes) - 1,
                    'target_price': closes[-1] * 0.95,
                    'probability': min(confidence / 100, 0.75)
                }

        return None

    def _detect_rounding_triangle(self, df, pattern_type):
        """Detect rounding triangle"""
        return self._detect_rounding_top(df, pattern_type)

    def _detect_diamond(self, df, pattern_type):
        """Detect diamond patterns (both bullish and bearish)"""
        closes = df['close'].values

        if len(closes) < 30:
            return None

        mid_idx = len(closes) // 2

        first_half = closes[:mid_idx]
        second_half = closes[mid_idx:]

        first_volatility = np.std(first_half)
        second_volatility = np.std(second_half)

        if first_volatility > second_volatility * 1.5:
            prior_trend = (closes[0] - closes[-30]) / closes[-30] if len(closes) >= 30 else 0

            is_bearish = prior_trend < 0
            bias = "Bearish" if is_bearish else "Bullish"

            confidence = 70

            return {
                'pattern': pattern_type,
                'type': f'{bias} Diamond',
                'category': pattern_type.category.value,
                'bias': bias,
                'confidence': confidence,
                'start_idx': 0,
                'end_idx': len(closes) - 1,
                'target_price': closes[-1] * (0.95 if is_bearish else 1.05),
                'probability': 0.65
            }

        return None

    def _detect_tea_cup(self, df, pattern_type):
        """Detect tea cup pattern (bullish reversal)"""
        closes = df['close'].values

        if len(closes) < 40:
            return None

        cup_portion = closes[-40:-10]
        handle_portion = closes[-10:]

        x_cup = np.arange(len(cup_portion))
        coeffs = np.polyfit(x_cup, cup_portion, 2)

        if coeffs[0] > 0:
            fitted = np.polyval(coeffs, x_cup)
            r_squared = 1 - (np.sum((cup_portion - fitted)**2) / np.sum((cup_portion - np.mean(cup_portion))**2))

            if r_squared > 0.70:
                handle_slope, _, handle_r, _, _ = linregress(range(len(handle_portion)), handle_portion)

                if handle_slope < 0 or (handle_slope > 0 and handle_slope < 0.001):
                    confidence = min(70 + r_squared * 20, 92)

                    cup_depth = (max(cup_portion) - min(cup_portion)) / min(cup_portion)

                    return {
                        'pattern': pattern_type,
                        'type': pattern_type.display_name,
                        'category': pattern_type.category.value,
                        'bias': 'Bullish',
                        'confidence': confidence,
                        'start_idx': len(closes) - 40,
                        'end_idx': len(closes) - 1,
                        'target_price': closes[-1] * (1 + cup_depth),
                        'probability': min(confidence / 100 * 1.2, 0.85)
                    }

        return None

    def _detect_inverse_tea_cup(self, df, pattern_type):
        """Detect inverse tea cup pattern (bearish reversal)"""
        closes = df['close'].values

        if len(closes) < 40:
            return None

        cup_portion = closes[-40:-10]
        handle_portion = closes[-10:]

        x_cup = np.arange(len(cup_portion))
        coeffs = np.polyfit(x_cup, cup_portion, 2)

        if coeffs[0] < 0:
            fitted = np.polyval(coeffs, x_cup)
            r_squared = 1 - (np.sum((cup_portion - fitted)**2) / np.sum((cup_portion - np.mean(cup_portion))**2))

            if r_squared > 0.70:
                handle_slope, _, handle_r, _, _ = linregress(range(len(handle_portion)), handle_portion)

                if handle_slope > 0 or (handle_slope < 0 and handle_slope > -0.001):
                    confidence = min(70 + r_squared * 20, 92)

                    cup_height = (max(cup_portion) - min(cup_portion)) / max(cup_portion)

                    return {
                        'pattern': pattern_type,
                        'type': pattern_type.display_name,
                        'category': pattern_type.category.value,
                        'bias': 'Bearish',
                        'confidence': confidence,
                        'start_idx': len(closes) - 40,
                        'end_idx': len(closes) - 1,
                        'target_price': closes[-1] * (1 - cup_height),
                        'probability': min(confidence / 100 * 1.2, 0.85)
                    }

        return None

    def _calculate_pattern_confidence(self, symmetry_error, prominence, duration):
        """Calculate confidence score for a pattern"""
        symmetry_score = max(0, 100 - (symmetry_error * 1000))

        prominence_score = min(prominence * 500, 100)

        duration_score = 100 if 15 <= duration <= 45 else max(0, 100 - abs(duration - 30) * 2)

        confidence = (symmetry_score * 0.4 + prominence_score * 0.4 + duration_score * 0.2)

        return min(max(confidence, 50), 95)

    def get_pattern_summary(self, detected_patterns):
        """Get summary of detected patterns"""
        if not detected_patterns:
            return {
                'total_patterns': 0,
                'bullish_count': 0,
                'bearish_count': 0,
                'highest_confidence': None
            }

        bullish = [p for p in detected_patterns if p['bias'] == 'Bullish']
        bearish = [p for p in detected_patterns if p['bias'] == 'Bearish']

        return {
            'total_patterns': len(detected_patterns),
            'bullish_count': len(bullish),
            'bearish_count': len(bearish),
            'highest_confidence': detected_patterns[0] if detected_patterns else None,
            'patterns': [p['type'] for p in detected_patterns]
        }
