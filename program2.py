#
# int toNum(string s) {
# 	return stoi(s, nullptr, 2);
# }
#
# string toString(int n) {
# 	char temp[64];
# 	itoa(n, temp, 2);
# 	return temp;
# }
#
# string unshiftZero(int shouldLength, string base) {
# 	if (shouldLength == base.length()) {
# 		return base;
# 	}
# 	else {
# 		string temp(shouldLength - base.length(), '0');
# 		return (temp + base);
# 	}
# }
#
# string binaryKaratsuba(string x, string y, int N) {
# 	if (N == 1) {
# 		return x == "1" && y == "1" ? "1" : "0";
# 	}
# 	else {
#         //	将x,y分成两部分,每部分n/2位
# 		string xLeft = x.substr(0, N / 2);
# 		string xRight = x.substr(N / 2);
# 		string yLeft = y.substr(0, N / 2);
# 		string yRight = y.substr(N / 2);
#
#         //	左右两部分二进制数相加作为中间值
# 		string middleware1 = toString(toNum(xLeft) + toNum(xRight));
# 		string middleware2 = toString(toNum(yLeft) + toNum(yRight));
#
#         //	中间值位数不足时往前补零
# 		if (middleware1.length() != N / 2 || middleware2.length() != N / 2) {
# 			int shouldLength = max(middleware1.length(), middleware2.length()) > N / 2
# 													?	N : N / 2;
# 			middleware1 = unshiftZero(shouldLength, middleware1);
# 			middleware2 = unshiftZero(shouldLength, middleware2);
# 		}
#
# 		int res1 = toNum(binaryKaratsuba(xLeft, yLeft, N / 2));
# 		int res2 = toNum(binaryKaratsuba(middleware1, middleware2, middleware1.length()));
# 		int res3 = toNum(binaryKaratsuba(xRight, yRight, N / 2));
#
#         //	XY=AC * 2^n + [(A+B)(C+D)-AC-BD] * 2^(n/2) + BD
# 		return toString((res1 << N) + ((res2 - res1 - res3) << (N / 2)) + res3);
# 	}
# }
