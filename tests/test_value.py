# -*- coding: utf-8 -*-
#
#    BitcoinLib - Python Cryptocurrency Library
#    Unit Tests for Value Class
#    © 2020 November - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
from bitcoinlib.values import *


class TestValue(unittest.TestCase):

    def test_value_class(self):
        self.assertEqual(str(Value(10)), '10.00000000 BTC')
        self.assertEqual(int(Value(10)), 10)
        self.assertEqual((Value(10).__repr__()),
                         "Value(value=10, denominator=1.00000000, network='bitcoin')")
        self.assertEqual(str(Value('10')), '10.00000000 BTC')
        self.assertEqual(str(Value('10 ltc')), '10.00000000 LTC')
        self.assertEqual(str(Value('10', network='litecoin')), '10.00000000 LTC')
        self.assertEqual(str(Value('10', network='dash_testnet')), '10.00000000 tDASH')
        self.assertEqual(str(Value('10 tDASH')), '10.00000000 tDASH')
        self.assertEqual(float(Value('0.001 BTC')), 0.001)
        self.assertEqual(float(Value('1 msat')), 0.00000000001)
        self.assertEqual(int(Value('1 BTC')), 1)
        self.assertEqual(str(Value('10 mBTC')), '10.00000 mBTC')
        self.assertEqual(float(Value('10 mBTC')), 0.01)
        self.assertEqual(str(Value(10, 'm')), '10.00000 mBTC')
        self.assertEqual(str(Value('10 µBTC')), '10.00 µBTC')
        self.assertEqual(float(Value('10 µBTC')), 0.00001)
        self.assertEqual(str(Value(10, 'µ')), '10.00 µBTC')
        self.assertEqual(str(Value(10, 'sat')), '10 sat')
        self.assertEqual(float(Value(10, 'sat')), 0.0000001)
        self.assertEqual(str(Value(10, 'k')), '10.00000000 kBTC')
        self.assertEqual(str(Value('10 sat')), '10 sat')
        self.assertEqual(float(Value('10 sat')), 0.0000001)
        self.assertEqual(str(Value('10 satLTC')), '10 satLTC')
        self.assertEqual(str(Value('10 sat', network='litecoin')), '10 satLTC')
        self.assertRaisesRegex(ValueError, "Currency symbol not recognised", Value, '10 mfliepflap')

    def test_value_class_str(self):
        self.assertEqual(Value(10).str(), '10.00000000 BTC')
        self.assertEqual(Value(10).str('m'), '10000.00000 mBTC')
        self.assertEqual(Value(10).str('mBTC'), '10000.00000 mBTC')
        self.assertEqual(Value(10).str('MBTC'), '0.00001000 MBTC')
        self.assertEqual(Value(12.3, 'sat').str('sat'), '12 sat')
        self.assertEqual(Value(12.3, 'sat').str(0.00000001), '12 sat')
        self.assertEqual(Value(12.3, 'sat').str('n'), '123 nBTC')
        self.assertEqual(Value(12.3, 'sat').str('nBTC'), '123 nBTC')
        self.assertEqual(Value(12345678.901, 'sat').str('mBTC'), '123.45679 mBTC')
        self.assertEqual(Value(012345678.901, 'sat').str('mBTC', decimals=8), '123.45678901 mBTC')
        self.assertEqual(Value(012345678.9016, 'sat').str('mBTC', decimals=8), '123.45678902 mBTC')
        self.assertEqual(Value(012345678.90122, 'sat').str('mBTC', decimals=10), '123.4567890122 mBTC')
        self.assertEqual(Value(012345678.901, 'sat').str('mBTC', decimals=1), '123.5 mBTC')
        self.assertEqual(Value(12.3, 'sat').str('msat'), '12300 msat')
        self.assertEqual(Value(12.3, 'sat').str('µsat'), '12300000 µsat')
        self.assertEqual(Value(10).str('m'), '10000.00000 mBTC')
        self.assertEqual(Value(10000000000000).str('m'), '10000000000000000.00000 mBTC')
        self.assertEqual(Value(10).str(0.001), '10000.00000 mBTC')
        self.assertEqual(Value('10 kBTC').str(1), '10000.00000000 BTC')
        self.assertEqual(Value('10 kLTC').str(1), '10000.00000000 LTC')
        self.assertEqual(Value('0.00021 YBTC').str(1), '210000000000000000000.00000000 BTC')
        self.assertEqual(Value('127127504620 Doge').str('TDoge'), '0.12712750 TDOGE')
        self.assertRaisesRegex(ValueError, "Denominator not found in NETWORK_DENOMINATORS definition",
                                Value('123 Dash').str, 'DD')

    def test_value_class_str_auto(self):
        pass
    
    def test_value_operators_comparison(self):
        self.assertTrue(Value(3) < Value(5))
        self.assertTrue(Value(3) <= Value(3))
        self.assertTrue(Value(3) == Value(3))
        self.assertFalse(Value(3) > Value(5))
        self.assertTrue(Value(3) >= Value(3))
        self.assertFalse(Value(3) != Value(3))
        self.assertTrue(Value("3 BTC") < Value("5000 mBTC"))
        self.assertTrue(Value("1 sat") == Value("0.00001 mBTC"))
        self.assertTrue(Value("10 sat") == Value("1 fin"))
        self.assertTrue(Value("10 satLTC") == Value("1 finLTC"))
        v1 = Value("10 sat")
        v2 = Value("1 finLTC")
        self.assertRaisesRegex(ValueError, "Cannot compare values from different networks", Value.__eq__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot compare values from different networks", Value.__lt__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot compare values from different networks", Value.__le__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot compare values from different networks", Value.__gt__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot compare values from different networks", Value.__ge__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot compare values from different networks", Value.__ne__, v1, v2)

    def test_value_operators_arithmetic(self):
        value1 = Value('3 BTC')
        self.assertEqual(value1 + Value('500 mBTC'), Value('3.50000000 BTC'))
        self.assertEqual(value1 - Value('500 mBTC'), Value('2.50000000 BTC'))
        self.assertEqual(str(value1 + 0.5), '3.50000000 BTC')
        self.assertEqual(str(value1 - 0.5), '2.50000000 BTC')
        self.assertEqual(str(value1 * 2), '6.00000000 BTC')
        value1 += Value(2)
        self.assertEqual(str(value1), '5.00000000 BTC')
        value1 -= Value(2)
        self.assertEqual(str(value1), '3.00000000 BTC')
        self.assertEqual(str(Value('2 BTC') / 3), '0.66666667 BTC')
        self.assertEqual(str(Value('2000 BTC') // 3), '666.00000000 BTC')
        # self.assertEqual(str(Value('5000000 sat') // 3), '666.00000000 BTC')
        self.assertEqual(str(round(Value('2 BTC') / 3, 2)), '0.67000000 BTC')
        self.assertEqual(str(round(Value('2 BTC') / 3)), '1.00000000 BTC')
        v1 = Value("10 BTC")
        v2 = Value("5 LTC")
        self.assertRaisesRegex(ValueError, "Cannot calculate with values from different networks",
                               Value.__add__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot calculate with values from different networks",
                               Value.__sub__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot calculate with values from different networks",
                               Value.__isub__, v1, v2)
        self.assertRaisesRegex(ValueError, "Cannot calculate with values from different networks",
                               Value.__iadd__, v1, v2)

    def test_value_operators_conversion(self):
        v2 = Value('21000000 BTC')
        self.assertEqual(hex(v2.value_sat), '0x775f05a074000')
        self.assertEqual(v2.to_hex(16, 'little'), '0040075af0750700')
        self.assertEqual(v2.to_bytes(8, 'little').hex(), '0040075af0750700')
        self.assertEqual(hex(v2.value_sat), '0x775f05a074000')
        self.assertEqual(bin(Value('2 BTC').value_sat), '0b1011111010111100001000000000')
        self.assertAlmostEqual(float(Value('2 BTC') / 3), 0.66666666)
        self.assertEqual(float(Value('2000 BTC') // 3), 666)
        self.assertEqual(int(Value('2000 BTC') / 3), 666)
