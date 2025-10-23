import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class TradingAnarchyAnalyzer:
    """
    Trading Anarchy 4-Push Detection System

    Based on the aircraft mechanic analogy:
    - Bolt turns = Price pushes
    - Thread pitch = Market unit of movement (pips per push)
    - Torque limit = Trading exhaustion point (4 pushes)

    This system detects when a market move is approaching exhaustion
    by counting pushes and measuring the typical movement unit.
    """

    def __init__(self, exhaustion_pushes=4):
        self.exhaustion_pushes = exhaustion_pushes
        self.push_history = []

        logger.info(f'TradingAnarchyAnalyzer initialized: exhaustion at {exhaustion_pushes} pushes')

    def analyze_market(self, price_data, target_pips=None):
        """
        Analyze market for push structure and exhaustion signals

        Args:
            price_data: DataFrame or dict with OHLC data
            target_pips: Optional target movement in pips

        Returns:
            Dictionary with push analysis and exhaustion warnings
        """
        if isinstance(price_data, dict):
            df = pd.DataFrame(price_data)
        else:
            df = price_data.copy()

        if len(df) < 20:
            logger.warning('Insufficient data for push analysis')
            return self._default_analysis()

        pushes = self._detect_pushes(df)

        if len(pushes) == 0:
            return self._default_analysis()

        push_unit = self._calculate_push_unit(pushes)

        current_trend = self._identify_current_trend(df)

        active_pushes = [p for p in pushes if p['direction'] == current_trend]

        exhaustion_level = len(active_pushes) / self.exhaustion_pushes

        if target_pips:
            expected_pushes = self._calculate_expected_pushes(target_pips, push_unit)
            remaining_pushes = max(0, expected_pushes - len(active_pushes))
        else:
            expected_pushes = None
            remaining_pushes = max(0, self.exhaustion_pushes - len(active_pushes))

        reversal_probability = self._calculate_reversal_probability(
            len(active_pushes),
            push_unit,
            df
        )

        warning_level = self._get_warning_level(exhaustion_level)

        return {
            'total_pushes': len(pushes),
            'active_pushes': len(active_pushes),
            'current_trend': current_trend,
            'push_unit_pips': round(push_unit, 2),
            'exhaustion_level': round(exhaustion_level * 100, 1),
            'exhaustion_threshold': self.exhaustion_pushes,
            'warning_level': warning_level,
            'reversal_probability': round(reversal_probability * 100, 1),
            'remaining_safe_pushes': remaining_pushes,
            'expected_pushes_to_target': expected_pushes,
            'is_exhausted': len(active_pushes) >= self.exhaustion_pushes,
            'should_exit': len(active_pushes) >= self.exhaustion_pushes,
            'push_details': active_pushes,
            'analogy': self._get_analogy_explanation(len(active_pushes), push_unit, target_pips)
        }

    def _detect_pushes(self, df):
        """
        Detect individual pushes (momentum waves) in price data

        A push is defined as a significant directional move followed by
        a consolidation or minor retracement.
        """
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values

        price_changes = np.diff(closes)

        momentum = pd.Series(closes).rolling(window=5).apply(
            lambda x: x.iloc[-1] - x.iloc[0]
        ).fillna(0).values

        threshold = np.std(price_changes) * 1.5

        pushes = []
        in_push = False
        push_start_idx = 0
        push_start_price = 0
        push_direction = None

        for i in range(1, len(momentum)):
            current_momentum = momentum[i]

            if not in_push:
                if abs(current_momentum) > threshold:
                    in_push = True
                    push_start_idx = i
                    push_start_price = closes[i]
                    push_direction = 'bullish' if current_momentum > 0 else 'bearish'

            else:
                if abs(current_momentum) < threshold * 0.3:
                    push_end_idx = i
                    push_end_price = closes[i]

                    push_magnitude = abs(push_end_price - push_start_price)
                    push_magnitude_pips = self._price_to_pips(push_magnitude, push_start_price)

                    if push_magnitude_pips > 5:
                        pushes.append({
                            'start_idx': push_start_idx,
                            'end_idx': push_end_idx,
                            'start_price': push_start_price,
                            'end_price': push_end_price,
                            'magnitude': push_magnitude,
                            'magnitude_pips': push_magnitude_pips,
                            'direction': push_direction,
                            'duration': push_end_idx - push_start_idx
                        })

                    in_push = False

                elif (push_direction == 'bullish' and current_momentum < -threshold) or \
                     (push_direction == 'bearish' and current_momentum > threshold):

                    in_push = False

        if in_push:
            push_end_idx = len(closes) - 1
            push_end_price = closes[-1]
            push_magnitude = abs(push_end_price - push_start_price)
            push_magnitude_pips = self._price_to_pips(push_magnitude, push_start_price)

            if push_magnitude_pips > 5:
                pushes.append({
                    'start_idx': push_start_idx,
                    'end_idx': push_end_idx,
                    'start_price': push_start_price,
                    'end_price': push_end_price,
                    'magnitude': push_magnitude,
                    'magnitude_pips': push_magnitude_pips,
                    'direction': push_direction,
                    'duration': push_end_idx - push_start_idx,
                    'is_current': True
                })

        return pushes

    def _calculate_push_unit(self, pushes):
        """
        Calculate the typical unit of movement (thread pitch analogy)

        This represents the average pips per push in the market
        """
        if len(pushes) == 0:
            return 25.0

        push_magnitudes = [p['magnitude_pips'] for p in pushes]

        median_push = np.median(push_magnitudes)

        return median_push

    def _identify_current_trend(self, df):
        """Identify the current market trend direction"""
        closes = df['close'].values

        if len(closes) < 20:
            return 'neutral'

        recent_trend = closes[-1] - closes[-20]

        if recent_trend > 0:
            return 'bullish'
        elif recent_trend < 0:
            return 'bearish'
        else:
            return 'neutral'

    def _calculate_expected_pushes(self, target_pips, push_unit):
        """
        Calculate expected number of pushes to reach target

        Like calculating bolt turns: target distance / thread pitch = turns needed
        """
        if push_unit == 0:
            return self.exhaustion_pushes

        expected = target_pips / push_unit

        return max(1, round(expected))

    def _calculate_reversal_probability(self, active_push_count, push_unit, df):
        """
        Calculate probability of reversal based on push count

        Probability increases exponentially as we approach the 4th push
        """
        if active_push_count == 0:
            return 0.1

        exhaustion_ratio = active_push_count / self.exhaustion_pushes

        base_probability = min(exhaustion_ratio ** 2, 0.95)

        volatility = df['close'].pct_change().std()
        volatility_factor = min(volatility * 10, 0.15)

        volume_declining = self._check_volume_decline(df)
        volume_factor = 0.10 if volume_declining else 0

        total_probability = min(base_probability + volatility_factor + volume_factor, 0.98)

        return total_probability

    def _check_volume_decline(self, df):
        """Check if volume is declining (sign of exhaustion)"""
        if 'volume' not in df.columns:
            return False

        recent_volume = df['volume'].tail(10).mean()
        earlier_volume = df['volume'].tail(30).head(20).mean()

        return recent_volume < earlier_volume * 0.8

    def _get_warning_level(self, exhaustion_level):
        """Get warning level based on exhaustion"""
        if exhaustion_level >= 1.0:
            return 'CRITICAL'
        elif exhaustion_level >= 0.75:
            return 'HIGH'
        elif exhaustion_level >= 0.50:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _price_to_pips(self, price_change, base_price):
        """
        Convert price change to pips

        For forex: 1 pip = 0.0001 for most pairs (0.01 for JPY pairs)
        For crypto: 1 pip = 1 unit of base currency
        """
        if base_price < 10:
            pip_value = 0.0001
        elif base_price < 200:
            pip_value = 0.01
        else:
            pip_value = 1.0

        pips = abs(price_change / pip_value)

        return pips

    def _get_analogy_explanation(self, active_pushes, push_unit, target_pips):
        """Get the aircraft mechanic analogy explanation"""
        if target_pips:
            expected_pushes = self._calculate_expected_pushes(target_pips, push_unit)

            return {
                'bolt_analogy': 'Tightening a rotor bolt',
                'turns_completed': active_pushes,
                'turns_needed': expected_pushes,
                'thread_pitch': f'{push_unit:.1f} pips per push',
                'target_distance': f'{target_pips} pips',
                'status': f'Completed {active_pushes}/{expected_pushes} pushes',
                'warning': 'Stop trading after 4th push to avoid reversal' if active_pushes >= self.exhaustion_pushes else 'Safe to continue'
            }
        else:
            return {
                'bolt_analogy': 'Tightening a rotor bolt',
                'turns_completed': active_pushes,
                'max_safe_turns': self.exhaustion_pushes,
                'thread_pitch': f'{push_unit:.1f} pips per push',
                'status': f'Push {active_pushes}/4',
                'warning': 'STOP - Exhaustion point reached!' if active_pushes >= self.exhaustion_pushes else f'Safe for {self.exhaustion_pushes - active_pushes} more pushes'
            }

    def _default_analysis(self):
        """Return default analysis when insufficient data"""
        return {
            'total_pushes': 0,
            'active_pushes': 0,
            'current_trend': 'neutral',
            'push_unit_pips': 25.0,
            'exhaustion_level': 0,
            'exhaustion_threshold': self.exhaustion_pushes,
            'warning_level': 'LOW',
            'reversal_probability': 10.0,
            'remaining_safe_pushes': self.exhaustion_pushes,
            'expected_pushes_to_target': None,
            'is_exhausted': False,
            'should_exit': False,
            'push_details': [],
            'analogy': {
                'bolt_analogy': 'Insufficient data for analysis',
                'status': 'Awaiting more price data'
            }
        }

    def get_trading_recommendation(self, push_analysis):
        """
        Get trading recommendation based on push analysis

        Returns:
            Dictionary with action recommendation
        """
        if push_analysis['is_exhausted']:
            return {
                'action': 'EXIT',
                'reason': f'Market exhausted after {push_analysis["active_pushes"]} pushes',
                'confidence': 90,
                'urgency': 'HIGH'
            }

        elif push_analysis['warning_level'] == 'HIGH':
            return {
                'action': 'REDUCE_POSITION',
                'reason': f'Approaching exhaustion: {push_analysis["remaining_safe_pushes"]} push(es) remaining',
                'confidence': 75,
                'urgency': 'MEDIUM'
            }

        elif push_analysis['warning_level'] == 'MEDIUM':
            return {
                'action': 'HOLD',
                'reason': f'Normal push progression: {push_analysis["active_pushes"]}/4 pushes complete',
                'confidence': 70,
                'urgency': 'LOW'
            }

        else:
            return {
                'action': 'CONTINUE',
                'reason': 'Early in push cycle, safe to continue',
                'confidence': 80,
                'urgency': 'LOW'
            }
