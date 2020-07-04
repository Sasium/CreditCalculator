import math
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--payment", type=int)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
args = parser.parse_args()
type_check = args.type != "annuity" and args.type != "diff"
conflict_check = args.type == "diff" and args.payment
quantity_check = len(vars(args)) < 4
if type_check or conflict_check or quantity_check or not args.interest:
    print("Incorrect parameters")
elif not args.payment and args.type == "annuity":
    negativity_check = args.principal < 0 or args.periods < 0\
                       or args.interest < 0
    if negativity_check:
        print("Incorrect parameters")
    else:
        monthly_credit_interest = args.interest / (12 * 100)
        numerator = monthly_credit_interest * math.pow(1 + monthly_credit_interest,
                                                       args.periods)
        denominator = math.pow(1 + monthly_credit_interest, args.periods) - 1
        payment = args.principal * numerator / denominator
        overpayment = math.ceil(payment) * args.periods - args.principal
        print("""Your annuity payment = {}!
              Overpayment = {}""".format(math.ceil(payment), overpayment))
elif not args.payment and args.type == "diff":
    negativity_check = args.principal < 0 or args.periods < 0\
                       or args.interest < 0
    if negativity_check:
        print("Incorrect parameters")
    else:
        monthly_credit_interest = args.interest / (12 * 100)
        payment = []
        overpayment = 0
        for i in range(0, args.periods):
            payment.append(math.ceil(args.principal / args.periods
                           + monthly_credit_interest
                           * (args.principal - args.principal * i / args.periods)))
            overpayment += payment[i]
            print("Month {}: paid out {}".format(i + 1, payment[i]))
        overpayment -= args.principal
        print("Overpayment = {}".format(overpayment))
elif not args.principal:
    negativity_check = args.payment < 0 or args.periods < 0\
                       or args.interest < 0
    if negativity_check:
        print("Incorrect parameters")
    else:
        monthly_credit_interest = args.interest / (12 * 100)
        numerator = monthly_credit_interest * math.pow(1 + monthly_credit_interest,
                                                       args.periods)
        denominator = math.pow(1 + monthly_credit_interest, args.periods) - 1
        credits_principal = args.payment * denominator / numerator
        overpayment = args.payment * args.periods - credits_principal
        print("""Your credit principal = {}!
        Overpayment = {}""".format(credits_principal, math.ceil(overpayment)))
else:
    negativity_check = args.payment < 0 or args.principal < 0\
                       or args.interest < 0
    if negativity_check:
        print("Incorrect parameters")
    else:
        monthly_credit_interest = args.interest / (12 * 100)
        count_of_payments = math.log(args.payment
                                     / (args.payment - monthly_credit_interest
                                        * args.principal),
                                     1 + monthly_credit_interest)
        count_of_months = int(math.ceil(count_of_payments % 12))
        count_of_years = int(count_of_payments // 12)
        if count_of_months == 12:
            count_of_months = 0
            count_of_years += 1
        if count_of_months == 1:
            count_of_months = "1 month"
        elif count_of_months != 0:
            count_of_months = str(count_of_months) + " months"
        if count_of_years == 1:
            count_of_years = "1 year"
        elif count_of_years != 0:
            count_of_years = str(count_of_years) + " years"
        if count_of_months != 0 and count_of_years != 0:
            format_text = str(count_of_years) + " and " + str(count_of_months)
        elif count_of_months == 0:
            format_text = str(count_of_years)
        else:
            format_text = str(count_of_months)
        print("You need {} to repay this credit".format(format_text))
        overpayment = math.ceil(count_of_payments) * args.payment - args.principal
        print("Overpayment = {}".format(overpayment))
