

# def monthlyPayment(principal, year_rate, year_duration):
#     monthly_rate = year_rate / (12 * 100)   # convert 4.9 to 0.049 and  monthly interest rate
#     month_amounts =  year_duration * 12

#     # 每月月供
#     monthly_payment = (principal * monthly_rate * (1 + monthly_rate) ** month_amounts) / (
#     (1 + monthly_rate) ** month_amounts - 1)
#     #总利息
#     total_interest_payable = monthly_payment * month_amounts - principal
#     print('-----------------------------------')
#     print ('Total interest payable is %.2f ' % total_interest_payable)

#     for i in range (1, month_amounts + 1):
#         #每月应还利息
#         monthly_interest_payable = principal * monthly_rate * ((1 + monthly_rate) ** month_amounts - (1 + monthly_rate) ** (i - 1 ))/ ((1 + monthly_rate) ** month_amounts -1)
#         #每月应还本金
#         monthly_principal_payable = principal * monthly_rate * (1 + monthly_rate) ** (i - 1)/ ((1 + monthly_rate) ** month_amounts -1)
#         #每月利息占比
#         monthly_interest_percentage = monthly_interest_payable * 100 / monthly_payment

#         print('-----------------------------------')
#         print ('%dth monthly payment is : %.2f (Interest: %.2f and Principal: %.2f)' % (i, monthly_payment,monthly_interest_payable,monthly_principal_payable))
#         print('%dth month interest percentage is %.2f %%' % (i, monthly_interest_percentage))

#     return


# if __name__ == '__main__':
#     principal = int(input('Please input your loan amounts:'))
#     year_rate = float(input('Please input Year Debt Interest Rate:(such as 4.9,it means 4.9%)'))
#     year_duration = int(input('Please input Debt Year Duration:'))
#     monthlyPayment(principal, year_rate, year_duration)