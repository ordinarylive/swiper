"""错误码"""

OK=0
PLATFORM_ERR=1000 #第三方平台错误
PHONE_ERR=1001    #手机号错误
VCODE_ERR=1002    #无效验证码
LOGIN_REQUIRE=1003  #用户尚未登录
PROFILE_ERR=1004   #个人资料错误
FLAG_ERROR=1005    #滑动类型错误


class LogicError(Exception):
    # 逻辑错误的基类
    code=None





def gen_logic_error(name,code):
    #创建一个逻辑错误
   return type(name,(LogicError,),{'code':code})




OK=gen_logic_error('OK',0)
PlatformErr=gen_logic_error('PlatformErr',1000)
PhoneErr=gen_logic_error('PhoneErr',1001)
VcodeErr=gen_logic_error('VcodeErr',1002)
LoginRequire=gen_logic_error('LoginRequire',1003)
ProfileErr=gen_logic_error('ProfileErr',1004)
FlagErr=gen_logic_error('FlagErr',1005)
















