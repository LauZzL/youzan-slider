import youzan


yz = youzan.YouZan()
yz.get_token()
yz.get_captcha()
solution = yz.check()
print(solution)
