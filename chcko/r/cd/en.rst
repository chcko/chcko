.. raw:: html

    %path = "maths/finance/interest"
    %kind = kinda["texts"]
    %level = 10
    <!-- html -->
    

`K` Capital

    An amount of money. 

`i` Interest rate

    The increase or decrease of capital `K` is notated in percent %=1/100. 

    - interest value: `3\% K = 0.03 K`. 
    - increase : `K + 3\% K = (1+3\%) K = 1.03 K`.
    - decrease : `K - 3\% K = (1-3\%) K = 0.97 K`.

`n` Period (Year/Quarter/Month/Day)

    The interest rate `i` always refers to a time period, in which the increase or decrease
    takes place (is compounded)

    - `i` normally refers to a full year (annual interest rate, effective annual interest rate)
    - `i_{12}` is a monthly interest rate
    - `i_4` is a quarterly interest rate

    After this time period `K` has grown by `iK`, i.e. `K_{n=1} = K_0 (1+i) = K_0 q` (q = 1+i).

Compound interest

    After one period the capital becomes `K_{n=1} = K_0 (1+i) = K_0 q`, 
    after n=2 periods `K_0 q^2`, after n=3 periods `K_0 q^3`...

    After n periods:

    - `K_n = K_0 q^n`

    - compound interests: multiply the starting capital (principal) with `q^n`
      to get the value `n` periods later.
    - discount interests: multiply the capital with `q^{-n}` to get the value `n` periods earlier.

.. http://en.wikipedia.org/wiki/Time_value_of_money

Annuity

    An annuity is a payment `r` in regular time periods. 
    The number of periods for the annuity depends on the payment.
    The accrued payments make up the lump-sum. This is the pension or **annuity formula**: 

    `R_n = \sum_{m=0}^{n-1} r_m = \sum_{m=0}^{n-1} r q^m = r \frac{q^n - 1}{q-1}`

    The formula can be used to calculate the **future value** (FV)`R_n` 
    when the interests are compounded at the end of the periods.

    Annuity due is when compounded at the beginning: `R_n^v = q R_n`

    The **present value** (PV) of an annuity is obtained by discounting from the FV:
    `B_n = R_n q^{-n}`.

Compounding periods smaller than a year

    To compare the effective annual rate of interest with the rate for the period one converts the rates.

    In a linear conversion we use when there is no compounding taking place 

    - `i_{12} = i/12`
    - `i_4 = i/4`

    With compounding the effective annual interest rate is calculated with the **conformal** conversion:
    Effective `i_{eff}` distinguishes from nominal interest rate `i`.

    - `i_{eff} = (i_{12} + 1)^{12} - 1`
    - `i_{eff} = (i_4 + 1)^4 - 1`

    Normally the annual interest rate is given.
    For a monthly or quarterly compounding this first needs to be converted.

Annuity rest

    To calculate the remaining value of the annuity at a certain time
    one subtracts the future value of the annuity for that time from
    the capital value for that time.

Convert one annuity to another 

    - First one finds the future value `R_n`. 
    - This `R_n` needs to be compounded to the end of the other annuity.
    - Using the annuity formula one can calculate the requested quantity (`n`, `q`, `r`) 
      of the new annuity.

Comparison of capitals or offers

    To compare values one must first compound their values to the same time
    (time-value, e.g. present value) using the compounding or annuity formulas.


