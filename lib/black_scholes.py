import math

# double opt_price(bool is_call,double spot,double strike,double texp,double vol,double rd,double rf)
# {
#     if (vol<=0 or texp<=0 or strike <= 0)
#     {
#         // return intrinsic value
#         double int_val = spot*exp(-rf*texp)-strike*exp(-rd*texp);
#         if (!is_call) int_val *= -1;
#         if (int_val<0) int_val = 0;
#         return int_val;
#     }
    
#     // otherwise calculate the standard value
    
#     double d1 = calc_d1(spot,strike,texp,vol,rd,rf);
#     double d2 = d1 - vol*sqrt(texp);
    
#     if (is_call)
#         return spot*exp(-rf*texp)*cnorm(d1) - strike*exp(-rd*texp)*cnorm(d2);
#     else
#         return strike*exp(-rd*texp)*cnorm(-d2) - spot*exp(-rf*texp)*cnorm(-d1);
# }

def opt_price(is_call, spot, strike, texp, vol, rd, rf):
    if vol <= 0 or texp <= 0 or strike <= 0:
        # return intrinsic value
        int_val = spot * math.exp(-rf * texp) - strike * math.exp(-rd * texp)
        
        if not is_call: 
            int_val *= -1
        
        return max(int_val, 0)
    
    # otherwise calculate the standard value
    d1 = calc_d1(spot, strike, texp, vol, rd, rf)
    d2 = d1 - vol * math.sqrt(texp)
    
    if is_call:
        return spot * math.exp(-rf * texp) * cnorm(d1) - strike * math.exp(-rd * texp) * cnorm(d2)
    else:
        return strike * math.exp(-rd * texp) * cnorm(-d2) - spot * math.exp(-rf * texp) * cnorm(-d1)


# double opt_delta(bool is_call,double spot,double strike,double texp,double vol,double rd,double rf)
# {
#     if (vol<=0 or texp<=0)
#     {
#         // return intrinsic delta
#         double int_val = spot*exp(-rf*texp)-strike*exp(-rd*texp);
#         if (!is_call) int_val *= -1;
#         if (int_val<0)
#             return 0;
#         else if (is_call)
#             return exp(-rf*texp);
#         else
#             return -exp(-rf*texp);
#     }
    
#     // otherwise calculate the standard value
    
#     if (is_call)
#         return exp(-rf*texp)*cnorm(calc_d1(spot,strike,texp,vol,rd,rf));
#     else
#         return -exp(-rf*texp)*cnorm(-calc_d1(spot,strike,texp,vol,rd,rf));
# }

def opt_delta(is_call, spot, strike, texp, vol, rd, rf):
    if vol <= 0 or texp <= 0:
        # return intrinsic delta
        int_val = spot * math.exp(-rf * texp) - strike * math.exp(-rd * texp)
        
        if not is_call:
            int_val *= -1
        
        if int_val < 0:
            return 0
        elif is_call:
            return math.exp(-rf * texp)
        else:
            return -math.exp(-rf * texp)
    
    # otherwise calculate the standard value
    if is_call:
        return math.exp(-rf * texp) * cnorm(calc_d1(spot, strike, texp, vol, rd, rf))
    else:
        return -math.exp(-rf * texp) * cnorm(-calc_d1(spot, strike, texp, vol, rd, rf))


# static double calc_d1(double spot,double strike,double texp,double vol,double rd,double rf)
# {
#     return (log(spot/strike)+(rd-rf+vol*vol/2.)*texp)/vol/sqrt(texp);
# }

def calc_d1(spot, strike, texp, vol, rd, rf):
    """ Calculates the d_1 value in the Black-Scholes formula with continuous yield dividends
    
    See https://en.wikipedia.org/wiki/Black–Scholes_model
    
    Parameters
    ----------
    spot : float
        Current spot price (S_t)
    strike : float
        Strike price (K)
    texp : float
        Time to maturity (in years) (T - t)
    vol : float
        Volatility of returns of the underlying asset (σ)
    rd : float
        
    rf : float
        Dividend yield (q)
    
    """
    return (math.log(spot / strike) + (rd - rf + vol * vol / 2.) * texp) / vol / math.sqrt(texp)


# double cnorm(double x)
# {
#     double xabs=fabs(x);
#     double f;
#     if(xabs>37)
#         f = 0;
#     else
#     {
#         double e = exp(-xabs*xabs/2.);
#         if(xabs<7.07106781186547)
#         {
#             double y = 3.52624965998911e-02 * xabs + 0.700383064443688;
#             y = y * xabs + 6.37396220353165;
#             y = y * xabs + 33.912866078383;
#             y = y * xabs + 112.079291497871;
#             y = y * xabs + 221.213596169931;
#             y = y * xabs + 220.206867912376;
#             f = e * y;
#             y = 8.83883476483184e-02 * xabs + 1.75566716318264;
#             y = y * xabs + 16.064177579207;
#             y = y * xabs + 86.7807322029461;
#             y = y * xabs + 296.564248779674;
#             y = y * xabs + 637.333633378831;
#             y = y * xabs + 793.826512519948;
#             y = y * xabs + 440.413735824752;
#             f /= y;
#         }
#         else
#         {
#             double y = xabs + 0.65;
#             y = xabs + 4 / y;
#             y = xabs + 3 / y;
#             y = xabs + 2 / y;
#             y = xabs + 1 / y;
#             f = e / y / 2.506628274631;
#         }
#     }

#     if(x>0) f = 1-f;
    
#     return f;
# }

def cnorm(x):
    xabs = abs(x)
    f = None
    
    if xabs > 37:
        f = 0
    else:
        e = math.exp(-xabs * xabs / 2.)
        
        if xabs < 7.07106781186547:
            y = 3.52624965998911e-02 * xabs + 0.700383064443688
            y = y * xabs + 6.37396220353165
            y = y * xabs + 33.912866078383
            y = y * xabs + 112.079291497871
            y = y * xabs + 221.213596169931
            y = y * xabs + 220.206867912376
            f = e * y
            y = 8.83883476483184e-02 * xabs + 1.75566716318264
            y = y * xabs + 16.064177579207
            y = y * xabs + 86.7807322029461
            y = y * xabs + 296.564248779674
            y = y * xabs + 637.333633378831
            y = y * xabs + 793.826512519948
            y = y * xabs + 440.413735824752
            f /= y
        else:
            y = xabs + 0.65
            y = xabs + 4 / y
            y = xabs + 3 / y
            y = xabs + 2 / y
            y = xabs + 1 / y
            f = e / y / 2.506628274631
    
    if x > 0:
        f = 1 - f
    
    return f
