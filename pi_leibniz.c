#include <stdio.h>

/* Recursive calculation of pi using the Leibniz formula */

/* Custom absolute value */
static long double abs_ld(long double x) {
    return x < 0 ? -x : x;
}

/* Compute 10^digits without using math.h */
static long double power_of_10(int digits) {
    long double result = 1.0L;
    for (int i = 0; i < digits; i++) {
        result *= 10.0L;
    }
    return result;
}

/* Recursive Leibniz series summation */
static long double leibniz_recursive(long long k, long double threshold) {
    long double term = 1.0L / (2.0L * k + 1.0L);
    if (k % 2 != 0) {
        term = -term;
    }
    if (abs_ld(term) < threshold) {
        return term;
    }
    return term + leibniz_recursive(k + 1, threshold);
}

/* Compute pi using the Leibniz series with given decimal accuracy */
static long double compute_pi(int digits) {
    long double threshold = 1.0L / power_of_10(digits);
    long double sum = leibniz_recursive(0, threshold);
    return 4.0L * sum;
}

int main(void) {
    int digits;
    printf("Anzahl der Stellen hinter dem Komma: ");
    if (scanf("%d", &digits) != 1 || digits < 0) {
        printf("Ungueltige Eingabe.\n");
        return 1;
    }

    long double pi = compute_pi(digits);
    printf("Naehereung fuer Pi: %.*Lf\n", digits, pi);
    return 0;
}
